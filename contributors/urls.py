from django.urls import path
from contributors import views

urlpatterns = [
    path('contributors/', views.ContributorList.as_view()),
    path('contributors/<int:pk>/', views.ContributorDetail.as_view())
]