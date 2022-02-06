


from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models

from config.utils.models import Entity

User = get_user_model()


class ProductManager(models.Manager):
    def select(self):
        return self.get_queryset().select_related('category','product','order')


class Product(Entity):
    name = models.CharField('name', max_length=255)
    description = models.TextField('description', null=True, blank=True)
    size = models.CharField('size',  max_length=6, default="-")
    qty = models.IntegerField('qty')
    cost = models.FloatField('cost',)
    price = models.FloatField('price',)
    discounted_price = models.FloatField('discounted price',default=0)

    category = models.ForeignKey('commerce.Category', verbose_name='category', related_name='product',
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    is_featured = models.BooleanField('is featured')
    is_active = models.BooleanField('is active')

    def __str__(self):
        return self.name

    objects = ProductManager()


class Order(Entity):
    user = models.ForeignKey(User, verbose_name='user', related_name='order', null=True, blank=True,
                             on_delete=models.SET_NULL)
    total = models.DecimalField('total', blank=True, null=True, max_digits=1000, decimal_places=0)
    #status = models.ForeignKey('commerce.OrderStatus', verbose_name='status', related_name='orders',on_delete=models.SET)
    #note = models.CharField('note', null=True, blank=True, max_length=255)
    #ref_code = models.CharField('ref code', max_length=255)
    ordered = models.BooleanField('ordered')
    items = models.ManyToManyField('commerce.Item', verbose_name='items', related_name='order')
    created = models.DateField(editable=False, auto_now_add=True)
    def __str__(self):
        return f'{self.user} + {self.total}'

    @property
    def order_total(self):
        order_total = sum(
            i.product.discounted_price * i.item_qty for i in self.items.all()
        )

        return order_total


class Item(Entity):
    """
    Product can live alone in the system, while
    Item can only live within an order
    """
    user = models.ForeignKey(User, verbose_name='user', related_name='item', null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey('commerce.Product', verbose_name='product', null=True, blank=True,
                                on_delete=models.SET_NULL)
    item_qty = models.IntegerField('item_qty')
    ordered = models.BooleanField('ordered')
    created = models.DateField(editable=False, auto_now_add=True)
    def __str__(self):
        return self.product.name


class Category(Entity):
    parent = models.ForeignKey('self', verbose_name='parent', related_name='children',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    name = models.CharField('name', max_length=255)
    description = models.TextField('description')
    image = models.ImageField('image', upload_to='category/')
    is_active = models.BooleanField('is active')

    created = models.DateField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        if self.parent:
            return f'-   {self.name}'
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'


class ProductImage(Entity):
    image = models.ImageField('image', upload_to='product/')
    is_default_image = models.BooleanField('is default image')
    product = models.ForeignKey('commerce.Product', verbose_name='product', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)



