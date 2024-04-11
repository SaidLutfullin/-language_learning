from io import BytesIO
from pathlib import Path

import fitz
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, FormView, ListView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import BaseUpdateView, CreateView, UpdateView
from PIL import Image
from rest_framework import status, viewsets
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from config.config_file import TRANSLATION_API_KEY, TRANSLATION_API_URL
from reader.forms import ForeignBookForm, PDFBookForm
from reader.models import ForeignBook, ForeignBookPage, PDFBook
from reader.serializers import (ForeignBookPageSerializer, PDFBookSerializer,
                                PDFBookSetPageNumberSerializer)


class ForeignBooksChooseTypeDetailView(LoginRequiredMixin, TemplateView):
    template_name = "reader/foreign_books_choose_type.html"


class ForeignBookListView(LoginRequiredMixin, ListView):
    model = ForeignBook
    template_name = "reader/foreign_book_list.html"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )


class ForeignBookCreateView(LoginRequiredMixin, FormView):
    model = ForeignBook
    form_class = ForeignBookForm
    template_name = "reader/foreign_book_form.html"
    pk_url_kwarg = "book_id"

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )

    def get_success_url(self):
        return reverse_lazy(
            "show_foreign_book", kwargs={"book_id": self.foreign_book.pk}
        )

    def form_valid(self, form):
        self.foreign_book = form.save(commit=False)
        self.foreign_book.user_id = self.request.user.pk
        self.foreign_book.language = self.request.user.language_learned
        self.foreign_book.save()
        return HttpResponseRedirect(self.get_success_url())


class ForeignBookUpdateView(ForeignBookCreateView, BaseUpdateView):
    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editing"] = True
        return context


class ForeignBookDeleteView(LoginRequiredMixin, DeleteView):
    model = ForeignBook
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy("foreign_books")
    template_name = "reader/foreign_book_confirm_delete.html"

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )


class ForeignBookShow(LoginRequiredMixin, DetailView):
    template_name = "reader/foreign_book_reader.html"
    model = ForeignBook
    pk_url_kwarg = "book_id"

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = context["object"].pk
        context["constants"] = {
            "API_URL": self.request.build_absolute_uri("/") + "api/v1/",
            "csrfToken": get_token(self.request),
            "user_lang": self.request.user.language_learned.language_code,
            "book_id": book_id,
            "update_url": reverse("foreign_books_update", kwargs={"book_id": book_id}),
        }
        return context


class ForeignBookPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        ordering = "id"
        queryset = queryset.order_by(ordering)
        return super().paginate_queryset(queryset, request, view)


class ForeignBookPageViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    model = ForeignBookPage
    queryset = ForeignBookPage.objects.all()
    pagination_class = ForeignBookPagination
    serializer_class = ForeignBookPageSerializer

    def get_queryset(self):
        queryset = self.model.objects.filter(
            foreign_book__language=self.request.user.language_learned,
            foreign_book__user=self.request.user,
        )

        book_id = self.request.query_params.get("book_id")
        if book_id is not None:
            queryset = queryset.filter(foreign_book_id=book_id)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        current_page_number = self.paginator.page.number
        response.data["current_page"] = current_page_number
        return response


class TranslateAPIView(LoginRequiredMixin, APIView):
    def get(self, request):
        word = request.query_params.get("word")
        src_lang = request.query_params.get("src_lang")
        dest_lang = request.query_params.get("dest_lang")

        is_error = False
        if word and src_lang and dest_lang:
            options = 0x0004
            uri = f"{TRANSLATION_API_URL}?key={TRANSLATION_API_KEY}&lang={src_lang}-{dest_lang}&text={word}&flags={options}&ui={src_lang}"
            response = requests.post(uri)
            if response.status_code != 200:
                is_error = True
            try:
                response_data = response.json()
                if "def" in response_data:
                    data = {"dictionary_articles": response_data["def"]}
                    return JsonResponse(data)
                else:
                    is_error = True
            except:
                is_error = True
        else:
            is_error = True
        if is_error:
            return Response(
                {"error": "Internal server error."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PDFBookCreateView(LoginRequiredMixin, CreateView):
    model = PDFBook
    form_class = PDFBookForm
    template_name = "reader/PDFbook_form.html"
    success_url = reverse_lazy("PDFbook_list")

    def form_valid(self, form):
        try:
            book = form.save(commit=False)
            book.user = self.request.user
            book.language = self.request.user.language_learned
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
            book.preview_image.save(
                f"PDFbook_preview_image{Path(book.book_file.name).stem}_preview.jpg",
                content_file,
                save=False,
            )

            book.save()
            return HttpResponseRedirect(self.success_url)
        except:
            form.add_error(
                "book_file",
                "Некоректное имя или формат файла. Попробуйте его переименовать.",
            )
            return self.form_invalid(form)


class PDFBookUpdateView(LoginRequiredMixin, UpdateView):
    model = PDFBook
    template_name = "reader/PDFbook_form.html"
    form_class = PDFBookForm
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy("PDFbook_list")

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.pk)


class PDFBookListView(LoginRequiredMixin, ListView):
    model = PDFBook
    template_name = "reader/PDFbook_list.html"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )


class PDFBookShow(LoginRequiredMixin, TemplateView):
    template_name = "reader/PDFbook_reader.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = kwargs.get("book_id")
        context["constants"] = {
            "API_URL": self.request.build_absolute_uri("/") + "api/v1/",
            "csrfToken": get_token(self.request),
            "user_lang": self.request.user.language_learned.language_code,
            "book_id": book_id,
            "update_url": reverse("PDFbook_update", kwargs={"book_id": book_id}),
        }
        return context


class PDFBookDeleteView(LoginRequiredMixin, DeleteView):
    model = PDFBook
    pk_url_kwarg = "book_id"
    success_url = reverse_lazy("PDFbook_list")
    template_name = "reader/foreign_book_confirm_delete.html"

    def get_queryset(self):
        return self.model.objects.filter(
            user_id=self.request.user.pk, language=self.request.user.language_learned
        )


class PDFBookRetrieveAPIView(LoginRequiredMixin, RetrieveAPIView):
    queryset = PDFBook.objects.all()
    serializer_class = PDFBookSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk)


class PDFBookSetPageNumberAPIView(LoginRequiredMixin, UpdateAPIView):
    queryset = PDFBook.objects.all()
    serializer_class = PDFBookSetPageNumberSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.pk)
