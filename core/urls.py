from django.urls import path
from .views import HomeView, HashUrlRedirectView

urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("<slug:hashed_url>", HashUrlRedirectView.as_view(), name="go_to_url")
]
