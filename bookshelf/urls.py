from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.TitleList.as_view(), name="index"),
    url(r'^document/add/$', views.DocumentCreate.as_view(), name="document-add"),
    url(r'^merge/', views.merge_titles, name="merge-titles"),
]
