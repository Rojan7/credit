from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Customer, Entry
from .forms import CustomerForm, EntryForm
from django.contrib import messages

DASHBOARD_PASSWORD = "9842080553"

# Dashboard (Home)
def home(request):
    # --- Password protection ---
    if not request.session.get('dashboard_access', False):
        if request.method == "POST":
            password = request.POST.get("password")
            if password == DASHBOARD_PASSWORD:
                request.session['dashboard_access'] = True
                return redirect('home')
            else:
                return render(request, "shop/password.html", {"error": "Incorrect password!"})
        return render(request, "shop/password.html")  # show password form

    # --- Actual dashboard ---
    query = request.GET.get("q")
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(Q(name__icontains=query))

    total_due = sum(c.total_due for c in customers)
    last_updated = max(
        (c.last_entry_date for c in customers if c.last_entry_date),
        default=None
    )

    return render(request, "shop/home.html", {
        "customers": customers,
        "total_due": total_due,
        "last_updated": last_updated,
        "query": query or "",
    })


# Add a new customer
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = CustomerForm()
    return render(request, "shop/add_customer.html", {"form": form})


# Customer detail page + add entries
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.customer = customer
            entry.save()
            return redirect("customer_detail", pk=pk)
    else:
        form = EntryForm()

    entries = customer.entries.order_by("-date")  # latest first
    return render(request, "shop/customer_detail.html", {
        "customer": customer,
        "form": form,
        "entries": entries,
    })


# Delete an entry
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    customer_id = entry.customer.id
    entry.delete()
    return redirect("customer_detail", pk=customer_id)


# Edit an entry
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("customer_detail", pk=entry.customer.id)
    else:
        form = EntryForm(instance=entry)
    return render(request, "shop/edit_entry.html", {"form": form, "entry": entry})


# Delete customer
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        password = request.POST.get("password")
        if password == DASHBOARD_PASSWORD:  # password check
            customer_name = customer.name
            customer.delete()
            messages.success(request, f"Customer '{customer_name}' deleted successfully.")
            return redirect("home")
        else:
            messages.error(request, "Incorrect password. Customer was not deleted.")

    return render(request, "shop/delete_customer.html", {"customer": customer})
