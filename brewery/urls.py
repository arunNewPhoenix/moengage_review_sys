# brewery/urls.py
from django.urls import path
from django.views.generic import RedirectView
from .views import signup, login, brewery_search, add_review

urlpatterns = [
    path('', RedirectView.as_view(url='signup/', permanent=True)),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('search/', brewery_search, name='brewery_search'),
    path('add_review/<str:brewery_id>/', add_review, name='add_review'),
]
