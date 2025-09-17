from django import forms
from .models import Stock


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_name', 'quantity', 'category', 'brand', 'price', 'reorder_level','receive_quantity', 'issue_to', 'phone_number','image','export_to_CSV']
    
        
class StockSearchForm(forms.ModelForm):
    item_name= forms.CharField(required=False)
    brand = forms.CharField(required=False)
    category = forms.CharField(required=False)

    class Meta:
        model=Stock
        fields=['item_name','brand','category']
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Add placeholders and classes to the form fields
            self.fields['item_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by name...'})
            self.fields['brand'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by brand...'})
            self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Search by category...'})

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name', 'quantity']

class IssueForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=['issue_quantity']

class ReceiveForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=['receive_quantity','receive_from']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model=Stock
        fields=['reorder_level']

