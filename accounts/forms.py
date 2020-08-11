from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # '__all__' is equal to ['customer', 'product', 'date_created', 'status']
        