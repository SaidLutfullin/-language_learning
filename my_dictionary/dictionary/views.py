from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from loguru import logger
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ServicePage
from dictionary.forms import Exporting
from dictionary.models import Words
from dictionary.serializers import (WordAnswerSerializer, WordCreateSerializer,
                                    WordsSerializer)
from dictionary.words_operation import (export_words,
                                        get_dictionary_statistics,
                                        get_question, get_words_list,
                                        send_answer)


class AddingWord(LoginRequiredMixin, TemplateView):
    template_name = "dictionary/adding_word.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["constants"] = {
            "API_URL": self.request.build_absolute_uri("/") + "api/v1/",
            "csrfToken": get_token(self.request),
            "user_lang": self.request.user.language_learned.language_code,
        }
        return context


class EditWord(LoginRequiredMixin, TemplateView):
    template_name = "dictionary/edit.html"
    success_url = reverse_lazy("dictionary")

    @logger.catch
    def get_object(self):
        return get_object_or_404(
            Words, pk=self.request.GET.get("id"), user_id=self.request.user.pk
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word = self.get_object()

        context["constants"] = {
            "API_URL": self.request.build_absolute_uri("/") + "api/v1/",
            "csrfToken": get_token(self.request),
            "user_lang": self.request.user.language_learned.language_code,
            "word_id": word.id,
            "russian_word": word.russian_word,
            "foreign_word": word.foreign_word,
            "context": word.context,
            "asking_date": word.asking_date,
            "success_url": reverse_lazy("dictionary"),
        }
        return context


class CreateUpdateWordAPIView(GenericAPIView, CreateModelMixin, UpdateModelMixin):
    model = Words
    serializer_class = WordCreateSerializer

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        language = self.request.user.language_learned
        serializer.save(user=user, language=language)


class Dictionary(LoginRequiredMixin, ListView):
    model = Words
    template_name = "dictionary/dictionary.html"
    context_object_name = "word_list"
    paginate_by = 10

    @logger.catch
    def get_queryset(self):
        search_query = self.request.GET.get("search-quesry", "")
        words_list = get_words_list(self.request.user, search_query)
        return words_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics = get_dictionary_statistics(self.request.user)
        context.update(statistics)

        search_query = self.request.GET.get("search-quesry")
        if search_query is not None and search_query != "":
            context["search_query"] = search_query
        return context


class TestView(LoginRequiredMixin, TemplateView):
    template_name = "dictionary/testing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["constants"] = {
            "question_type": self.kwargs["question_type"],
            "word_operations_api": reverse("word_operations_api"),
            "get_success_page_api": reverse("get_success_page_api"),
            "tts": reverse("tts"),
            "csrfToken": get_token(self.request),
            "user_lang": self.request.user.language_learned.language_code,
        }
        return context


class Exporting(LoginRequiredMixin, FormView):
    form_class = Exporting
    template_name = "dictionary/exporting.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["label_suffix"] = ""
        return kwargs

    def form_valid(self, form):
        fields = [key for key in form.cleaned_data if form.cleaned_data[key]]
        path = export_words(self.request.user, fields)
        return FileResponse(open(path, "rb"))


# API endpoints
class WordOperations(LoginRequiredMixin, APIView):

    def get(self, request):
        excluded_word_id = request.query_params.get("excludedWordID")
        question = get_question(request.user, excluded_word_id)
        serializer = WordsSerializer(question)
        return Response(serializer.data)

    def post(self, request):
        serializer = WordAnswerSerializer(data=request.data)
        if serializer.is_valid():
            send_answer(
                request.user, serializer.data["word_id"], serializer.data["is_correct"]
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSuccessPage(LoginRequiredMixin, APIView):

    def get(self, request):
        try:
            page = ServicePage.objects.filter(page_type="test_completed").first()
        except ObjectDoesNotExist:
            page = None
        response_data = {
            "success_page_title": page.title,
            "success_page": page.text,
        }
        return Response(response_data)
