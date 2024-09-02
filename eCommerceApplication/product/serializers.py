from .models import Product

class ProductSerializer():
    class Meta:
        model = Product
        fields = '__all__'

    class create():
        product = Product(data)
        return product
