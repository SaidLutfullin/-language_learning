from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from loguru import logger

from .forms import ContactForm
from .services import send_email


class ContactUs(FormView):
    form_class = ContactForm
    template_name = "feedback/contact_us.html"
    success_url = reverse_lazy("contact_us")

    def get_initial(self):
        if self.request.user.is_authenticated:
            first_name = self.request.user.first_name
            last_name = self.request.user.last_name
            full_name = []
            if first_name:
                full_name.append(first_name)
            if last_name:
                full_name.append(last_name)
            full_name = " ".join(full_name)
            if not full_name:
                full_name = self.request.user.username

            email = self.request.user.email
            return {"name": full_name, "email": email}

    def form_valid(self, form):
        try:
            send_email(self.request.user.id, form.cleaned_data)
            self.object = form.save()
            messages.success(self.request, "Сообщение отправлено")
            return HttpResponseRedirect(self.get_success_url())
        except Exception as ex:
            logger.error(ex)
            messages.error(self.request, "Сообщение не отправлено")
            return self.render_to_response(self.get_context_data(form=form))
