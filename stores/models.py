from django.db import models

# ::::::::: CATEGORY :::::::::
class Category(models.Model):

    def __str__(self):
        pass

# ::::::::: PRODUCT :::::::::
class Products(models.Model):

    def __str__(self):
        pass

# ::::::::: CART :::::::::
class Cart(models.Model):

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
