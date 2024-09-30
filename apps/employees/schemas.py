from datetime import date
from decimal import Decimal

from ninja import ModelSchema
from pydantic import field_serializer

from .models import Employee


class EmployeeSchema(ModelSchema):

    @staticmethod
    def __date_to_string(date: date):
        return date.strftime('%Y-%m-%d')
    
    @field_serializer('birth_date', check_fields=False)
    def serialize_birth_date(self, birth_date: date) -> str:
        return self.__date_to_string(birth_date)
    
    @field_serializer('hire_date', check_fields=False)
    def serialize_hire_date(self, hire_date: date) -> str:
        return self.__date_to_string(hire_date)
    
    @field_serializer('card_date', check_fields=False)
    def serialize_card_date(self, card_date: date) -> str:
        return self.__date_to_string(card_date)

    @field_serializer('salary', check_fields=False)
    def serialize_salary(self, salary: Decimal) -> float:
        return float(salary)

    class Meta:
        model = Employee
        fields = '__all__'