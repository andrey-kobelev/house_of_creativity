from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, DeleteView
)
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.urls import reverse

from datetime import datetime


from .models import Post, User, Category, Comment
from .forms import PostModelForm, CommentModelForm, ProfileForm


# ONLY FOR POSTS

class BlogIndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10
    queryset = Post.objects.select_related('category', 'author').filter(
        pub_date__lte=datetime.now(),
        is_published=True,
        category__is_published=True
    )


class BlogPostCreateView(CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.author.username}
        )


class BlogPostUpdateView(UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class BlogPostDeleteView(DeleteView):
    form = None
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        self.form = PostModelForm(request.GET, instance=instance)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.author.username}
        )

# CBV FOR CATEGY BLOCK


class BlogCategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug']
        )
        posts = category.posts.filter(is_published=True)
        return posts


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    posts = category.posts.filter(is_published=True)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    temp_name = 'blog/category.html'

    context = {
        'page_obj': page_obj,
        'category': category
    }

    return render(request, temp_name, context)
# END CBV FOR CATEGY BLOCK


class BlogPostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all()
        context["form"] = CommentModelForm()
        return context


# ONLY FOR COMMENTS


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentModelForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('blog:post_detail', post_id)


def edit_comment(request, post_id, comment_id):
    temp_name = 'blog/comment.html'
    instance = get_object_or_404(Comment, pk=comment_id)
    form = CommentModelForm(request.POST or None, instance=instance)
    if request.POST:
        form = CommentModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)

    context = {
        'form': form,
        'comment': instance
    }

    return render(request, temp_name, context)


def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    temp_name = 'blog/comment.html'
    context = {
        'comment': comment
    }

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)

    return render(request, temp_name, context)

# ONLY FOR PROFILE


def profile(request, username):
    template_name = 'blog/profile.html'
    usr = User.objects.get(username=username)
    posts = usr.posts.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'profile': usr
    }

    return render(request, template_name, context)


def update_profile(request):
    template_name = 'blog/user.html'
    instance = get_object_or_404(User, pk=request.user.pk)
    form = ProfileForm(request.GET or None, instance=instance)

    if request.POST:
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', instance.username)

    context = {
        'form': form,
    }

    return render(request, template_name, context)
