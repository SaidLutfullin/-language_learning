import re
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, ListView, TemplateView, UpdateView
from loguru import logger
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import ServicePage

from .forms import AddinWordForm, EditingForm, Exporting
from .models import Words
from .serializers import WordAnswerSerializer, WordsSerializer
from .words_operation import (
    export_words,
    get_dictionary_statistics,
    get_question,
    get_words_list,
    send_answer,
)


class AddingWord(LoginRequiredMixin, FormView):
    form_class = AddinWordForm
    template_name = "dictionary/adding_word.html"
    success_url = reverse_lazy("adding_word")
    initial = {"asking_date": date.today()}

    @logger.catch
    def form_valid(self, form):
        word = form.save(commit=False)
        word.user_id = self.request.user.pk
        word.language = self.request.user.language_learned
        word.russian_word = re.sub(r"\<[^>]*\>", "", word.russian_word)
        word.foreign_word = re.sub(r"\<[^>]*\>", "", word.foreign_word)
        word.context = re.sub(r"\<[^>]*\>", "", word.context)

        if not form.cleaned_data["start_learning"]:
            word.asking_date = None

        word.save()
        return HttpResponseRedirect(self.get_success_url())


class EditWord(LoginRequiredMixin, UpdateView):
    form_class = EditingForm
    template_name = "dictionary/edit.html"
    success_url = reverse_lazy("dictionary")

    @logger.catch
    def get_object(self):
        return get_object_or_404(
            Words, pk=self.request.GET.get("id"), user_id=self.request.user.pk
        )

    @logger.catch
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if "delete" in self.request.POST:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    @logger.catch
    def form_valid(self, form):
        word = form.save(commit=False)
        # delete html tags from users strings just in case
        word.russian_word = re.sub(r"\<[^>]*\>", "", word.russian_word)
        word.foreign_word = re.sub(r"\<[^>]*\>", "", word.foreign_word)
        word.context = re.sub(r"\<[^>]*\>", "", word.context)

        if "save" in self.request.POST:
            if form.cleaned_data["start_learning"]:
                word.box_number = 0
                word.save(
                    update_fields=[
                        "russian_word",
                        "foreign_word",
                        "context",
                        "asking_date",
                        "box_number",
                    ]
                )
            else:
                word.save(update_fields=["russian_word", "foreign_word", "context"])
        return HttpResponseRedirect(self.get_success_url())


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
            "csrfToken": get_token(self.request),
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
        question = get_question(request.user)
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
