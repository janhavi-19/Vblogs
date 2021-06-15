
from django.urls import path
from . import views
from .views import BlogDetailView,AddPostView, CategoryView, LikeView, AddCategoryView, UpdatePostView, DeletePostView, AddCommentView, ThoughtsView, AllBlogsView, Overview

urlpatterns = [
    path('',views.home,name="home"),
    # path('',HomeView.as_view(),name="home"),
    path('blog/<int:pk>',BlogDetailView.as_view(),name="blog-detail"),
    path('add_post/',AddPostView.as_view(),name="add_post"),
    path('add_category/',AddCategoryView.as_view(),name="add_category"),
    path('blog/edit/<int:pk>',UpdatePostView.as_view(), name='update_post'),
    path('blog/delete/<int:pk>',DeletePostView.as_view(),name="blog_delete"),
    path('category/<str:cats>/',views.CategoryView,name="category"),
    path('like/<int:pk>/',LikeView,name="like_post"),
    path('about_us',views.AboutView,name="about_us"),
    path('contact_us',views.ContactUsView,name="contact_us"),
    path('search',views.search,name="search"),
    path('all_blogs/',AllBlogsView.as_view(),name="all_blogs"),
    #path('my_blogs/<int:pk>',MyBlogsView.as_view(),name="my_blogs"),
    path('searchCategory/',views.searchCategory,name="searchCategory"),
    path('blog/<int:pk>/comment/',AddCommentView.as_view(),name="add_comment"),
    path('blog/<int:pk>/thoughts/',ThoughtsView.as_view(),name="add_thoughts"),
    path('overview/<int:pk>',Overview.as_view(),name="overview"),
]
