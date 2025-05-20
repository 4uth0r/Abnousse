from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View

from .models import Category, Post, Like
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    paginate_by = 6
    context_object_name = 'posts'
    template_name = 'blog/post-list.html'

    def get_queryset(self):
        return Post.objects.filter(language=get_language(), publish='p')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['latest_posts'] = Post.objects.filter(language=get_language(), publish='p')[:4]
        return context


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post-detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['pk'], publish='p')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = kwargs.get('form') or CommentForm()
        context['comments'] = self.object.comments.filter(approved=True, parent__isnull=True).order_by('-created')

        post = self.object
        context['previous_post'] = Post.objects.filter(publish='p', language=post.language, id__lt=post.id).order_by('-id').first()
        context['next_post'] = Post.objects.filter(publish='p', language=post.language, id__gt=post.id).order_by('id').first()

        context['related_posts'] = Post.objects.filter(publish='p', language=post.language, category=post.category).exclude(id=post.id).order_by('-created')[:4]

        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.save()
            session_key = self.request.session.session_key

        context['session_key'] = session_key
        context['is_liked_by'] = self.object.is_liked_by(session_key)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if not request.user.is_authenticated:
            messages.error(request, _('برای ارسال دیدگاه باید وارد شوید.'))
            return redirect(
                f"{reverse_lazy('blog:post-detail', kwargs={'pk': self.object.pk})}"
            )

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, _('دیدگاه شما با موفقیت ارسال شد.'))
        else:
            messages.error(request, _('متن دیدگاه نمی‌تواند خالی باشد.'))

        return redirect(
            reverse_lazy('blog:post-detail', kwargs={'pk': self.object.pk})
        )


class ToggleLikeView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, language=get_language(), publish='p', pk=pk)
        session_key = request.session.session_key or request.session.save()

        like, created = Like.objects.get_or_create(post=post, session_key=session_key)

        if not created:
            like.delete()

        is_liked = post.is_liked_by(session_key)
        
        return render(
            request,
            'blog/partials/_like_button.html',
            {'post': post, 'is_liked_by': is_liked}
        )
