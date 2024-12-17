from datetime import datetime

from django.conf import settings
from django.views.generic import (
    ListView, CreateView, DeleteView)
from django.shortcuts import (
    get_object_or_404, render,
    redirect, Http404)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .utils import get_page_obj
from .models import Post, User, Category, Comment
from .forms import (
    PostModelForm, CommentModelForm, ProfileForm, CreationForm
)


# BLOCK INDEX
class BlogIndexListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        posts = self.model.objects.all().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now()
        )
        return posts


# BLOCK POSTS
class BlogPostCreateView(LoginRequiredMixin, CreateView):
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


def edit_post(request, post_id):
    temp_name = 'blog/create.html'
    instance = get_object_or_404(
        Post, pk=post_id
    )

    if instance.author == request.user and request.user.is_authenticated:

        form = PostModelForm(request.POST or None, instance=instance)

        context = {
            'form': form
        }

        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)

        return render(request, temp_name, context)
    return redirect('blog:post_detail', post_id)


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    form = None
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author == request.user or request.user.is_superuser:
            self.form = PostModelForm(request.GET, instance=instance)
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail', kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.object.author.username}
        )


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, pk=post_id)
    if not post.is_published:
        if ((post.author != request.user)
                or (not request.user.is_authenticated)):
            raise Http404()

    comments = post.comments.all().order_by('created_at')
    comment_form = CommentModelForm()

    context = {
        'post': post,
        'comments': comments,
        'form': comment_form
    }

    return render(request, template_name, context)


# CATEGORY BLOCK
def category_posts(request, category_slug):
    temp_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )

    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=datetime.now()
    )

    context = {
        'category': category,
        'page_obj': get_page_obj(posts, request)
    }

    return render(request, temp_name, context)


# BLOCK COMMENTS
@login_required
def add_comment(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

        return redirect('blog:post_detail', post_id)
    raise Http404()


@login_required
def edit_comment(request, post_id, comment_id):
    temp_name = 'blog/comment.html'
    instance = get_object_or_404(Comment, pk=comment_id)
    if instance.author == request.user or request.user.is_superuser:
        form = CommentModelForm(request.POST or None, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id)

        context = {
            'form': form,
            'comment': instance
        }

        return render(request, temp_name, context)

    return redirect('blog:post_detail', post_id)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    temp_name = 'blog/comment.html'
    if comment.author == request.user or request.user.is_superuser:
        context = {
            'comment': comment
        }

        if request.method == 'POST':
            comment.delete()
            return redirect('blog:post_detail', post_id)

        return render(request, temp_name, context)
    return redirect('blog:post_detail', post_id)


# BLOCK PROFILE
def profile(request, username):
    template_name = 'blog/profile.html'
    usr = get_object_or_404(User, username=username)
    posts = usr.posts.all()

    if request.user != usr:
        posts = usr.posts.filter(is_published=True)

    context = {
        'page_obj': get_page_obj(posts, request),
        'profile': usr
    }

    return render(request, template_name, context)


@login_required
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


# REGISTRATION USER BLOCK
class CreationUserView(CreateView):
    model = User
    form_class = CreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')
