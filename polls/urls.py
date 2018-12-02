from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/',views.RegisterView.as_view(), name="register"),
    path('<int:pk>/',views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/aggregate/', views.aggregate, name='aggregate'),
    path('score',views.scoreview, name="score"),
    path('<int:question_id>/<int:active_id>/detail_list', views.DetailListView.as_view(), name="detail_list"),
]
