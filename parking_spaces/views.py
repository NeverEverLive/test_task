from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from parking_spaces.models import Reservation

from parking_spaces.forms import ReservationForm, AuthUserForm, RegisterUserForm


@permission_required('parking_spaces.delete_reservation')
def delete_page(request, pk):
    get_reservation = Reservation.objects.get(pk=pk)
    get_reservation.delete()
    return redirect(reverse('edit_page'))


class HomeListView(ListView):
    model = Reservation
    template_name = 'index.html'
    context_object_name = 'queryset'


class HomeDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'detail.html'
    context_object_name = 'get_reservation'


class CustomSuccessMessageMixin:
    @property
    def success_message(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super(CustomSuccessMessageMixin, self).form_valid(form)

    def get_success_url(self):
        return f'{self.success_url}?id={self.object.id}'


class ReservationCreateView(PermissionRequiredMixin, CustomSuccessMessageMixin, CreateView):
    model = Reservation
    template_name = 'edit_page.html'
    form_class = ReservationForm
    success_url = reverse_lazy('edit_page')
    success_message = "Record Created"
    permission_required = 'parking_spaces.add_reservation'

    def get_context_data(self, **kwargs):
        kwargs['queryset'] = Reservation.objects.all().order_by('start_date')
        return super(ReservationCreateView, self).get_context_data(**kwargs)


class ReservationUpdateView(PermissionRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Reservation
    template_name = 'edit_page.html'
    form_class = ReservationForm
    success_url = reverse_lazy('edit_page')
    success_message = "Record updated"
    permission_required = 'parking_spaces.change_reservation'

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super(ReservationUpdateView, self).get_context_data(**kwargs)


class ReservationDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reservation
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_message = "Record deleted"
    permission_required = 'parking_spaces.delete_reservation'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ReservationDeleteView, self).post(request)


class ParkingLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url


class RegisterView(CreateView, CustomSuccessMessageMixin):
    model = User
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('home')
    success_message = "User created"

    def form_valid(self, form):
        form_valid = super(RegisterView, self).form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


class LogOutView(LogoutView):
    next_page = reverse_lazy('home')
