from pydantic import BaseModel, field_serializer, FieldSerializationInfo
from typing import Any
from typing import List
from uuid import UUID


class Product(BaseModel):
    id: UUID
    name: str
    description: str

    @field_serializer("id")
    def ser_id(self, value: Any, info: FieldSerializationInfo):
        return str(value)
    
class Offer(BaseModel):
    id: UUID
    price: int
    items_in_stock: int
