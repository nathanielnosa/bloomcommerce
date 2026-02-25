from django.db import models
from users.models import Profile
import secrets
from .paystack import Paystack

# ::::::::: CATEGORY :::::::::
class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="category", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ::::::::: PRODUCT :::::::::
SIZE_CHOICE=(
    ('s','s'),
    ('m','m'),
    ('l','l'),
    ('xl','xl'),
)
class Products(models.Model):
    title = models.CharField(max_length=255,null=True)
    description = models.TextField(null=True)
    price = models.BigIntegerField(null=True)
    discount_price = models.BigIntegerField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    main = models.ImageField(upload_to="products",null=True)
    image1 = models.ImageField(upload_to="products",null=True,blank=True)
    image2 = models.ImageField(upload_to="products",null=True,blank=True)
    image3 = models.ImageField(upload_to="products",null=True,blank=True)
    image4 = models.ImageField(upload_to="products",null=True,blank=True)
    size = models.CharField(max_length=50,choices=SIZE_CHOICE,null=True)
    color = models.CharField(max_length=50,null=True)
    reviews = models.TextField(null= True, blank=True)
    rating = models.IntegerField(null= True, blank=True)
    in_stock = models.IntegerField(null=True)
    is_available = models.IntegerField(default=True,null=True)
    product_specification = models.TextField(null= True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.title

# ::::::::: CART :::::::::
class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    total = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return str(self.total)

# ::::::::: CART PRODUCT :::::::::
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    subtotal = models.PositiveIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return f'{self.cart.id} - {self.product.title}({self.quantity})'

# ::::::::: ORDER :::::::::
ORDER_STATUS=(
    ('pending','pending'),
    ('completed','completed'),
    ('canceled','canceled'),
)
PAYMENT_METHOD=(
    ('paystack','paystack'),
    ('stripe','stripe'),
    ('paypal','paypal'),
)
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    order_by = models.CharField(max_length=255, null=True)
    shipping_address = models.TextField(null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=50,null=True)
    subtotal = models.BigIntegerField(null=True)
    amount = models.BigIntegerField(null=True)
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS ,default='pending')
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD ,default='paystack')
    payment_completed = models.BooleanField(default=False)
    ref = models.CharField(max_length=255, unique=True, null=True)

    def __str__(self):
        return f'OrderId-{self.id} - {self.amount}'
    
    def save(self, *args,**kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref
        super().save(*args,**kwargs)
    
    def amount_value(self)->int:
        self.amount * 100
    
    # verify payment
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref)
        if status and result.get("status") == "success":
            if result['amount'] / 100 == self.amount:
                self.payment_completed = True
                self.save()
                return True
            if self.payment_completed == True:
                self.cart = None
                self.save()
                return True
            return False
        return False
