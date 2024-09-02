from django.urls import path
from .views import CurrentCustomerView, CustomerUpdateView, CustomerDeleteView, PasswordUpdateView

urlpatterns = [
        path('me/', CurrentCustomerView.as_view(), name='current-customer-detail'),
        path('me/update/', CustomerUpdateView.as_view(), name='current-customer-update'),
        path('me/delete-account/', CustomerDeleteView.as_view(), name='current-customer-delete-account'),
        path('me/update-password/', PasswordUpdateView.as_view(), name='current-customer-update-password'),
]
