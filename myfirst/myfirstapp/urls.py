from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('/first',views.Myonly.as_view()),
    path('/article',views.article),
    path('/detail/<int:article_id>',views.get_detail_page),
    path('/image',views.image),
    path('/apps', views.apps),
    path('/down',views.ImageView.as_view()),
    path('/testcookie',views.Cookietest.as_view()),
    path('/getcookie',views.Cookietest1.as_view()),
    path('/authorize', views.Authorize.as_view()),
    path('/user', views.UserView.as_view()),
    path('/logout',views.Loginout.as_view()),
    path('/status',views.Status.as_view()),
    path('/weather',views.Weather.as_view())
]