from typing import List
from account.authorization import GlobalAuth
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import UUID4

from commerce.models import Product, Item, Category, Order
from commerce.schemas import ProductOut, AddToCartPayload, CategoryOut, CategoryCreat
from config.utils.schemas import MessageOut

User = get_user_model()

commerce_controller = Router(tags=['products'])
order_controller = Router(tags=['order'])

'''
@commerce_controller.get(' search_products', response={
    200: List[ProductOut],
})
def list_products(request, q: str = None,):
    products = Product.objects.all()

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    return products

'''
@commerce_controller.get('', summary='search products', response={
    200: List[ProductOut],
    404: MessageOut
})
def search_products(request, *, q: str = None):
    """
    To create an order please provide:
     - your_name
     - user_name
     - and list of Items (product + amount)
    """
    products_qs = Product.objects.filter(is_active=True)\
        .select_related( 'category')

    if not products_qs:
        return 404, {'detail': 'No products found'}

    if q:
        products_qs = products_qs.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )


    return products_qs


@commerce_controller.get('new_products', response={
    200: List[ProductOut],
})
def new_products(request, categorys: UUID4 = None, featuerd: bool = None, is_active: bool = None ):
    products = Product.objects.all()

    if categorys:
        products = products.filter(category__id=categorys
                                   )
    if featuerd:
        products = products.filter(is_featured=featuerd
                                   )
    if is_active:
        products = products.filter(is_active=is_active
                                   )
    products = products[:10]
    return products




@commerce_controller.get(' specific_products/{id}', response={
    200: ProductOut
})
def retrieve_product(request, id: UUID4):
    return get_object_or_404(Product, id=id)

#
# @commerce_controller.post('products', response={
#     201: ProductOut,
#     400: MessageOut
# })
# def create_product(request, payload: ProductCreate):
#     try:
#         product = Product.objects.create(**payload.dict(), is_active=True)
#     except:
#         return 400, {'detail': 'حدث خلل ما!'}
#
#     return 201, product


@commerce_controller.get('products', response={
    200: List[ProductOut],

})
def list_products(request):
    products = Product.objects.all()
    return products

#
# @commerce_controller.delete('Delete_product/{id}')
# def delete_product(request, id:UUID4):
#     deleted_product = get_object_or_404(Product, id=id)
#     deleted_product.delete()
#     return {"success": True}
#
#
# @commerce_controller.put(" update_product/{id}", response={
#     200: ProductOut,
#     400: MessageOut
# })
# def update_product(request, id: UUID4, update: ProductCreate):
#     product_u = get_object_or_404(Product, id=id)  #check if i have a product or not
#     for attr, value in update.dict().items():
#         setattr(update, attr, value)
#     product_u.save()
#     return product_u


@commerce_controller.get('category', response={
    200:list[CategoryOut],
})
def lists_category(request):
    category = Category.objects.all()
    return category


@commerce_controller.get('specific_category/{id}', response={
    200: CategoryOut
})
def retrieve_category(request, id:UUID4):
    return get_object_or_404(Category, id=id)


@commerce_controller.post('Category', response={
    201: CategoryOut,
    400: MessageOut
})
def create_category(request, payload: CategoryCreat):
    try:
        category = Category.objects.create(**payload.dict(), is_active=True)
    except:
        return 400, {'detail': 'something wrong happened!'}

    return 201, category


@commerce_controller.put(" update_category/{id}", response={
    200: CategoryOut,
    400: MessageOut
})
def update_category(request, id: UUID4, update: CategoryCreat):
    category_u = get_object_or_404(Category, id=id)
    for attr, value in update.dict().items():
        setattr(update, attr, value)
    category_u.save()
    return category_u


@commerce_controller.delete('delete_Category/{id}')
def delete_category(request, id: UUID4):

    deleted_category = get_object_or_404(Category, id=id)
    deleted_category.delete()
    return {"success": True}


@order_controller.post('add-to-cart', response=MessageOut, auth=GlobalAuth())
def add_to_cart(request, payload: AddToCartPayload):
    payload_validated = payload.copy()
    if payload.qty < 1:
        payload_validated.qty = 1

    try:
        item = Item.objects.get(product_id=payload.product_id)
    except Item.DoesNotExist:
        user = get_object_or_404(User, id=request.auth['pk'])
        Item.objects.create(product_id=payload.product_id, user=user, item_qty=payload_validated.qty,
                            ordered=False)
        return 200, {'detail': 'تمت عملية الاضافة الى السلة بنجاح'}

    item.item_qty += payload_validated.qty
    item.save()
    return 200, {'detail': 'item qty updated successfully!'}


@order_controller.post('increase-item/{item_id}', auth=GlobalAuth(), response=MessageOut)
def increase_item_qty(request, item_id: UUID4):
    user = get_object_or_404(User, id=request.auth['pk'])
    item = get_object_or_404(Item, id=item_id, user=user)
    item.item_qty += 1
    item.save()

    return 200, {'detail': 'تم زيادة كمية المنتج بنجاخ!'}


@order_controller.post('decrease_item/{item_id}', auth=GlobalAuth(), response=MessageOut)
def decrease_item(request, item_id: UUID4):
    user = get_object_or_404(User, id=request.auth['pk'])
    item = get_object_or_404(Item, id=item_id, user=user)
    item.item_qty -= 1
    if item.item_qty == 0:
        item.delete()
    else:
        item.save()
    return 200, {'detail': 'تم تقليل كمية المنتج بنجاح'}


@order_controller.delete('item_deleted/{id}',  auth=GlobalAuth(),response={204: MessageOut})
def deleted_item(request, id: UUID4):
    user = get_object_or_404(User, id=request.auth['pk'])
    item = get_object_or_404(Item, id=id ,user=user)
    item.delete()
    return 204, {'detail', 'تم حذف المنتج بنجاح'}



@order_controller.post('create_order',auth=GlobalAuth(),response=MessageOut)
def creat_order(request):
    user =User.objects.get(id=request.auth['pk'])
    orderd_x=Order.objects.create(ordered=True,user=user)
    user_items=Item.objects.filter(user=user).filter(ordered=False)
    orderd_x.items.add(*user_items)
    orderd_x.total=orderd_x.order_total
      user_items.update(ordered=True)
    orderd_x.save()

    return 200, {'detail':f'{orderd_x.total} تم الحجز السعر الكلي '}

@order_controller.get('cart', auth=GlobalAuth(), response={
    200: List[ItemOut],
    404: MessageOut
})
def view_cart(request):

    cart_items = Item.objects.filter(user=request.auth['pk'], ordered=False)

    if cart_items:
        return cart_items

    return 404, {'detail': 'السلة فارغة'}


