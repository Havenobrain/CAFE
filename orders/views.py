from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .serializers import OrderSerializer
from .models import Order
from .forms import OrderForm


def order_list(request: HttpRequest) -> HttpResponse:
    """
    Отображает список заказов с возможностью поиска и фильтрации.

    :param request: HTTP-запрос от пользователя.
    :return: HTML-страница со списком заказов.
    """
    query: str = request.GET.get('query', '')  
    status_filter: str = request.GET.get('status', '')  
    orders = Order.objects.all()

    
    if query:
        orders = orders.filter(table_number__icontains=query)

   
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES,  
    })


def add_order(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает добавление нового заказа.

    :param request: HTTP-запрос от пользователя.
    :return: HTML-страница для добавления заказа или перенаправление на список заказов.
    """
    if request.method == 'POST':
        form: OrderForm = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/add_order.html', {'form': form})


def edit_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Обрабатывает редактирование заказа.

    :param request: HTTP-запрос от пользователя.
    :param order_id: ID редактируемого заказа.
    :return: HTML-страница для редактирования заказа.
    """
    order: Order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form: OrderForm = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/edit_order.html', {'form': form, 'order': order})


def update_status(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Обрабатывает изменение статуса заказа.

    :param request: HTTP-запрос от пользователя.
    :param order_id: ID заказа, у которого изменяется статус.
    :return: HTML-страница для изменения статуса или перенаправление на список заказов.
    """
    order: Order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        new_status: str = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return redirect('order_list')
    return render(request, 'orders/update_status.html', {'order': order})


def delete_order(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Обрабатывает удаление заказа.

    :param request: HTTP-запрос от пользователя.
    :param order_id: ID удаляемого заказа.
    :return: Перенаправление на список заказов.
    """
    order: Order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('order_list')


def revenue_report(request: HttpRequest) -> HttpResponse:
    """
    Отображает отчет по выручке за смену.

    :param request: HTTP-запрос от пользователя.
    :return: HTML-страница с общей суммой выручки.
    """
    paid_orders = Order.objects.filter(status='paid')
    total_revenue: float = sum(order.total_price for order in paid_orders)
    return render(request, 'orders/revenue_report.html', {'total_revenue': total_revenue})


class OrderViewSet(ModelViewSet):
    """
    API ViewSet для управления заказами.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['status']
