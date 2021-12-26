import datetime

from ninja import Schema
from pydantic import UUID4


class CategoryOut(Schema):
    id: UUID4
    name: str
    description: str
    image: str


class CategoryCreat(Schema):
    id: UUID4
    name: str
    description: str
    image: str
    created:datetime.datetime
    is_active=bool


class ProductOut(Schema):
    id: UUID4
    is_featured: bool
    name: str
    description: str
    size: str
    qty: int
    price: int
    discounted_price: int
    category: CategoryOut
    created: datetime.datetime
    updated: datetime.datetime


class ProductCreate(Schema):
    id: UUID4
    is_featured: bool
    name: str
    description: str
    size: str
    qty: int
    cost: int
    price: int
    discounted_price: int
    category_id: UUID4



class AddToCartPayload(Schema):
    product_id: UUID4
    qty: int
    ordered: bool
'''
class CreateOrder(Schema):
    user_id=UUID4
    items= str
    total= int
    ordered: bool
'''