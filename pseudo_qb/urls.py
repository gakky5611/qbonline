from django.urls import path

from . import views

app_name='pseudo_qb'
urlpatterns = [
   path('',views.PracticeView, name='practice'),
   path('register/', views.RegisterView.as_view(), name='register'),
]