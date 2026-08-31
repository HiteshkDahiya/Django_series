from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, FormView, CreateView
from .forms import ContactUsForm, RegistrationForm, RegistrationSellerForm
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from .models import CustomUser, SellerAdditional
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def index(request):
#     age = 10
#     arr = ['priyanshu', 'aman', 'rohit', 'shubhi']
#     dic = {'a':'one', 'b':'two'}
#     return render(request, 'first_app/index.html', {'age':age, 'array':arr, 'dic':dic})
#     #return HttpResponse("<h1>Hello</h1>")

class Index(TemplateView):
    template_name = 'first_app/index.html'
    def get_context_data(self, **kwargs):
        age = 10
        arr = ['priyanshu', 'aman', 'rohit', 'shubhi']
        dic = {'a':'one', 'b':'two'}
        context_old = super().get_context_data(**kwargs)
        context = {'age':age, 'array':arr, 'dic':dic, 'context_old':context_old}
        return context


def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST['phone']
        if len(phone)<10 or len(phone)>10:
            raise ValidationError("Phone number length is not right")
        query = request.POST['query']
        print(name + " " + email + " " + phone + " " +query)
    return render(request, 'first_app/contactus.html')

def contactus2(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():      #clean_data
            if len(form.cleaned_data.get('query'))>10:
                form.add_error('query', 'Query length is not right')
                return render(request, 'first_app/contactus2.html', {'form':form})
            form.save()
            return HttpResponse("Thank You")
        else:
            # if len(form.cleaned_data.get('query'))>10:
                #form.add_error('query', 'Query length is not right')
                # form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
            return render(request, 'first_app/contactus2.html', {'form':form})
    return render(request, 'first_app/contactus2.html', {'form':ContactUsForm})

class ContactUs(FormView):
    form_class = ContactUsForm
    template_name = 'first_app/contactus2.html'
    #success_url = '/'   #hardcoded url
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        if len(form.cleaned_data.get('query'))>10:
            form.add_error('query', 'Query length is not right')
            return render(self.request, 'firstapp/contactus2.html', {'form':form})
        form.save()
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        if len(form.cleaned_data.get('query'))>10:
            form.add_error('query', 'Query length is not right')
            #form.errors['__all__'] = 'Query length is not right. It should be in 10 digits.'
        response = super().form_invalid(form)
        return response

class RegisterView(CreateView):
    template_name = 'first_app/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

class LoginView(LoginView):
    template_name = 'first_app/login.html'

class RegisterSellerView(LoginRequiredMixin, CreateView):
    template_name = 'first_app/registerseller.html'
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

