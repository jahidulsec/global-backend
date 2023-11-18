from rest_framework import serializers
from .models import Newsteller, SideMenu, SubSideMenu, Category, Brand, Product, Reviews, Order, OrderItem, Slider, Banner, ProductImage, KeyFeature, Specification, SpecTable
from django.db.models import Avg, Count
from global_computer import settings


# serializers


# brand
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'slug', 'title', 'logo']





# category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']



# side menu
class SubSideMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSideMenu
        fields = ['id', 'slug', 'name']


class SideMenuSerializer(serializers.ModelSerializer):
    
    sub_side_menu = SubSideMenuSerializer(read_only=True, many=True)
    uploaded_submenu = serializers.ListField(
        child = serializers.CharField(max_length = 255), 
        write_only=True
    )

    class Meta:
        model = SideMenu
        fields = ['id', 'title', 'slug', 'logo', 'query', 'sub_side_menu', 'uploaded_submenu']

    def create(self, validated_data):
        return super().create(validated_data)

# product image
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'id', 
            'product', 
            'image', 
        ]




# key features
class KeyFeatureSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = KeyFeature
        fields = ['id', 'field_name', 'field_description', 'product_id', 'product']



# specification
class SpecTableSerializer(serializers.ModelSerializer):
    specification = serializers.StringRelatedField()

    class Meta:
        model = SpecTable
        fields = ['id', 'specification', 'field_name', 'field_description']


class SpecificationSerializer(serializers.ModelSerializer):
    spec_table = SpecTableSerializer(many=True, read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Specification
        fields = ['id', 'product', 'table_name', 'spec_table']


# review


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField()
    average_stars = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = ['id', 'product', 'product_id', 'user', 'count_review',
                  'user_id', 'average_stars','comment', 'stars', 'date']
        
    def get_average_stars(self, obj):
        average = Reviews.objects.filter(product_id=obj.product_id).aggregate(Avg('stars')).get('stars__avg')
        if average == None:
            return 0
        return average

    def get_count_review(self, obj):
        count = Reviews.objects.filter(product_id=obj.product_id).aggregate(Count('user')).get('user__count')
        if count == None:
            return 0
        return count
        


# product
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    brand_id = serializers.IntegerField(write_only=True)
    key_features = KeyFeatureSerializer(many=True, read_only=True)

    side_menu = SideMenuSerializer(read_only=True)
    side_menu_id = serializers.IntegerField(write_only=True)

    average_stars = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()

    specification = SpecificationSerializer(many=True, read_only=True)

    images = ProductImageSerializer(many=True, read_only=True)
    # uploaded_images = serializers.ListField(
    #     child = serializers.ImageField(max_length = 1000000, allow_empty_file=False),
    #     write_only=True
    # )
    
    uploaded_images = serializers.ListField(
        child = serializers.CharField(max_length = 1000000),
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
                    'id', 'title', 'slug', 'category', 'category_id', 'brand', 'brand_id',
                    'model_name', 'price', 'prev_price', 'emi_price', 'average_stars', 'count_review',
                    'discount', 'is_stock', 'sold_stock', 'total_stock', 'description',
                    "side_menu", "side_menu_id",
                    'featured', 'offered', 'offered_time', 'display_big',
                    'images', 'uploaded_images', 'key_features', 'specification'
                ]
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            newProductImage = ProductImage.objects.create(product=product, image=image)
        
        return product
    
    def get_average_stars(self, obj):
        average = Reviews.objects.filter(product_id=obj.id).aggregate(Avg('stars')).get('stars__avg')
        if average == None:
            return 0
        return average

    def get_count_review(self, obj):
        count = Reviews.objects.filter(product_id=obj.id).aggregate(Count('user')).get('user__count')
        if count == None:
            return 0
        return count




class SingleProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    brand_id = serializers.IntegerField()
    side_menu = SideMenuSerializer(read_only=True)
    side_menu_id = serializers.IntegerField()
    key_features = KeyFeatureSerializer(many=True, read_only=True)

    images = ProductImageSerializer(many=True, read_only=True)
    # uploaded_images = serializers.ListField(
    #     child = serializers.ImageField(max_length = 1000000, allow_empty_file=False),
    #     write_only=True
    # )

    uploaded_images = serializers.ListField(
        child = serializers.CharField(max_length = 1000000),
        write_only=True
    )

    specification = SpecificationSerializer(many=True, read_only=True)

    reviews = ReviewSerializer(read_only=True, many=True)
    average_stars = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = [
                    'id', 'title', 'slug', 'category', 'category_id','brand', 'brand_id',
                    'side_menu', 'side_menu_id',
                    'model_name', 'price', 'prev_price', 'emi_price', 'display_big',
                    'discount', 'is_stock', 'sold_stock', 'total_stock', 'description',
                    'featured', 'offered', 'offered_time', 'average_stars', 'count_review',
                    'images', 'uploaded_images', 'key_features',
                    'specification', 'reviews'
                ]
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            newProductImage = ProductImage.objects.create(product=product, image=image)
        
        return product
    
    def get_average_stars(self, obj):
        average = Reviews.objects.filter(product_id=obj.id).aggregate(Avg('stars')).get('stars__avg')
        if average == None:
            return 0
        return average

    def get_count_review(self, obj):
        count = Reviews.objects.filter(product_id=obj.id).aggregate(Count('user')).get('user__count')
        if count == None:
            return 0
        return count
    
   


# single image add
class SingleProductImageSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    image = serializers.StringRelatedField(read_only=True)
    # uploaded_images = serializers.ListField(
    #     child = serializers.ImageField(max_length = 1000000, allow_empty_file=False),
    #     write_only=True
    # )
    uploaded_images = serializers.ListField(
        child = serializers.CharField(max_length = 1000000),
        write_only=True
    )
    class Meta:
        model = ProductImage
        fields = ['id',  'product_id', 'image', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.get(pk=validated_data['product_id'])
        for image in uploaded_images:
            newProductImage = ProductImage.objects.create(product=product, image=image)
            newProductImage.save()
        
        return newProductImage




# slider
class SliderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    category = serializers.StringRelatedField(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Slider
        fields = ['id', 'product', 'category', 'category_id', 'mini_text', 'mid_text', 'color', 'image', 'product_id']


# banner
class BannerSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Banner
        fields = ['id', 'product', 'title', 'subtitle', 'slogan', 'color', 'image', 'product_id']




# order
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'unit_price', 'quantity', 'price',]



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    user_id = serializers.IntegerField()
    orders = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order 
        fields = ['id', 'user', 'user_id', 'slug', 'status', 'total', 'date', 'phone', 
                  'street_address', 'district', 'division', 'order_note', 
                  'payment_method', 'orders']
        
        

class SingleOrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    user_id = serializers.IntegerField()
    orders = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order 
        fields = ['id', 'user', 'user_id', 'slug', 'status', 'total', 'date', 'phone', 
                  'street_address', 'district', 'division', 'order_note', 
                  'payment_method', 'orders']




# newsteller
class NewstellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsteller
        fields = ['id', 'email']
