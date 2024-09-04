from django.urls import path
from .views import CurrentCustomerView, CustomerUpdateView, CustomerDeleteView, PasswordUpdateView
from .views import AddressCreateView, AddressRetrieveView, AddressUpdateView, AddressDeleteView


urlpatterns = [
    path('me/', CurrentCustomerView.as_view(), name='current-customer-detail'),
    path('me/update/', CustomerUpdateView.as_view(), name='current-customer-update'),
    path('me/delete-account/', CustomerDeleteView.as_view(), name='current-customer-delete-account'),
    path('me/update-password/', PasswordUpdateView.as_view(), name='current-customer-update-password'),
    path('address/create/', AddressCreateView.as_view(), name='address-create'),
    path('address/<int:pk>/', AddressRetrieveView.as_view(), name='address-retrieve'),
    path('address/<int:pk>/update/', AddressUpdateView.as_view(), name='address-update'),
    path('address/<int:pk>/delete/', AddressDeleteView.as_view(), name='address-delete'),
]
