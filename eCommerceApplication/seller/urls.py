from django.urls import path
from .views import CurrentSellerView, SellerUpdateView, SellerDeleteView, PasswordUpdateView
from .views import ProductCreateView, ProductRetrieveView, ProductUpdateView, ProductDeleteView


urlpatterns = [
    path('me/', CurrentSellerView.as_view(), name='current-seller-detail'),
    path('me/update/', SellerUpdateView.as_view(), name='current-seller-update'),
    path('me/delete-account/', SellerDeleteView.as_view(), name='current-seller-delete-account'),
    path('me/update-password/', PasswordUpdateView.as_view(), name='current-seller-update-password'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', ProductRetrieveView.as_view(), name='product-retrieve'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
]
