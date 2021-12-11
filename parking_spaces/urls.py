from django.urls import path

from parking_spaces.views import HomeListView, HomeDetailView, delete_page, \
    ReservationCreateView, ReservationUpdateView, ReservationDeleteView,\
    ParkingLoginView, RegisterView, LogOutView


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('detail/<int:pk>', HomeDetailView.as_view(), name='detail_page'),
    path('edit/', ReservationCreateView.as_view(), name='edit_page'),
    path('update/<int:pk>', ReservationUpdateView.as_view(), name='update_page'),
    # path('delete/<int:pk>', ReservationDeleteView.as_view(), name='delete_page'),
    path('delete/<int:pk>', delete_page, name='delete_page'),
    path('login/', ParkingLoginView.as_view(), name='login_page'),
    path('sign_in/', RegisterView.as_view(), name='sign_in_page'),
    path('logout/', LogOutView.as_view(), name='log_out_page'),
]
