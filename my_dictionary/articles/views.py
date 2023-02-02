from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Article, Comment
from .forms import CommentForm
from django.views.generic.edit import FormMixin
from loguru import logger


class Articles(ListView):
    model = Article
    template_name = 'articles/articles.html'
    context_object_name = 'articles' 
    paginate_by = 10

    @logger.catch
    def get_queryset(self):
        return self.model.objects.filter(is_published=True, is_main_page=False)


class ShowArticle(FormMixin, DetailView):

    template_name = 'articles/conrete_article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'
    form_class = CommentForm

    def get_object(self, queryset=None):
        article_slug = self.kwargs.get('article_slug', None)
        if article_slug is None:
            return get_object_or_404(Article, is_main_page=True, is_published=True)
        else:
            return get_object_or_404(Article, slug=self.kwargs.get('article_slug'),
                                        is_published=True)

    def get_initial(self):
        if self.request.user.is_authenticated:
            first_name = self.request.user.first_name
            last_name = self.request.user.last_name
            full_name = []
            if first_name:
                full_name.append(first_name)
            if last_name:
                full_name.append(last_name)    
            full_name = ' '.join(full_name)
            if not full_name:
                full_name = self.request.user.username

            email = self.request.user.email
            #user_id = self.request.user.id
            return {
                'name':full_name,
                'email':email
            }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comments'] = Comment.objects.filter(active=True, article=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return HttpResponseRedirect(self.object.get_absolute_url())
