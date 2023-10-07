from django.urls import path, include, re_path
from api.v1.servis.questions import QuestionListAPI


urlpatterns = [
    path("questions/", QuestionListAPI.as_view()),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
