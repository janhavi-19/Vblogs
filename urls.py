from django.urls import path
from . import views
from .views import BlogDetailView, BlogDeleteView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path('',views.home,name="home"),
    # path('',HomeView.as_view(),name="home"),
    path('blog/<int:pk>',BlogDetailView.as_view(),name="blog-detail"),
    path('blog/update/<int:pk>',BlogUpdateView.as_view(),name="blog-update"),
    path('blog/delete/<int:pk>',BlogDeleteView.as_view(),name="blog-delete"),
    

]
