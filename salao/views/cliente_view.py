from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from ..models.agendamento import Cliente
from ..forms.cliente_form import ClienteForm

@login_required
@permission_required('salao.add_cliente', raise_exception=True)
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes:clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form, 'title': 'Adicionar Cliente'})

@login_required
@permission_required('salao.change_cliente', raise_exception=True)
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form, 'title': 'Editar Cliente'})

@login_required
@permission_required('salao.view_cliente', raise_exception=True)
def clientes_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes_list.html', {'clientes': clientes})
