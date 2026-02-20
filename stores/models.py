from django.db import models

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
    # person
    # total
    # created
    def __str__(self):
        pass

# ::::::::: CART PRODUCT :::::::::
class CartProduct(models.Model):

    def __str__(self):
        pass

# ::::::::: ORDER :::::::::
class Order(models.Model):

    def __str__(self):
        pass


# category - text
# products - title,reviews,price, discount price, instock,description, size (s,m,l,xl),color,Product Specifications,Material,Washing Instructions,Wearing,weight, image*6
#cart -  total, user
#cartproduct - cart, products, quantity,subtotal,amount
