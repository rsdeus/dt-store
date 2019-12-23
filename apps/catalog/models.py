from django.db import models

from django.urls import reverse

# Create your models here.


class Partner(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)

    email = models.EmailField('E-mail', unique=True)
    phone = models.CharField('Telefone', max_length=12, blank=True)
    site = models.CharField('Site', max_length=12, blank=True)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Parceiro'
        verbose_name_plural = 'Parceiros'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:partner', kwargs={'slug': self.slug})


class Category(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})


class Product(models.Model):

    name = models.CharField('Nome', max_length=100)
    slug = models.SlugField('Identificador', max_length=100)
    bar_code = models.CharField('Código de Barras', max_length=100, blank=True, null=True)
    category = models.ForeignKey('catalog.Category', verbose_name='Categoria', on_delete=models.SET_NULL, null=True, blank=True)

    short_description = models.TextField('Descrição Curta', max_length=255, blank=True)
    description = models.TextField('Descrição', blank=True)

    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    published = models.BooleanField('Publicado', default=True)

    stock = models.IntegerField('Quantidade em Estoque', default=0)

    partner = models.ForeignKey('catalog.Partner', verbose_name='Parceiro', on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField('Imagem', upload_to='products_imagens', blank=True, null=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug})
