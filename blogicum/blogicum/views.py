from blog.forms import CreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView


class CreationUserCreateView(CreateView):
    model = get_user_model()
    form_class = CreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')
