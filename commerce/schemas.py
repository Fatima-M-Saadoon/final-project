import datetime
from typing import List
from django.db.models.fields import BooleanField
from ninja import Schema
from pydantic import UUID4

from commerce.models import ProductImage


class CategoryOut(Schema):
    id: UUID4
    name: str
    description: str
    image: str


class CategoryCreat(Schema):
    name: str
    description: str
    image: str
    created: datetime.datetime
    is_active = bool


class ImageOut(Schema):
    image: str
    is_default_image: bool

'''
class ImageIn(Schema):
    image: str
    is_default_image: bool
    product: UUID4
'''

class ProductOut(Schema):
    id: UUID4
    is_featured: bool
    name: str
    description: str
    images: List[ImageOut]
    size: str
    qty: int
    price: int
    discounted_price: float
    category: CategoryOut
    created: datetime.datetime
    updated: datetime.datetime

'''
class ProductCreate(Schema):
    is_featured: bool
    name: str
    description: str
    image: List[UUID4]
    size: str
    qty: int
    cost: int
    price: int
    discounted_price: float
    category: UUID4
'''

class AddToCartPayload(Schema):
    product_id: UUID4
    qty: int
    ordered: bool

class UUIDSchema:
    id=UUID4


class ItemSchema(Schema):
    product: ProductOut
    item_qty: int
    ordered: bool
    id:UUID4

class ItemOut( ItemSchema):
    id=UUID4
    # class UUIDSchema(Schema):
    #     id: UUID4


class UserOut(Schema):
    username: str


class OrderSchema(Schema):
    items: List[ItemSchema]
    order_total: float
    ordered: bool
    user: UserOut


class OrderCreate(Schema):
    items: List[UUID4]
    item_qty:int
