from django.views.generic import UpdateView, CreateView, ListView, DeleteView
from .forms import TextBookForm, ExerciseForm
from .models import TextBook, Exercise
from datetime import date
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from loguru import logger
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
import pypdfium2 as pdfium
from django.core.files.base import ContentFile
from io import BytesIO
from pathlib import Path


class ShowTextBook(LoginRequiredMixin, ListView):
    template_name = 'text_books/show_text_book.html'
    model = Exercise
    context_object_name = 'exercises'
    paginate_by = 5

    def get_queryset(self):
        text_book_id = self.kwargs.get('text_book_id')
        return self.model.objects.filter(text_book_id=text_book_id, text_book__owner_id=self.request.user.pk)

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        text_book_id = self.kwargs.get('text_book_id')
        text_book = TextBook.objects.filter(pk=text_book_id, owner_id=self.request.user.pk).first()
        context['text_book'] = text_book
        if not text_book.keys_file == "":
            context['keys_book_url'] = text_book.keys_file.url
        return context


class TextBooksList(LoginRequiredMixin, ListView):
    template_name = 'text_books/text_books_list.html'
    model = TextBook
    context_object_name = 'text_books'
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(owner_id=self.request.user.pk)


class AddTextBook(LoginRequiredMixin, CreateView):
    template_name = 'text_books/text_book_form.html'
    form_class = TextBookForm
    success_url = reverse_lazy('my_text_books')

    #@logger.catch
    def form_valid(self, form):
        text_book = form.save(commit=False)
        text_book.owner_id = self.request.user.pk
        # getting preview
        pdf = pdfium.PdfDocument(self.request.FILES['book_file'].file)
        page = pdf.get_page(0)
        preview_image = page.render(
            scale=1,
            rotation=0,
        )
        preview_image = preview_image.to_pil()
        preview_image.thumbnail((200, 200))

        image_io = BytesIO()
        preview_image.save(image_io, format='JPEG')
        image_data = image_io.getvalue()
        content_file = ContentFile(image_data)
        text_book.preview_image.save(f'text_book_preview_image{Path(text_book.book_file.name).stem}_preview.jpg',
                                     content_file,
                                     save=False)
        text_book.save()
        return HttpResponseRedirect(self.success_url)


class EditTextBook(LoginRequiredMixin, UpdateView):
    template_name = 'text_books/text_book_form.html'
    form_class = TextBookForm
    pk_url_kwarg = 'text_book_id'

    def get_queryset(self):
        return TextBook.objects.filter(owner_id=self.request.user.pk)


class DeleteTextBook(LoginRequiredMixin, DeleteView):
    template_name = 'text_books/confirm_deleting.html'
    success_url = reverse_lazy('my_text_books')
    pk_url_kwarg = 'text_book_id'

    def get_queryset(self):
        return TextBook.objects.filter(owner_id=self.request.user.pk)


class AddExercise(LoginRequiredMixin, CreateView):
    template_name = 'text_books/show_text_book.html'
    form_class = ExerciseForm
    success_url = reverse_lazy('my_text_books')
    initial = {'date': date.today()}

    @transaction.atomic
    def form_valid(self, form):
        exercise = form.save(commit=False)
        exercise.text_book_id = self.kwargs.get('text_book_id')
        exercise.save()
        text_book = TextBook.objects.get(pk=exercise.text_book.id, owner_id=self.request.user.pk)
        text_book.current_page_number = exercise.page_number
        text_book.keys_page_number = exercise.keys_page_number
        text_book.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        text_book_id = self.kwargs.get('text_book_id')
        return reverse('show_text_book', kwargs={'text_book_id': text_book_id})

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        text_book_id = self.kwargs.get('text_book_id')
        text_book = TextBook.objects.get(pk=text_book_id, owner_id=self.request.user.pk)
        context['text_book'] = text_book
        if not text_book.keys_file == "":
            context['keys_book_url'] = text_book.keys_file.url
        return context


class UpdateExercise(LoginRequiredMixin, UpdateView):
    template_name = 'text_books/show_text_book.html'
    form_class = ExerciseForm
    pk_url_kwarg = 'exercise_id'

    def get_queryset(self):
        return Exercise.objects.filter(text_book__owner_id=self.request.user.pk)

    @logger.catch
    def form_valid(self, form):
        exercise = form.save()
        text_book = TextBook.objects.get(pk=exercise.text_book.id, owner_id=self.request.user.pk)
        text_book.current_page_number = exercise.page_number
        text_book.keys_page_number = exercise.keys_page_number
        text_book.save()
        return HttpResponseRedirect(self.get_success_url(text_book.id))

    def get_success_url(self, text_book_id):
        return reverse('show_text_book', kwargs={'text_book_id': text_book_id})

    @logger.catch
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        text_book = self.object.text_book
        text_book.current_page_number = self.object.page_number
        text_book.keys_page_number = self.object.keys_page_number
        context['text_book'] = text_book
        if not text_book.keys_file == "":
            context['keys_book_url'] = text_book.keys_file.url
        return context


class DeleteExercise(LoginRequiredMixin, DeleteView):
    template_name = 'text_books/confirm_deleting.html'
    success_url = reverse_lazy('my_text_books')
    pk_url_kwarg = 'exercise_id'

    def get_queryset(self):
        return Exercise.objects.filter(text_book__owner_id=self.request.user.pk)
