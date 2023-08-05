from django.conf.urls import url

from annotator_store import views
from .models import BaseAnnotation

app_name = 'annotator_store'

# api urls only for now
urlpatterns = [
    url(r'^$', views.AnnotationIndex.as_view(), name='index'),
    # urls are without trailing slashes per annotatorjs api documentation
    url(r'^search$', views.AnnotationSearch.as_view(), name='search'),
    url(r'^annotations$', views.Annotations.as_view(), name='annotations'),
    url(r'^annotations/(?P<id>%s)$' % BaseAnnotation.UUID_REGEX,
        views.AnnotationView.as_view(), name='view'),
]
