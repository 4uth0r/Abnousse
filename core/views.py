from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import ContactForm


class HomeView(TemplateView):
    template_name = 'core/index.html'


class AboutView(TemplateView):
    template_name = 'core/about.html'


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _('پیام شما با موفقیت ارسال شد.'))
        return super().form_valid(form)
