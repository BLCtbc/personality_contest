from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('mailing_list', views.add_user_to_mailing_list, name='mailing_list'),
    path('live', views.LiveShowsView.as_view(), name='shows')
]
