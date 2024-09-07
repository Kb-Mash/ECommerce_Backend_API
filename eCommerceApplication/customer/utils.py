from .models import Customer
from rest_framework import status
from rest_framework.response import Response

# Responses #

def success_response(message, data=None, status_code=status.HTTP_200_OK):
    return Response({
        "status": "success",
        "message": message,
        "data": data
    }, status=status_code)

def error_response(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "status": "error",
        "message": message,
        "errors": errors
    }, status=status_code)

def not_found_response(message):
    return error_response(message, status_code=status.HTTP_404_NOT_FOUND)

def no_content_response(message):
    return success_response(message, status_code=status.HTTP_204_NO_CONTENT)

# Customer Instance #

def get_customer_instance(request):
    """
    Retrieves the customer instance based on the authenticated user.
    Returns a tuple: (customer, error_response).
    If the customer is found, error_response will be None.
    If the customer is not found, customer will be None and error_response will contain the error message.
    """
    try:
        customer = Customer.objects.get(user=request.user)
        return customer, None
    except Customer.DoesNotExist:
        err_response = not_found_content("Customer does not exist")
        return None, err_response

