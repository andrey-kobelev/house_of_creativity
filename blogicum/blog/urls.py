from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # BLOCK FOR POSTS
    path('', views.BlogIndexListView.as_view(), name='index'),

    path(
        'posts/create/', views.BlogPostCreateView.as_view(), name='create_post'
    ),

    path(
        'posts/<int:post_id>/edit/',
        views.BlogPostUpdateView.as_view(), name='edit_post'
    ),

    path(
        'posts/<int:post_id>/delete/',
        views.BlogPostDeleteView.as_view(),
        name='delete_post'
    ),

    path(
        'posts/<int:post_id>/detail/',
        views.BlogPostDetailView.as_view(), name='post_detail'
    ),

    path(
        'posts/<slug:category_slug>/category/',
        views.get_category_list,
        name='category_posts'
    ),

    # BLOCK FOR COMMENTS
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

    # BLOCK FOR PROFILE
    path(
        'profile/<slug:username>/', views.profile,
        name='profile'
    ),

    path(
        'profile/edit', views.update_profile,
        name='edit_profile'
    )
]
