from django.urls import path
from . import views

# urlpatterns = [
#     path('products/', views.product_list_api_view),
#     path('products/<int:id>/', views.product_detail_api_view),
#     path('products/reviews/', views.products_reviews_rating_view),
#
#     path('reviews/', views.review_list_api_view),
#     path('reviews/<int:id>/', views.review_detail_api_view),
#
#     path('categories/', views.category_list_api_view),
#     path('categories/<int:id>/', views.category_detail_api_view),
# ]


urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('products/reviews/', views.products_reviews_rating_view),

    path('reviews/', views.review_list_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),

    path('categories/', views.category_list_api_view),
    path('categories/<int:id>/', views.category_detail_api_view),
]