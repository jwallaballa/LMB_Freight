from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import OrderForm


def add_order_view(request):
    """
    Handles the creation of a new order via a form.

    This function will render the form for a GET request and process
    the form submission for a POST request.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('dashboard'))
    else:
        form = OrderForm()

    context = {
        'form': form,
    }


    return render(request, 'order_form.html', context)
