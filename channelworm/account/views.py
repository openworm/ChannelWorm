from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from account.form import UserForm


def register():
    return 'user_register_form.html'


def index(request):
    return render(request, 'digitizer/index.html')


class RegisterView(View):
    form_class = UserForm
    initial = {'key': 'value'}
    template_name = 'account/user_register_form.html'
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {'form': form})
