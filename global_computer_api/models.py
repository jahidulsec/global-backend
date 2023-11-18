from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()



# Create your models here.
# category
class Category(models.Model):
    slug = models.SlugField(max_length=255, null=True)
    title = models.CharField(max_length=255, db_index=True, unique=True)

    def __str__(self) -> str:
        return self.slug

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)







# brand
class Brand(models.Model):
    slug = models.SlugField(max_length=255, blank=True)
    title = models.CharField(max_length=255, db_index=True, unique=True)
    logo = models.ImageField(max_length=10000, null=True)

    def __str__(self) -> str:
        return self.title
    
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)



# sideMenu
class SideMenu(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    logo = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, null=True)
    query = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class SubSideMenu(models.Model):
    side_menu = models.ForeignKey(SideMenu, on_delete=models.CASCADE, related_name='sub_side_menu')
    slug = models.SlugField(max_length=255, null=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)



# product
class Product(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, db_index=True)
    side_menu = models.ForeignKey(SideMenu, on_delete=models.PROTECT, db_index=True, null=True) 
    model_name = models.SlugField(max_length=255, db_index=True, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_index=True)
    prev_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    emi_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    is_stock = models.BooleanField(default=False)
    sold_stock = models.IntegerField(default=0, blank=True)
    total_stock = models.IntegerField(default=0, blank=True)
    description = models.TextField(default=None, blank=True)
    featured = models.BooleanField(default=False, db_index=False)
    display_big = models.BooleanField(default=False, null=True, db_index=True)
    offered = models.BooleanField(default=False, db_index=False)
    offered_time = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            new_slug = "{brand}-{cat}-{model}".format(
                brand = self.brand, 
                cat = self.category,
                model = self.model_name
            )
            self.slug = slugify(new_slug)
        return super().save(*args, **kwargs)
    

# product Images
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # image = models.ImageField(upload_to='images/products/')
    image = models.CharField(max_length=255)
    

# key features
class KeyFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='key_features')
    field_name = models.CharField(max_length=255)
    field_description = models.CharField(max_length=255)




# specification
class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, related_name='specification')
    table_name = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.table_name


class SpecTable(models.Model):
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE, related_name='spec_table')
    field_name = models.CharField(max_length=255, db_index=True)
    field_description = models.CharField(max_length=255, db_index=True)




# reviews
class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  
    comment = models.TextField()
    stars = models.IntegerField(db_index=True)
    date = models.DateField()

    def __str__(self) -> str:
        return self.product.title
    
    

# slider
class Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    mini_text = models.CharField(max_length=255, null=True)
    mid_text = models.CharField(max_length=255, null=True)
    color = models.BooleanField(default=False)
    # image = models.ImageField(upload_to='images/slider')
    image = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.product.title
    

# banner
class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slogan = models.CharField(default=None, max_length=255)
    image = models.ImageField(upload_to='image/slider')
    color = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product.title
    


import datetime

# order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(db_index=True, null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateField(db_index=True)
    phone = PhoneNumberField(blank=True)
    street_address = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    division = models.CharField(max_length=255, null=True)
    order_note = models.TextField(null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True)

    def __str__(self) -> str:
        return self.user.username
    
    def generete_unique_key(self):
        last_order = Order.objects.all().order_by('id').last()

        unique_key = 0
        if (last_order != None):
            unique_key = int(last_order.slug[12:])


        if self.date[8:10] == '31' and unique_key != 0:
            unique_key = 0
        else:
            unique_key += 1

        return unique_key

    def save(self, *args, **kwargs):  # new

        if not self.slug:
            unique = self.generete_unique_key()
            new_slug = "INV-{year}{month}{date}{num}".format(
                year = self.date[0:4], 
                month = self.date[5:7],
                date = self.date[8:10],
                num = unique
            )
            self.slug = slugify(new_slug)
        return super().save(*args, **kwargs)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')



# newsteller
class Newsteller(models.Model):
    email = models.EmailField(unique=True, max_length=254)