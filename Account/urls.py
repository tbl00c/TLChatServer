from django.conf.urls import url
from .views import UserLoginAPIView, UserRegisterAPIView, getToken

urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view()),
    url(r'^register/$', UserRegisterAPIView.as_view()),
    url(r'^gettoken/$', getToken),
]