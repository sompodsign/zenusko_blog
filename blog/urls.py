from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    # path('', views.PostListView.as_view(), name='post_list'),
    path('', views.post_list, name='post_list'),
    # path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         views.post_detail, name='post_detail'),
    # path('<int:post_id>/share/',
    #      views.post_share, name='post_share'),
    path('new_post/', views.post, name='post_article'),
    path('edit_post/<int:id>', views.edit_post, name='edit_post'),
    path('delete_post/<int:id>', views.delete_post, name='delete_post'),
    path('contact/', views.contact, name='contact'),
    path('my_posts/', views.author_posts, name='author_posts')

]
