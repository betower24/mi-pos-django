from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib import messages

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto agregado con éxito!')
            return redirect('agregar_producto')
    else:
        form = ProductoForm()
    
    return render(request, 'pos/agregar_producto.html', {'form': form})