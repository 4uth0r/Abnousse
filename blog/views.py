from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages

from .models import Category, Post
from .forms import CommentForm


def comment_chunk(request, pk):
    post = get_object_or_404(Post, pk=pk, publish='p')
    page = int(request.GET.get('page', 1))
    paginator = Paginator(
        post.comments.filter(approved=True, parent__isnull=True).order_by('-created'),
        5
    )
    comments_page = paginator.get_page(page)
    html = render_to_string(
        'blog/_comments_chunk.html',
        {'comments_page': comments_page}
    )
    return HttpResponse(html)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post-list.html'

    def get_queryset(self):
        return Post.objects.filter(language=get_language(), publish='p')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
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
