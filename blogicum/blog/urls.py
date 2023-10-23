from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # BLOCK INDEX
    path('', views.BlogIndexListView.as_view(), name='index'),

    # BLOCK POSTS
    path(
        'posts/create/', views.BlogPostCreateView.as_view(), name='create_post'
    ),

    path(
        'posts/<int:post_id>/',
        views.post_detail, name='post_detail'
    ),

    path(
        'posts/<int:post_id>/edit/',
        views.edit_post, name='edit_post'
    ),

    path(
        'posts/<int:post_id>/delete/',
        views.BlogPostDeleteView.as_view(),
        name='delete_post'
    ),
    # BLOCK CATEGORY
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),

    # BLOCK COMMENTS
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),

    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'
    ),

    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
    ),

    # BLOCK PROFILE
    path(
        'profile/<slug:username>/', views.profile,
        name='profile'
    ),

    path(
        'profile/edit', views.update_profile,
        name='edit_profile'
    )
]
