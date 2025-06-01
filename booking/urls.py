from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'booking'

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('management/', views.management_view, name='management_view'),
    path('management/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('list_rooms/', views.list_rooms, name='list_rooms'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='booking:hotel_list'), name='logout'),
    path('accounts/profile/', views.hotel_list, name='profile_redirect'),
]
