from django.urls import path

from apps.comments.views import ReviewsView, ReviewView

urlpatterns = [
    path('<slug:slug>/', ReviewsView.as_view()),
    path('<slug:slug>/<str:id>/', ReviewView.as_view()),
]
