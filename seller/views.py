from django.shortcuts import render
from django.views.generic import CreateView
from first_app.forms import RegistrationForm, RegistrationSellerForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def index(request):
    return render(request, 'seller/index.html')

class RegisterView(CreateView):
    template_name = 'seller/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

class LoginView(LoginView):
    template_name = 'seller/login.html'

class RegisterSellerView(LoginRequiredMixin, CreateView):
    template_name = 'seller/registerseller.html'
    form_class = RegistrationSellerForm
    success_url = reverse_lazy('index')

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     if response.status_code == 302:
    #         gst = request.POST.get('gst')
    #         warehouse_location = request.POST.get('warehouse_location')
    #         user = CustomUser.objects.get(email = request.POST.get('email'))
    #         s_add = SellerAdditional.objects.create(user = user, gst = gst, warehouse_location = warehouse_location)
    #         return response
    #     else:
    #         return response

    def form_valid(self, form):
        user = self.request.user
        user.type.append(user.Types.SELLER)
        user.save()
        form.instance.user = self.request.user
        return super().form_valid(form)


class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('index')
