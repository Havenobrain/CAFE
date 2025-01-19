from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__' 

    def validate_table_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("Номер стола должен быть положительным числом.")
        return value

    def validate_items(self, value):
        if not value.strip():
            raise serializers.ValidationError("Список блюд не может быть пустым.")
        return value

    def validate(self, data):
        if data['status'] not in ['pending', 'ready', 'paid']:
            raise serializers.ValidationError({"status": "Недопустимое значение статуса. Используйте 'pending', 'ready' или 'paid'."})
        return data
