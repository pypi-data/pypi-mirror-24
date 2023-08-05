from collections import OrderedDict
import json
import logging
import uuid
from django.apps import apps
from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
from jsonfield import JSONField
try:
    import guardian
    from guardian.shortcuts import assign_perm, get_objects_for_user, \
        get_objects_for_group, get_perms_for_model, get_perms
    from guardian.models import UserObjectPermission, GroupObjectPermission
except ImportError:
    guardian = None
import six


logger = logging.getLogger(__name__)


ANNOTATION_MODEL_NAME = getattr(settings, 'ANNOTATOR_ANNOTATION_MODEL',
    "annotator_store.Annotation")

ANNOTATION_OBJECT_PERMISSIONS = getattr(settings, 'ANNOTATION_OBJECT_PERMISSIONS',
    False)


class AnnotationQuerySet(models.QuerySet):
    'Custom :class:`~django.models.QuerySet` for :class:`Annotation`'

    def visible_to(self, user):
        """
        Return annotations the specified user is allowed to view.
        Objects are found based on view_annotation permission and

        annotations; users can access only their own annotations or
        those where permissions have been granted to a group they belong to.

        .. Note::
            Due to the use of :meth:`guardian.shortcuts.get_objects_for_user`,
            it is recommended to use this method first; it
            does combine the existing queryset query, but it does not
            chain as querysets normally do.

        """

        # if per-object permissions are enabled, use guardian to find
        # annotations the current user can view
        if ANNOTATION_OBJECT_PERMISSIONS:
            qs = get_objects_for_user(user, 'view_annotation',
                                      get_annotation_model())
            # combine the current queryset query, if any, with the newly
            # created queryset from django guardian
            qs.query.combine(self.query, 'AND')
            return qs

        else:
            # otherwise, return everything or nothing based on django perms
            if user.has_perm('annotator_store.view_annotation'):
                return self.filter()
            else:
                # empty queryset if user doesn't have view permission
                return self.none()

    def visible_to_group(self, group):
        """
        Return annotations the specified group is allowed to view.
        Objects are found based on view_annotation permission and
        per-object permissions.

        .. Note::
            Due to the use of :meth:`guardian.shortcuts.get_objects_for_user`,
            it is recommended to use this method first; it does combine
            the existing queryset query, but it does not chain as querysets
            normally do.

        """

        # group permissions are only enabled when per-object permissions
        # are turned on
        if ANNOTATION_OBJECT_PERMISSIONS:
            qs = get_objects_for_group(group, 'view_annotation',
                                       get_annotation_model())
            # combine current queryset query, if any, with the newly
            # created queryset from django guardian
            qs.query.combine(self.query, 'AND')
            return qs

        else:
            return self.filter()

    def last_created_time(self):
        '''Creation time of the most recently created annotation. If
        queryset is empty, returns None.'''
        try:
            return self.values_list('created', flat=True).latest('created')
        except ObjectDoesNotExist:
            pass

    def last_updated_time(self):
        '''Update time of the most recently created annotation. If
        queryset is empty, returns None.'''
        try:
            return self.values_list('updated', flat=True).latest('updated')
        except ObjectDoesNotExist:
            pass


class AnnotationManager(models.Manager):
    '''Custom :class:`~django.models.Manager` for :class:`Annotation`.
    Returns :class:`AnnotationQuerySet` as default queryset, and exposes
    :meth:`visible_to` for convenience.'''

    def get_queryset(self):
        return AnnotationQuerySet(self.model, using=self._db)

    def visible_to(self, user):
        'Convenience access to :meth:`AnnotationQuerySet.visible_to`'
        return self.get_queryset().visible_to(user)

    def visible_to_group(self, group):
        'Convenience access to :meth:`AnnotationQuerySet.visible_to_group`'
        return self.get_queryset().visible_to_group(group)


@six.python_2_unicode_compatible
class BaseAnnotation(models.Model):
    '''Django database model to store Annotator.js annotation data,
    based on the
    `annotation format documentation <http://docs.annotatorjs.org/en/v1.2.x/annotation-format.html>`_.'''

    #: regex for recognizing valid UUID, for use in site urls
    UUID_REGEX = r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

    #: annotation schema version: default v1.0
    schema_version = "v1.0"
    # for now, hard-coding until or unless we need to support more than
    # one version of annotation

    #: unique id for the annotation; uses :meth:`uuid.uuid4`
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # data model includes version, do we need to set that in the db?
    # "annotator_schema_version": "v1.0",        # schema version: default v1.0

    #: datetime annotation was created; automatically set when added
    created = models.DateTimeField(auto_now_add=True)
    #: datetime annotation was last updated; automatically updated on save
    updated = models.DateTimeField(auto_now=True)
    #: content of the annotation
    text = models.TextField(blank=True)
    #: the annotated text
    quote = models.TextField(blank=True)
    #: URI of the annotated document
    uri = models.URLField()
    #: user who owns the annotation
    #: when serialized, id of annotation owner OR an object with an 'id' property
    # Make user optional for now
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    # tags still todo
    # "tags": [ "review", "error" ],             # list of tags (from Tags plugin)

    #: any additional data included in the annotation not parsed into
    #: specific model fields; this includes ranges, permissions,
    #: annotation data, etc
    extra_data = JSONField(default=json.dumps({}))
    # example range from the documentation
    # "ranges": [
    #     {
    #        "start": "/p[69]/span/span",           # (relative) XPath to start element
    #        "end": "/p[70]/span/span",             # (relative) XPath to end element
    #        "startOffset": 0,                      # character offset within start element
    #        "endOffset": 120                       # character offset within end element
    #    }
    # ]

    # NOTE: according to the documentation, the basic schema is
    # extensible, can be added to by plugins, and any fields added by the
    # frontend should be preserved by the backend.  Store any of that
    # additional information in the extra_data field.

    #: fields in the db model that are provided by annotation json
    #: when creating or updating an annotation
    common_fields = ['text', 'quote', 'uri', 'user']
    #: internal fields that are not set from values provided by
    #: annotation json when creating or updating
    internal_fields = ['updated', 'created', 'id', 'user',
        'annotator_schema_version']

    objects = AnnotationManager()

    class Meta:
        abstract = True
        # extend default permissions to add a view option
        # change_annotation and delete_annotation provided by django
        permissions = (
            ('view_annotation', 'View annotation'),
            ('admin_annotation', 'Manage annotation'),
        )

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Annotation: %s>' % self.text

    def get_absolute_url(self):
        'URL to view this annotation within the annotation API.'
        return reverse('annotation-api:view', kwargs={'id': self.id})

    def text_preview(self):
        'Short preview of annotation text content'
        if self.text:
            return self.text[:100] + ('...' if len(self.text) > 100 else '')
        # provide indicator for annotations with no text
        return '[no text]'
    text_preview.short_description = 'Text'

    def uri_link(self):
        'URI as a clickable link'
        return format_html('<a href="{}">{}</a>', self.uri, self.uri)
    uri_link.short_description = 'URI'

    @property
    def related_pages(self):
        'convenience access to list of related pages in extra data'
        if 'related_pages' in self.extra_data:
            return self.extra_data['related_pages']

    @classmethod
    def filter_data(cls, data, internal_only=False):
        if internal_only:
            filter_fields = cls.internal_fields
        else:
            filter_fields = cls.common_fields + cls.internal_fields
        return {key: val for key, val in data.items()
               if key not in filter_fields}

    @classmethod
    def create_from_request(cls, request):
        '''Initialize a new :class:`Annotation` based on data from a
        :class:`django.http.HttpRequest`.

        Expects request body content to be JSON; sets annotation user
        based on the request user.
        '''

        data = json.loads(request.body.decode())

        model_data = {}
        extra_data = {}
        for key, val in six.iteritems(data):
            if key in BaseAnnotation.common_fields:
                model_data[key] = val
            else:
                extra_data[key] = val

        if not request.user.is_anonymous():
            model_data['user'] = request.user

        # remove any common and internal fields from extra data so they
        # don't get duplicated in the json field
        extra_data = cls.filter_data(extra_data)

        annotation = cls(extra_data=json.dumps(extra_data), **model_data)
        # if extra data is present, handle any extra processing
        # exactly the same as when updating an annotation
        if annotation.extra_data:
            annotation.extra_data = annotation.handle_extra_data(extra_data, request)
            annotation.save()

        return annotation

    def update_from_request(self, request):
        '''Update attributes from data in a
        :class:`django.http.HttpRequest`. Expects request body content to be
        JSON.   Currently does *not* modify user.'''
        data = json.loads(request.body.decode())
        # NOTE: could keep a list of modified fields and
        # and allow Django to do a more efficient db update

        # ignore backend-generated fields and remove so they are
        # not duplicated in extra data
        # NOTE: current implementation assumes that user should
        # NOT be changed after annotation is created
        data = self.filter_data(data, internal_only=True)

        # set database fields from data in the request
        for field in self.common_fields:
            try:
                setattr(self, field, data[field])
                # remove from data so it is not duplicated
                del data[field]
            except KeyError:
                pass

        if data:
            # any other data included in the request and not yet
            # processed should be stored as extra data.
            # Allow subclasses to process any extra data they care about
            # and then store whatever is left.
            # NOTE: replacing existing extra data rather than updating;
            # any extra data should have been included in the annotation
            # that was loaded for editing; using update would make it
            # impossible to delete extra data fields.
            self.extra_data = self.handle_extra_data(data, request)

        self.save()

    def handle_extra_data(self, data, request):
        '''Handle any "extra" data that is not part of the stock annotation
        data model.  Use this method to customize the logic for creating
        and updating annotations from request data.

        NOTE: request is passed in to support permissions handling
        when object-level permissions are enabled.
        '''
        return data

    def info(self):
        '''Return a :class:`collections.OrderedDict` of fields to be
        included in serialized JSON version of the current annotation.'''
        info = OrderedDict([
            ('id', str(self.id)),
            ('annotator_schema_version', self.schema_version),
            # iso8601 formatted dates
            ('created', self.created.isoformat() if self.created else ''),
            ('updated', self.updated.isoformat() if self.updated else ''),
            ('text', self.text),
            ('quote', self.quote),
            ('uri', self.uri),
            ('user', self.user.username if self.user else ''),
            # tags handled as part of extra data
        ])
        # There shouldn't be collisions between extra data and db
        # fields, but in case there are, none of the extra data shoudl
        # override core fields
        info.update({k: v for k, v in six.iteritems(self.extra_data)
                     if k not in info})

        return info

    # generic django permission checks; methods are provided for consistency
    # with optional per-object permissions

    def user_can_view(self, user):
        return user.has_perm('annotator_store.view_annotation')

    def user_can_update(self, user):
        return user.has_perm('annotator_store.change_annotation')

    def user_can_delete(self, user):
        return user.has_perm('annotator_store.delete_annotation')


# if per-object permissions are requested and guardian is installed
# define annotation permission functionality

if ANNOTATION_OBJECT_PERMISSIONS and guardian:

    class AnnotationWithPermissions(BaseAnnotation):
        '''Mix-in annotation class to provide object-level permissions
        handling via django-guardian'''

        class Meta:
            abstract = True
            permissions = (
                ('view_annotation', 'View annotation'),
                ('admin_annotation', 'Manage annotation'),
            )

        # example permissions from the documentation
        # "permissions": {
        #     "read": ["group:__world__"],
        #     "admin": [],
        #     "update": [],
        #     "delete": []
        # }

        #: map annotator permissions to django annotation permission codenames
        permission_to_codename = {
            'read': 'view_annotation',
            'update': 'change_annotation',
            'delete': 'delete_annotation',
            'admin': 'admin_annotation'
        }
        #: lookup annotation permission mode by django permission codename
        codename_to_permission = dict([(codename, mode) for mode, codename
                                       in six.iteritems(permission_to_codename)])

        def info(self):
            '''Update default annotation info to include permissions'''
            info = super(AnnotationWithPermissions, self).info()
            # annotation permissions dict based on database permissions
            permissions = self.permissions_dict()
            # only include if at least one permission is not empty
            if any(permissions.values()):
                info['permissions'] = permissions
            return info

        def save(self, *args, **kwargs):
            """Extend default save method to ensure annotation user has
            access to edit and update their own annotation."""
            super(AnnotationWithPermissions, self).save(*args, **kwargs)
            # NOTE: currently annotation model assumes user is not modified;
            # if it is changed, previous owner will still have permissions
            self.grant_user_access()

        def handle_extra_data(self, data, request):
            '''Handle any "extra" data that is not part of the stock annotation
            data model.  Use this method to customize the logic for updating
            an annotation from request data.'''
            data = super(AnnotationWithPermissions, self).handle_extra_data(data, request)
            if 'permissions' in data:
                # only change permissions if user has admin annotation
                # permission; otherwise, ignore any changes
                if self.user_has_perm(request.user, 'admin_annotation'):
                    logger.debug('user has admin perms, updating db permissions')
                    self.db_permissions(data['permissions'])
                else:
                    logger.debug('user does not have admin perms, ignoring permissions')

                # remove permissions from extra data so it does not
                # get stored in the catch-all json field
                del data['permissions']

            return data

        def user_permissions(self):
            '''Queryset of :class:`guardian.model.UserObjectPermission`
            objects associated with this annotation.'''
            return UserObjectPermission.objects.filter(object_pk=self.pk)

        def group_permissions(self):
            '''Queryset of :class:`guardian.model.GroupObjectPermission`
            objects associated with this annotation.'''
            return GroupObjectPermission.objects.filter(object_pk=self.pk)

        def get_group_or_user(self, ident):
            # look up annotation group or user based on username
            # or group id in annotation permissions list
            if ident.startswith('group:'):
                group_id = ident[len('group:'):]
                try:
                    return AnnotationGroup.objects.get(id=int(group_id))
                except ValueError:
                    # non-integer identifier found
                    logger.warn("Invalid group id '%s' in annotation %s permissions",
                                group_id, self.pk)
                except AnnotationGroup.DoesNotExist:
                    logger.warn("Error finding group '%s' in annotation %s permissions",
                                group_id, self.pk)
            else:
                try:
                    return User.objects.get(username=ident)
                except User.DoesNotExist:
                    logger.warn("Error finding user '%s' in annotation %s permissions",
                                ident, self.pk)

        def assign_permission(self, permission, entity):
            """Wrapper around :meth:`guardian.shortcuts.assign_perm`.
            Gives the specified permission to the specified user or group
            on the current object.
            """
            assign_perm(permission, entity, self)

        def db_permissions(self, permissions):
            '''Convert annotation permission data into actionable
            django permissions using :mod:`guardian` per-object permissions.
            '''
            # since there is no way to know what permissions were
            # previously in place and need to be removed, remove all permissions
            self.user_permissions().delete()
            self.group_permissions().delete()

            # NOTE: should eventually handle special case
            # group:__world__, but setting that is currently not supported
            # by the readux annotator permissions module

            # then re-assign permissions based on annotation permissions
            for mode, users in six.iteritems(permissions):
                for ident in users:
                    entity = self.get_group_or_user(ident)
                    if entity is not None:
                        # give user/group the appropriate permission on this object
                        self.assign_permission(self.permission_to_codename[mode],
                                               entity)

        def grant_user_access(self):
            if self.user is not None:   # possibly also check anonymous?
                for perm in get_perms_for_model(self):
                    # skip default django add permission - not relevant
                    # on an individual object
                    if perm.codename == 'add_annotation':
                        continue
                    self.assign_permission(perm.codename, self.user)

        def permissions_dict(self):
            '''Convert stored :mod:`guardian` per-object permissions into
            annotation permission dictionary format'''
            # convert db permissions into annotator style permissions

            # construct base permissions dict, empty list for each mode
            permissions = dict([(mode, [])
                               for mode in self.permission_to_codename.keys()])

            for user_perm in self.user_permissions():
                # convert db codename to annotation mode
                mode = self.codename_to_permission[user_perm.permission.codename]
                # store by username
                permissions[mode].append(user_perm.user.username)

            for group_perm in self.group_permissions():
                mode = self.codename_to_permission[group_perm.permission.codename]
                permissions[mode].append(group_perm.group.annotationgroup.annotation_id)

            return permissions

        def user_has_perm(self, user, permission):
            'Check if a user has a specific permission on this object.'
            # NOTE: according to guardian docs, it should work to use this
            # user.has_perm(permission, self)
            # but that check fails when it should not.
            return permission in get_perms(user, self)

        def user_can_view(self, user):
            return self.user_has_perm(user, 'view_annotation')

        def user_can_update(self, user):
            return self.user_has_perm(user, 'change_annotation')

        def user_can_delete(self, user):
            return self.user_has_perm(user, 'delete_annotation')


    class AnnotationGroup(Group):
        """Annotation Group; extends :class:`django.contrib.auth.models.Group`.

        Intended to facilitate group permissions on annotations.
        """
        # inherits name from Group
        #: optional notes field
        notes = models.TextField(blank=True)
        #: datetime annotation was created; automatically set when added
        created = models.DateTimeField(auto_now_add=True)
        #: datetime annotation was last updated; automatically updated on save
        updated = models.DateTimeField(auto_now=True)

        def num_members(self):
            return self.user_set.count()
        num_members.short_description = '# members'

        def __repr__(self):
            return '<Annotation Group: %s>' % self.name

        @property
        def annotation_id(self):
            return 'group:%d' % self.pk


# if default annotation model is requested, define it here
# otherwise, custom annotation model will be used
if ANNOTATION_MODEL_NAME == "annotator_store.Annotation":

    if ANNOTATION_OBJECT_PERMISSIONS and guardian:

        class Annotation(AnnotationWithPermissions):
                pass

    else:
        class Annotation(BaseAnnotation):
            pass


def get_annotation_model():
    app_name, model_name = ANNOTATION_MODEL_NAME.split(".")
    app = apps.get_app_config(app_name)
    return app.get_model(model_name)


