from django.conf.urls import url
import views

app_name = "wechat_mp"
urlpatterns = [
    url(r'^ports/', views.ports),
    # url(r'^notice/$',views.notice,name="notice"),
]
