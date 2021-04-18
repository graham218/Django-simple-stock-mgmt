from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
	title = 'Welcome: This is the Home Page'
	context = {
	"title": title,
	}
	return render(request, "home.html",context)

@login_required
def myCategory(request):
	form=CategorysForm(request.POST or None)
	title="Add new Categories here"
	context={
		"title":title,
		"form":form,
	}
	return render(request, "add_categories.html",context)

@login_required
def list_item(request):
	header="LIST OF ITEMS"
	form=StockSearchForm(request.POST or None)
	queryset=Stock.objects.all()
	context={
		"header":header,
		"queryset":queryset,
		"form":form,
	}
	if request.method== 'POST':
		queryset=Stock.objects.filter(category__icontains=form['category'].value(),
			item_name__icontains=form['item_name'].value()
			)
		if form['export_to_csv'].value()==True:
			response=HttpResponse(content_type='text/csv')
			response['Content-Disposition']='attachment; filename="List_of_stock.csv"'
			writer=csv.writer(response)
			writer.writerow(['CATEGORY','ITEM NAME','QUANTIY'])
			instance=queryset
			for stock in instance:
				writer.writerow([stock.category, stock.item_name, stock.quantity])
			return response

		context={
			"form":form,
			"header":header,
			"queryset":queryset,
		}
	return render(request, "list_item.html", context)

@login_required
def add_items(request):
	title="Add Items"
	form=StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,"Successfully saved")
		return redirect("/list_item")
	context={
		"title":title,
		"form":form,
	}
	return render(request, "add_items.html", context)

@login_required
def update_items(request, pk):
	queryset=Stock.objects.get(id=pk)
	form=StockUpdateForm(instance=queryset)
	if request.method=='POST':
		form=StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request,"Updated successfully")
			return redirect("/list_item")
	context={
		"form":form,
	}
	return render(request, "add_items.html", context)

@login_required
def delete_items(request, pk):
	queryset=Stock.objects.get(id=pk)
	if request.method=='POST':
		queryset.delete()
		messages.success(request,"Successfully deleted")
		return redirect("/list_item")
	return render(request, "delete_items.html")

def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
		"title": queryset.item_name,
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)

def issue_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = IssueForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.receive_quantity=0
		instance.quantity -= instance.issue_quantity
		instance.issue_by = str(request.user)
		messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
		instance.save()

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": 'Issue ' + str(queryset.item_name),
		"queryset": queryset,
		"form": form,
		"username": 'Issue By: ' + str(request.user),
	}
	return render(request, "add_items.html", context)


def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.issue_quantity = 0
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Receive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)

def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))

		return redirect("/list_item")
	context = {
			"instance": queryset,
			"form": form,
		}
	return render(request, "add_items.html", context)

@login_required
def list_history(request):
	header = 'LIST OF ITEMS'
	form = StockHistorySearchForm(request.POST or None)
	queryset = StockHistory.objects.all()
	context = {
		"header": header,
		"queryset": queryset,
		"form": form,
	}
	#form = StockSearchForm(request.POST or None)
	if request.method == 'POST':
		category = form['category'].value()
		queryset = StockHistory.objects.filter(
								item_name__icontains=form['item_name'].value()
								)
		queryset = StockHistory.objects.filter(
						item_name__icontains=form['item_name'].value(),
						last_updated__range=[
												form['start_date'].value(),
												form['end_date'].value()
											]
						)
		if (category != ''):
			queryset = queryset.filter(category_id=category)
		if form['export_to_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
			writer = csv.writer(response)
			writer.writerow(
				['CATEGORY', 
				'ITEM NAME',
				'QUANTITY', 
				'ISSUE QUANTITY', 
				'RECEIVE QUANTITY', 
				'RECEIVE BY', 
				'ISSUE BY', 
				'LAST UPDATED'])
			instance = queryset
			for stock in instance:
				writer.writerow(
				[stock.category, 
				stock.item_name, 
				stock.quantity, 
				stock.issue_quantity, 
				stock.receive_quantity, 
				stock.receive_by, 
				stock.issue_by, 
				stock.last_updated])
			return response
		context = {
		"form": form,
		"header": header,
		"queryset": queryset,
	}

	return render(request, "list_history.html",context)

@login_required
def add_customers(request):
	title="Add New Customers"
	form=CustomerDetailsForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request,"Customer has been added successfully into the system")
		return redirect("/list_customers")
	context={
		"title":title,
		"form":form,
	}
	return render(request, "add_customers.html",context)

@login_required
def list_customers(request):
	title="List of Customers"
	header="LIST OF ALL CUSTOMERS"
	form=CustomerSearchForm(request.POST or None)
	queryset=CustomerDetails.objects.all()

	#searching
	if request.method=="POST":
		queryset=CustomerDetails.objects.filter(customer_name__icontains=form['customer_name'].value(),
		national_id__icontains=form['national_id'].value())
		
		if form['export_to_CSV'].value()==True:
			response=HttpResponse(content_type='text/csv')
			response['Content-Disposition']='attachment; filename="List of Customers.csv"'
			writer=csv.writer(response)
			writer.writerow(['CUSTOMER NAME','NATIONAL ID','EMAIL','PHONE NO','HOME ADDRESS'])
			instance=queryset
			for customers in instance:
				writer.writerow([customers.customer_name,customers.national_id,customers.email,customers.phone_number,customers.home_address])
			return response
	context={
		"title":title,
		"header":header,
		"form":form,
		"queryset":queryset,
	}
	return render(request, "list_customers.html",context)

@login_required
def update_customers(request, pk):
	queryset=CustomerDetails.objects.get(id=pk)
	form=CustomerUpdateForm(instance=queryset)
	if request.method=="POST":
		form=CustomerDetailsForm(request.POST or None, instance=queryset)
		if form.is_valid():
			form.save()
		messages.success(request,"Customer's details updated successfully on database")
		return redirect("/list_customers")
	context={
		"form":form,
	}
	return render(request, "add_customers.html",context)

@login_required
def delete_customers(request,pk):
	queryset=CustomerDetails.objects.get(id=pk)
	if request.method=="POST":
		queryset.delete()
		return redirect("/list_customers")
	messages.success(request,"Customer has been successfully deleted from the system")
	return render(request,"delete_customers.html")