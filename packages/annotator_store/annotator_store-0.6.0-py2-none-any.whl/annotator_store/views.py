from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from eulcommon.djangoextras.auth import login_required_with_ajax, \
    permission_required_with_ajax
from eulcommon.djangoextras.http.responses import HttpResponseSeeOtherRedirect
import six

from .models import get_annotation_model, ANNOTATION_OBJECT_PERMISSIONS
from .utils import absolutize_url, permission_required


# get and use configured annotation model
Annotation = get_annotation_model()


class AnnotationIndex(View):
    'Annotator store API index view, with information and links for API urls.'

    def get(self, request):
        # Include absolute API links as per annotator 2.0 documentation
        # http://docs.annotatorjs.org/en/latest/modules/storage.html#storage-api
        base_url = absolutize_url(reverse('annotation-api:index'))

        return JsonResponse({
            "name": "Annotator Store API",
            "version": "2.0.0",
            "links": {
                "annotation": {
                    "create": {
                        "desc": "Create a new annotation",
                        "method": "POST",
                        "url": "%sannotations" % base_url
                    },
                    "delete": {
                        "desc": "Delete an annotation",
                        "method": "DELETE",
                        "url": "%sannotations/:id" % base_url
                    },
                    "read": {
                        "desc": "Get an existing annotation",
                        "method": "GET",
                        "url": "%sannotations/:id" % base_url
                    },
                    "update": {
                        "desc": "Update an existing annotation",
                        "method": "PUT",
                        "url": "%sannotations/:id" % base_url
                    }
                },
                "search": {
                    "desc": "Basic search API",
                    "method": "GET",
                    "url": "%ssearch" % base_url
                }
            }
        })


non_ajax_error_msg = 'Currently Annotations can only be updated or created via AJAX.'


class Annotations(View):
    """API annotations view.

    On GET, lists annotations.
    On AJAX POST with json data in request body, creates a new
    annotation.

    Users must be logged in to create new annotations, and can only
    view their own annotations.
    """

    def get(self, request):
        'List viewable annotations as JSON.'
        # NOTE: this method doesn't *technically* require that the user
        # be logged in, but under current permission model, no
        # annotations will be visible to anonymous users.

        notes = Annotation.objects.visible_to(request.user)
        # TODO: sort order?

        # TODO: pagination? look at reference implementation
        return JsonResponse([n.info() for n in notes], safe=False)

    @method_decorator(permission_required('annotator_store.add_annotation'))
    def post(self, request):
        'Create a new annotation via AJAX.'
        # for now, only support creation via ajax
        if request.is_ajax():
            note = Annotation.create_from_request(request)
            note.save()

            # create log entry for creation of the annotation
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(note).pk,
                object_id=note.pk,
                object_repr=str(note),
                change_message='Created via annotator API',
                action_flag=ADDITION)

            # annotator store documentation says to return 303
            # not sure why this isn't a 201 Created...
            return HttpResponseSeeOtherRedirect(note.get_absolute_url())

        else:
            return HttpResponseBadRequest(non_ajax_error_msg)


class AnnotationView(View):
    '''Views for displaying, updating, and removing a single
    :class:`~readux.annotations.models.Annotation`.  All views require
    that the user be logged in and own the annotation being viewed,
    updated, or deleted.'''

    # all single-annotation views currently require user to be logged in
    @method_decorator(login_required_with_ajax())
    def dispatch(self, *args, **kwargs):
        return super(AnnotationView, self).dispatch(*args, **kwargs)

    def get_object(self):
        note = get_object_or_404(Annotation, id=self.kwargs.get('id', None))
        # check permissions for view access
        # NOTE: assumes user must have view access in order to change/delete
        if not note.user_can_view(self.request.user):
            raise PermissionDenied()

        return note

    def get(self, request, id):
        '''Display the JSON information for the requested annotation.'''
        # NOTE: if id is not a valid uuid this results in a ValueError
        # instead of a 404; should be handled by uuid regex in url config
        return JsonResponse(self.get_object().info())

    def put(self, request, id):
        '''Update the annotation via JSON data posted by AJAX.'''
        if request.is_ajax():
            note = self.get_object()

            if not note.user_can_update(self.request.user):
                raise PermissionDenied()

            # NOTE: if user has update permission but not admin permission,
            # any changes to annotation permissions will be ignored
            note.update_from_request(request)

            # create log entry for modification of the annotation
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(note).pk,
                object_id=note.pk,
                object_repr=str(note),
                change_message='Updated via annotator API',
                action_flag=CHANGE)

            return HttpResponseSeeOtherRedirect(note.get_absolute_url())
        else:
            return HttpResponseBadRequest(non_ajax_error_msg)

    def delete(self, request, id):
        '''Remove the annotation.  On success, returns a 204 No Content
        response as per the annotator store API documentation.'''
        note = self.get_object()

        if not note.user_can_delete(self.request.user):
            raise PermissionDenied()

        # log that the annotation is being deleted
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(note).pk,
            object_id=note.pk,
            object_repr=str(note),
            change_message='Deleted via annotator API',
            action_flag=DELETION)
        # delete the note
        note.delete()

        response = HttpResponse('')
        # return 204 no content, according to annotator store api docs
        response.status_code = 204
        return response


class AnnotationSearch(View):
    '''Search annotations and display as JSON.  Results are restricted
    to annotations the users has permission to view (currently only
    annotations owned by the user for everyone other than superusers).

    The following search fields are currently supported:
       - uri (exact match)
       - text (case-insensitive partial match)
       - quote (case-insensitive partial match)
       - user (exact match on username)
       - keyword: case-insensitive partial match on text, quote, or
         with extra data (e.g., to match tags)

    Search results can be limited by specifying ``limit`` or ``offset``
    parameters.
    '''

    def get(self, request):
        # TODO: look at reference implementation to see what
        # other search fields should be supported

        # Only provide access to notes a user can view
        # (For non-superusers, this is only notes they own)
        notes = Annotation.objects.visible_to(request.user)

        search_keys = request.GET.keys()
        for field in search_keys:
            search_val = request.GET[field]
            if field == 'text':
                notes = notes.filter(text__icontains=search_val)
            elif field == 'quote':
                notes = notes.filter(quote__icontains=search_val)
            elif field == 'user':
                notes = notes.filter(user__username=search_val)
            elif field in Annotation.common_fields:
                notes = notes.filter(**{field: search_val})
            # special case: "keyword" search on multiple fields
            elif field == 'keyword':
                notes = notes.filter(
                    Q(text__icontains=search_val) |
                    Q(quote__icontains=search_val) |
                    Q(extra_data__icontains=search_val)
                )
                # NOTE: contains search on extra data jsonfield is
                # probably not a great idea...

        # for now, ignore date fields and extra data
        # NOTE: date searching would be nice, but probably requires
        # parsing dates and generating date ranges
        # tag searching may be important eventually too

        # minimal pagination: limit/offset
        limit = request.GET.get('limit', None)
        offset = request.GET.get('offset', None)
        # slice queryset by offset first, so limit will be relative to that
        try:
            if offset is not None:
                notes = notes[int(offset):]
            if limit is not None:
                notes = notes[:int(limit)]
        except ValueError:
            # if non-numeric values are passed, just ignore them
            pass

        return JsonResponse({
            'total': notes.count(),
            'rows': [n.info() for n in notes]
        })