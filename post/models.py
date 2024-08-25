from django.db import models
from django.utils.safestring import mark_safe
import re

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def render_content(self):
        """
        Processa o conteúdo do campo 'content' e substitui shortcodes por conteúdo dinâmico.
        """
        processed_content = self._process_shortcodes(self.content)
        return mark_safe(processed_content)

    def _process_shortcodes(self, content):
        """
        Procura por shortcodes no conteúdo e substitui-os pelo conteúdo correspondente.
        """
        pattern = r'\{\|\s*assunto:\s*([^|]+)\s*\|\s*modelo:\s*([^|]+)\s*\|\}'
        def replace_shortcode(match):
            assunto = match.group(1).strip()
            modelo = match.group(2).strip().lower()
            return self._generate_content(assunto, modelo)
        processed_content = re.sub(pattern, replace_shortcode, content)
        print(f'-----------Conteúdo processado: {processed_content}')  # Debugging
        return processed_content

    def _generate_content(self, assunto, modelo):
        """
        Gera o conteúdo baseado no assunto e no modelo fornecidos no shortcode.
        """
        print(f'Gerando conteúdo - Assunto: {assunto}, Modelo: {modelo}')  # Debugging

        if assunto.startswith('tag:'):
            tag_name = assunto[len('tag:'):].strip()
            posts = Post.objects.filter(tags__name__icontains=tag_name).distinct()
        else:
            posts = Post.objects.filter(title__icontains=assunto)

        if not posts.exists():
            return '<p>Nenhum post encontrado.</p>'
        
        if modelo == 'card':
            return self._render_card(posts)
        elif modelo == 'title':
            return self._render_title(posts)
        elif modelo == 'list':
            return self._render_list(posts)
        else:
            return '<p>Modelo desconhecido.</p>'
        
    def _render_card(self, posts):
        """
        Renderiza posts como um card com imagem, título e trecho.
        """
        return ''.join([
            f'''
            <div class="post-card">
                <img src="{post.image.url}" alt="{post.title}" class="post-image" style="max-width:100px; max-height:100px;"/>
                <h3>{post.title}</h3>
                <p>{post.content[:100]}...</p>
            </div>
            ''' if post.image else f'<h3>{post.title}</h3>'
            for post in posts
        ])

    def _render_title(self, posts):
        """
        Renderiza apenas o título dos posts.
        """
        return ''.join([f'<h3>{post.title}</h3>' for post in posts])

    def _render_list(self, posts):
        """
        Renderiza posts como uma lista ordenada com título e data.
        """
        return '<ol>' + ''.join([
            f'<li>{post.title} - {post.created_at.strftime("%d/%m/%Y")}</li>'
            for post in posts
        ]) + '</ol>'

    def __str__(self):
        return self.title
