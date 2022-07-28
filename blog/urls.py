from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
        path('', posts_list, name='post_list'),
        path('tag/<slug:tag_slug>', posts_list, name='post_list_by_tag'),
        # path('', PostsList.as_view(), name='post_list'),
        path('p/<slug:slug>/<int:year>/<int:month>/<int:day>/', post_details, name='post_details'),
        path('p/share/<int:post_id>/', share_post, name='share_post'),
]
