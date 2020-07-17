from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='publicado')

class Category(models.Model):
    nome = models.CharField(max_length=100)
    publicado = models.DateTimeField(default = timezone.now)
    criado = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Post(models.Model):
    STATUS = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )

    titulo = models.CharField(verbose_name ='Titulo', max_length=250)
    slug = models.SlugField(max_length=250)
    autor = models.ForeignKey(User, 
                            on_delete = models.CASCADE)
    categoria = models.ManyToManyField(Category, related_name='get_posts')
    imagem = models.ImageField(upload_to='blog', null=True, blank=True)
    conteudo = RichTextField(verbose_name='Conteudo')
    publicado = models.DateTimeField(default = timezone.now)
    criado = models.DateTimeField(auto_now_add = True)
    alterado = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10, choices = STATUS, default='rascunho')

    # Caso eu chamar objects ele mostra apenas os publicados
    # Assim eu deixo o published EM BAIXO para que no admin mostre todos
    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return f'post/{self.slug}'

    def get_absolute_url_update(self):
        return f'edit/'

    @property
    def view_image(self):
        return mark_safe('<img src="%s" width="400px" />'%self.imagem.url)   
        view_image.short_description = "Imagem Cadastrada" 
        view_image.allow_tags = True    

    class Meta:
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'
        ordering = ['publicado']

    def __str__(self):
        return self.titulo

    
    


    

    

