from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Class Base Views:::

class PostListView(ListView):
    model = Post
    template_name = 'blog_app/home.html'
    # usually the generic templates are searched as :: <app-name>/<model-name>_<viewtype>.html
    # Here it looked for blog_app/post_list.html
    context_object_name = 'posts' # default it is called object_list
    ordering = ['-date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # Template name post_form.html

# Overrideing the method to assign the post author before the createion of teh form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title', 'content']
    # Template name post_form.html

# Overrideing the method to assign the post author before the createion of teh form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):    # Just Like this authentication of the User 
                            # we can pass many test conditions to our different views 
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):     
        post = self.get_object()
        if self.request.user== post.author:
            return True
        return False

class UserPostListView(ListView):
    model = Post
    template_name = 'blog_app/user_posts.html'
    context_object_name = 'posts' # default it is called object_list
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

# Fuction Based Views
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog_app/home.html', context)


def about(request):
    return render(request, 'blog_app/about.html',{'title':'About'})

    