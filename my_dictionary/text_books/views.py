from datetime import date
from io import BytesIO
from pathlib import Path

import fitz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.http import Http404, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from PIL import Image
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from text_books.forms import TextBookForm
from text_books.models import Exercise, TextBook
from text_books.pagination import ExerciseAPIListPagination
from text_books.serializers import ExerciseSerializer, TextBookSerializer


class TextBookManager(LoginRequiredMixin, TemplateView):
    template_name = "text_books/text_book_manager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        text_book_id = self.kwargs.get("text_book_id")
        context["constants"] = {
            "text_book_id": text_book_id,
            "API_URL": reverse("api-root"),
            "edit_text_book_url": reverse("edit_text_book", kwargs={'text_book_id': text_book_id}),
            "csrfToken": get_token(self.request),
        }
        return context


class TextBooksList(LoginRequiredMixin, ListView):
    template_name = "text_books/text_books_list.html"
    model = TextBook
    context_object_name = "text_books"
    paginate_by = 10

    def get_queryset(self):
        # TODO show only this language textbooks
        return self.model.objects.filter(owner_id=self.request.user.pk)


class AddTextBook(LoginRequiredMixin, CreateView):
    template_name = "text_books/text_book_form.html"
    form_class = TextBookForm
    success_url = reverse_lazy("my_text_books")

    def form_valid(self, form):
        try:
            text_book = form.save(commit=False)
            text_book.owner_id = self.request.user.pk
            file = self.request.FILES["book_file"].file
            pdf_file = fitz.open(stream=file.read())
            page = pdf_file.load_page(0)
            pix = page.get_pixmap()
            preview_image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            preview_image.thumbnail((200, 200))
            image_io = BytesIO()
            preview_image.save(image_io, format="JPEG")
            image_data = image_io.getvalue()
            content_file = ContentFile(image_data)
            text_book.preview_image.save(
                f"text_book_preview_image{Path(text_book.book_file.name).stem}_preview.jpg",
                content_file,
                save=False,
            )

            text_book.save()
            return HttpResponseRedirect(self.success_url)
        except:
            form.add_error(
                "book_file",
                "Некоректное имя или формат файла. Попробуйте его переименовать.",
            )
            return self.form_invalid(form)


class EditTextBook(LoginRequiredMixin, UpdateView):
    template_name = "text_books/text_book_form.html"
    form_class = TextBookForm
    pk_url_kwarg = "text_book_id"

    def get_queryset(self):
        return TextBook.objects.filter(owner_id=self.request.user.pk)


class DeleteTextBook(LoginRequiredMixin, DeleteView):
    template_name = "text_books/confirm_deleting.html"
    success_url = reverse_lazy("my_text_books")
    pk_url_kwarg = "text_book_id"

    def get_queryset(self):
        return TextBook.objects.filter(owner_id=self.request.user.pk)


# API endpoints
class ExerciseViewSet(LoginRequiredMixin, ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    pagination_class = ExerciseAPIListPagination

    def get_queryset(self):
        return self.queryset.filter(text_book__owner_id=self.request.user.pk)

    def list(self, request):
        text_book_id = request.GET.get("text_book_id")
        if text_book_id is not None:
            queryset = self.queryset.filter(text_book=text_book_id)
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["date"] = date.today()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class TextBookRetrieveAPIView(LoginRequiredMixin, RetrieveAPIView):
    queryset = TextBook.objects.all()
    serializer_class = TextBookSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return self.queryset.filter(owner_id=self.request.user.pk)
