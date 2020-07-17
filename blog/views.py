from django.shortcuts import render
from django.dispatch import receiver 
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.utils.text import slugify

from django.db.models.signals import post_save

from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class BlogListView(ListView):
    model = Post
    template_name = 'blog/home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    # Para renomear o object
    # context_object_name = 'custom'

class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_new.html'
    success_url = reverse_lazy('blog:home')
    success_message = "Postagem criada com sucesso"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.autor = self.request.user
        obj.save()
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    success_message = "%(field)s - alterado com sucesso"
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.autor = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            field=self.object.titulo,
        )


class BlogDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_message = "Deletado com sucesso"
    success_url = reverse_lazy('blog:home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request,self.success_message)
        return super(BlogDeleteView,self).delete(request, *args, **kwargs)


@receiver(post_save, sender=Post)
def insert_slug(sender, instance, **kwargs):
    if kwargs.get('created', False):
        print('Criando slug')
        
    if not instance.slug:
        instance.slug = slugify(instance.titulo)
        return instance.save()
