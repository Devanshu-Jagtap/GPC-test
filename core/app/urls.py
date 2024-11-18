from django.urls import path
from django.views.generic.base import View
from . views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Login page
    path('signup/', SignupView.as_view(), name='signup'),
     path('index/', IndexView.as_view(), name='index'),
     path('form/', FormPage.as_view(), name='form'),
     path('fetch-subcategories/', FetchSubcategoriesView.as_view(), name='fetch_subcategories'),
     path('submit-news/', SubmitNewsView.as_view(), name='submit_news'),
     path('subcategory/', SubCategoryView.as_view(), name='subcategory'),
     path('subcategory/<int:id>/', SubCategoryView.as_view(), name='subcategory'),
     path('news/', news_list.as_view(), name='news_list'),
     path('news/<int:id>/', news_detail.as_view(), name='news_detail'),
    path('category/', CategoryView.as_view(), name='category'),  # List and create categories
    path('category/<int:id>/', CategoryView.as_view(), name='category_detail'),  # Update and delete a category
    path('logout/', LogoutView.as_view(), name='logout'),
   
]