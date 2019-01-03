from django.urls import path
from . import views

app_name = 'Posts'

urlpatterns = [

    path('', views.PostListView.as_view(), name='post_list'),
    path('detail/<int:id>/<slug:slug>/', views.post_detail, name='detail')
]
