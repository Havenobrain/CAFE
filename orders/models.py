from typing import Any
from django.db import models


class Order(models.Model):
    """
    Модель заказа в кафе. Содержит информацию о номере стола, заказанных блюдах,
    общей стоимости, статусе заказа и дате создания.
    """
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number: int = models.PositiveIntegerField()
    items: str = models.TextField(help_text="Список блюд в формате: 'Название - Цена'")
    total_price: float = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status: str = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at: Any = models.DateTimeField(auto_now_add=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Переопределяет метод save для автоматического расчёта total_price
        перед сохранением объекта в базу данных.
        """
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self) -> float:
        """
        Вычисляет общую стоимость заказа, основываясь на списке блюд и их ценах.

        Ожидается, что items состоит из строк формата "Название - Цена",
        разделённых символом новой строки.

        Returns:
            float: Общая стоимость всех блюд в заказе.
        """
        total: float = 0
        for item in self.items.split('\n'):
            try:
                _, price = item.rsplit('-', 1)
                total += float(price.strip())
            except (ValueError, IndexError):
                continue
        return total
