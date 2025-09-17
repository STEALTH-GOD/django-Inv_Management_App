from django.shortcuts import render,redirect, get_object_or_404
from .models import Stock, StockHistory
from .forms import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'inventory/home.html')

@login_required
def list_items(request):
    title = "List of Items"
    queryset = Stock.objects.all()
    form=StockSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            item_name= form.cleaned_data.get('item_name')
            brand= form.cleaned_data.get('brand')
            category= form.cleaned_data.get('category')

            if item_name:
                queryset= queryset.filter(item_name__icontains=item_name)
            if brand:
                queryset = queryset.filter(brand__icontains=brand)
            if category:
                queryset = queryset.filter(category__icontains=category)
    context={
    "title":title,
    "queryset": queryset,
    "form": form,
    }
    return render(request, 'inventory/list_items.html', context)

# def add_items(request):
#     form = StockCreateForm(request.method == "POST")
#     if form.is_valid():
#         form.save()
#     context={
#         "form": form,
#         "title": "Add Item"
#     }
#     return render(request, 'inventory/add_items.html',context)


@login_required
def add_items(request):
    if request.method == "POST":
        form = StockCreateForm(request.POST, request.FILES)
        if form.is_valid():
            item=form.save()
            messages.success(request, f'{item.item_name} has been added successfully')
            return redirect('list_items')  # Redirect after successful form submission
    else:
        form = StockCreateForm()  # Create blank form for GET request
    
    context = {
        "form": form,
        "title": "Add Item"
    }
    return render(request, 'inventory/add_items.html', context)

@login_required
def update_items(request, pk):
    item = Stock.objects.get(id=pk)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=item)
        if form.is_valid():
            changed_fields = form.changed_data  
            updated_item = form.save()

            if changed_fields:
                for field in changed_fields:
                    messages.success(
                        request,
                        f"{field.replace('_', ' ').title()} has been updated successfully"
                    )
            else:
                messages.info(request, "No changes were made")

            return redirect('list_items')
    else:
        form = StockUpdateForm(instance=item)
    
    context = {
        'form': form,
        'title': f'Update {item.item_name}'
    }
    return render(request, 'inventory/update_items.html', context)

@login_required
def delete_items(request, pk):
    item = get_object_or_404(Stock, id=pk)
    if request.method == 'POST':
        item.delete()
        messages.warning(request, f'{item.item_name} has been deleted successfully')
        return redirect('list_items')
    context = {
        'item': item
    }
    return render(request, 'inventory/delete_items.html', context)

@login_required
def stock_details(request, pk):
    stock = get_object_or_404(Stock, id=pk)   
    return render(request, 'inventory/stock_details.html', {'stock': stock})

@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity=0
        # Reset the issue_quantity field after saving to prevent old values persisting
        old_issue_quantity = instance.issue_quantity
        instance.quantity -= old_issue_quantity 
        # instance.issue_quantity = 0  # Reset the field
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        return redirect('/stock_details/'+str(instance.id))
    context = {
        "title": "Issue " + queryset.item_name,
        "queryset": queryset,
        "form": form,
        "username": "Issue",  # Add this to differentiate from add_items
        "is_issue_form": True  # Flag to identify this is an issue form
    }
    return render(request, 'inventory/issue_receive_items.html', context)  # Use a different template

@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity=0
        # Reset the receive_quantity field after saving to prevent old values persisting
        old_receive_quantity = instance.receive_quantity
        instance.quantity += old_receive_quantity
        # instance.receive_quantity = 0  # Reset the field
        messages.success(request, "Received Successfully. " + str(instance.quantity) + " " + str(instance.item_name) + "s now in Store")
        instance.save()
        return redirect('/stock_details/' + str(instance.id))

    context = {
        "title": "Receive " + queryset.item_name,
        "queryset": queryset,
        "form": form,
        "username": "Receive", 
        "is_receive_form": True  
    }
    return render(request, 'inventory/issue_receive_items.html', context)  # Use a different template


@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form= ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder Level has been set to " + str(instance.reorder_level) + " for " + str(instance.item_name))
        return redirect('/stock_details/' + str(instance.id))

    
    context = {
        "instance" : queryset,
        "form": form,
        "title": f"Change Reorder Level for {queryset.item_name}",
        "is_reorder_form": True,
        "queryset": queryset,
    }
    return render(request, 'inventory/issue_receive_items.html', context)

    
@login_required
def list_history(request):
    title = 'ITEMS HISTORY'
    queryset = StockHistory.objects.all()
    form = StockSearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        item_name=form.cleaned_data.get('item_name')
        brand= form.cleaned_data.get('brand')
        category= form.cleaned_data.get('category')

        if item_name:
            queryset=queryset.filter(item_name__icontains=item_name)
        if brand:
            queryset=queryset.filter(brand__icontains=brand)
        if category:
            queryset=queryset.filter(category__icontains=category)
    context = {
        "title": title,
        "form": form,
        "queryset":queryset,
    }
    return render(request, "inventory/list_history.html", context)

def delete_history(request, pk):
    history = get_object_or_404(StockHistory, pk=pk)
    if request.method == "POST":
        history.delete()
        messages.success(request, "History entry deleted successfully.")
    return redirect('list_history')