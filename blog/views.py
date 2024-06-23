from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from blog.forms import PostForm
from blog.models import Post


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        post = form.save()
        user = self.request.user
        post.owner = user
        post.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    # success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        if form.is_valid():
            edit_post = form.save()
            edit_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs.get('pk')])

    # def get_form_class(self):
    #     user = self.request.user
    #     if user == self.object.owner:
    #         return PostForm
    #     raise PermissionDenied


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        blog = Post.objects.all()
        context['blog'] = blog
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object()
        self.object.number_views += 1
        self.object.save()
        return self.object


def toggle_activity(request, pk):
    post_publish = get_object_or_404(Post, pk=pk)
    if post_publish.is_published:
        post_publish.is_published = False
    else:
        post_publish.is_published = True
    post_publish.save()
    return redirect(reverse('blog:post_list'))
