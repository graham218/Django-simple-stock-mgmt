from django import forms
from .models import *

class StockCreateForm(forms.ModelForm):
	class Meta:
		model=Stock
		fields=['category','item_name','quantity']
	#prevent saving form with blank details
	def clean_category(self):
		category=self.cleaned_data.get('category')
		if not category:
			raise forms.ValidationError('This field is required')

		for instance in Stock.objects.all():
			if instance.category==category:
				raise forms.ValidationError(category+' is already created')
		return category

	def clean_item_name(self):
		item_name=self.cleaned_data.get('item_name')
		if not item_name:
			raise forms.ValidationError('This field is required')
		return item_name

class StockSearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	class Meta:
		model = Stock
		fields = ['category', 'item_name']

class StockUpdateForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['category', 'item_name', 'quantity']

class IssueForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['receive_quantity', 'receive_by']

class ReorderLevelForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['reorder_level']

class StockHistorySearchForm(forms.ModelForm):
	export_to_CSV = forms.BooleanField(required=False)
	start_date = forms.DateTimeField(required=False)
	end_date = forms.DateTimeField(required=False)
	class Meta:
		model = StockHistory
		fields = ['category', 'item_name', 'start_date', 'end_date']

class CategorysForm(forms.ModelForm):
	class Meta:
		model=Category
		fields=['name']

class CustomerDetailsForm(forms.ModelForm):
	class Meta:
		model=CustomerDetails
		fields=['customer_name','national_id','email','phone_number','home_address']
	#preventing null and duplicate entries
	def clean_customer_name(self):
		customer_name=self.cleaned_data.get('customer_name')
		if not customer_name:
			raise forms.ValidationError('Customers name is required')
		return customer_name

	def clean_national_id(self):
		national_id=self.cleaned_data.get('national_id')
		if not national_id:
			raise forms.ValidationError("Customer's National ID is required")
		for instance in CustomerDetails.objects.all():
			if instance.national_id==national_id:
				raise forms.ValidationError('Customer with national ID '+national_id+' already exists')
		return national_id

	def clean_email(self):
		email=self.cleaned_data.get('email')
		if not email:
			raise forms.ValidationError('This field is required')
		for instance in CustomerDetails.objects.all():
			if instance.email==email:
				raise forms.ValidationError('A customer with this email address already exists')
		return email

	def clean_phone_number(self):
		phone_number=self.cleaned_data.get('phone_number')
		if not phone_number:
			raise forms.ValidationError('Customers name is required')
		
		for instance in CustomerDetails.objects.all():
			if instance.phone_number==phone_number:
				raise forms.ValidationError('A customer with this phone number already exists')
		return phone_number
	
class CustomerSearchForm(forms.ModelForm):
	export_to_CSV=forms.BooleanField(required=False)
	class Meta:
		model=CustomerDetails
		fields=['customer_name','national_id']

class CustomerUpdateForm(forms.ModelForm):
	class Meta:
		model=CustomerDetails
		fields=['customer_name','national_id','email','phone_number','home_address']