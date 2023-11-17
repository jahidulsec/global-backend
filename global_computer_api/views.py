from typing import Any
from django.shortcuts import render
from .models import Newsteller, Category, Banner, Product, Slider, Order, OrderItem, Brand, KeyFeature, SpecTable, Specification, Reviews, SideMenu, ProductImage
from django.contrib.auth import  get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SingleOrderSerializer, NewstellerSerializer, ReviewSerializer, CategorySerializer, BrandSerializer, BannerSerializer, ProductSerializer, KeyFeatureSerializer, SliderSerializer, OrderItemSerializer, OrderSerializer, SpecificationSerializer, SpecTableSerializer, SingleProductSerializer, ReviewSerializer, SideMenuSerializer, SingleProductImageSerializer
from .permissions import IsManagerOnly
from .paginations import SetPagination
from django_filters.rest_framework import DjangoFilterBackend, Filter
from rest_framework.response import Response
from rest_framework import filters
from .filters import ProductFilter
from django.contrib.auth import get_user_model
import os
import datetime


User = get_user_model()

currentDate = datetime.datetime.now().date()

# Create your views here.

# category 
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['slug']
    pagination_class = SetPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'



    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



# Brand
class BrandView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.OrderingFilter]
    pagination_class = SetPagination


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class SingleBrandView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def put(self, request, slug, *args, **kwargs):
        brand = Brand.objects.get(slug=slug)
        if brand.logo:
            os.remove(brand.logo.path)
        return super().put(request, *args, **kwargs)
    
    def delete(self, request, slug, *args, **kwargs):
        brand = Brand.objects.get(slug=slug)
        if brand.logo:
            os.remove(brand.logo.path)
        return super().delete(request, *args, **kwargs)

    

# side menu
class SideMenuView(generics.ListCreateAPIView):
    queryset = SideMenu.objects.all()
    serializer_class = SideMenuSerializer
    filter_backends = [filters.OrderingFilter]
    pagination_class = SetPagination


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsManagerOnly]
        return [permission() for permission in permission_classes]


class SingleSideMenuView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SideMenu.objects.all()
    serializer_class = SideMenuSerializer
    lookup_field = 'slug'


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    


# product 
class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter  # model__field
    search_fields = ['title']
    

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

   

class SingleProductView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = SingleProductSerializer
    pagination_class = SetPagination
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


# product images
class ProductImagesView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = SingleProductImageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    

class SingleProductImagesView(generics.DestroyAPIView): 
    queryset = ProductImage.objects.all()
    serializer_class = SingleProductImageSerializer

    def delete(self, request, pk, *args, **kwargs):
        product_image = ProductImage.objects.get(pk=pk)
        if product_image.image :
            os.remove(product_image.image.path)
        return super().delete(request, *args, **kwargs)


# key features
class KeyFeatureView(generics.ListCreateAPIView):
    queryset = KeyFeature.objects.all()
    serializer_class = KeyFeatureSerializer


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if (len(data) == 0):
            return Response({"status":"enter required fields"}, 400)
        feature = KeyFeature(
            product_id = data['product_id'],
            field_name = data['field_name'],
            field_description = data['field_description']
        )
        feature.save()


        return Response({'status': 'Features has been added.'}, 201) 
    

class SingleKeyFeatureView(generics.RetrieveUpdateDestroyAPIView):
    queryset = KeyFeature.objects.all()
    serializer_class = KeyFeatureSerializer


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def retrieve(self, request, pk, *args, **kwargs):
        feature = KeyFeature.objects.filter(product_id=pk)
        if (len(feature) == 0):
            return Response({"status": "No data found!"}, 404)
        serialized_data = KeyFeatureSerializer(feature, many=True)
        return Response(serialized_data.data, 200)


    def update(self, request, pk, *args, **kwargs):
        feature = KeyFeature.objects.filter(product_id=pk)
        if (len(feature) == 0):
            return Response({"status": "No data found!"}, 404)

        data = request.data.copy()
        if (len(data) != len(feature)):
            return Response({"status": "add required fields!"}, 404)   

        for idx in range(len(feature)):
            if (feature[idx].field_name != data[idx]["field_name"]):
                feature[idx].field_name = data[idx]["field_name"]
            if (feature[idx].field_description != data[idx]["field_description"]):
                feature[idx].field_description = data[idx]["field_description"]

        for item in feature:
            item.save()

        serialized_data = KeyFeatureSerializer(feature, many=True)
        return Response(serialized_data.data, 200)


    def destroy(self, request, pk, *args, **kwargs):
        feature = KeyFeature.objects.filter(product_id=pk)
        if (len(feature) == 0):
            return Response({"status": "No data found to delete!"}, 404)
        feature.delete()
        return Response({"status": "features has been deleted!"}, 200)
    

class SingleKeyFieldDelView(generics.DestroyAPIView):
    queryset = KeyFeature.objects.all()
    serializer_class = KeyFeatureSerializer
    permission_classes = [IsAdminUser]



# specification
class SpecificationView(generics.ListCreateAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if (len(data) == 0):
            return Response({'message': 'Add required fields'}, 400)
        product = Product.objects.get(id=data['product_id'])

        if (len(data['tables']) == 0):
            return Response({'detail': 'enter required fields!'}, 400)

        for item in data["tables"]:
            if (len(item['table_name']) == 0):
                return Response({'table_name': 'table name required!'}, 400)
            specs = Specification(
                product = product,
                table_name = item['table_name']
            )
            specs.save()
        
            for i in item['fields']:
                if (len(i['field_name']) == 0):
                    return Response({'field_name': 'field name required!'}, 400)
                
                if (len(i['field_description']) == 0):
                    return Response({'field_description': 'field name required!'}, 400)
                
                table = SpecTable (
                    specification= specs,
                    field_name = i['field_name'],
                    field_description = i['field_description']
                )
                table.save()

        return Response('Ok', 201)


class SingleSpecificationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer


    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


    def retrieve(self, request, pk, *args, **kwargs):
        specification = Specification.objects.filter(product_id=pk)
        if(len(specification)==0):
            return Response({"status": "Not found!"}, 404)
        
        data = SpecificationSerializer(specification, many=True)
        return Response(data.data, 200)
    

    def update(self, request, pk, *args, **kwargs):
        specification = Specification.objects.filter(product_id=pk)
        if(len(specification)==0):
            return Response({"status": "Not found!"}, 404)
        
        data = request.data.copy()


        if (len(data) != len(specification)):
            return Response({"status": "add required fields!"}, 404)
        
        for idx, item in enumerate(specification):
            spec_table = SpecTable.objects.filter(specification_id = item.id)
            if (len(data[idx]['table_name']) == 0):
                return Response({'table_name': 'table name required!'}, 400)
            item.table_name = data[idx]["table_name"]  
            item.save()  

            spec_table_data = data[idx]["spec_table"]

            for i, value in enumerate(spec_table):
                if (len(value[i]['field_name']) == 0):
                    return Response({'table_name': 'field name required!'}, 400)
                value.field_name = spec_table_data[i]["field_name"]

                if (len(value[i]['field_description']) == 0):
                    return Response({'table_name': 'field description required!'}, 400)
                value.field_description = spec_table_data[i]["field_description"]
                value.save()

        return Response({'status': 'update'},200)


    def destroy(self, request, pk, *args, **kwargs):
        specification = Specification.objects.filter(product_id=pk)
        if(len(specification)==0):
            return Response({"status": "Not found!"}, 404)
        specification.delete()
        return Response({"status": "Table has been deleted!"}, 200)
    

class SingleSpecTableView(generics.RetrieveDestroyAPIView):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



class SingleSpecView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpecTable.objects.all()
    serializer_class = SpecTableSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


# slider
class SliderView(generics.ListCreateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    


class SingleSliderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def put(self, request, pk, *args, **kwargs):
        slider = Slider.objects.get(pk=pk)
        if len(slider.image) > 0 :
            os.remove(slider.image.path)
        return super().put(request, *args, **kwargs)
    
    def delete(self, request, pk, *args, **kwargs):
        slider = Slider.objects.get(pk=pk)
        if len(slider.image) > 0 :
            os.remove(slider.image.path)
        return super().delete(request, *args, **kwargs)



#  banner
class BannerView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    

class SingleBannerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



# Reviews
class ReviewView(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product__slug']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user_id"] = self.request.user.id
        
        exist_review = Reviews.objects.filter(user_id = self.request.user.id, product_id = data["product_id"])
        if exist_review.exists():
            return Response({'status': 'You already have a review on this product!'}, 400)


        serialized_review = ReviewSerializer(data=data)

        if (serialized_review.is_valid()):
            serialized_review.save()
            return Response(serialized_review.data, 201)

        return Response({"status": "add required fields!"}, 400)




class SingleReviewView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer


    def get_queryset(self):
        return Reviews.objects.all().filter(user=self.request.user)
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    


    def delete(self, request, pk, *args, **kwargs):
        reviews = Reviews.objects.all().filter(user=self.request.user)
        if (len(reviews) == 0):
            return Response({"status": "no item to delete"})
        reviews.get(id=pk).delete()
        return Response("ok")


# order
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['status']
    pagination_class = SetPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Manager').exists(): #manager
            return Order.objects.all()
        return Order.objects.all().filter(user=self.request.user)
    

        
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        order_items = data["orders"]

        # try:
        order = Order(
            user_id = self.request.user.id,
            status = False,
            total = 0,
            date = data["date"],
            street_address = data["street_address"],
            district = data["district"],
            division = data["division"],
            phone = data["phone"],
            payment_method = data["payment_method"],
        )
        order.save()
        # except:
        #     return Response({'status': 'Add required fields!'}, 400)
        
        result_total = 0

        for item in order_items:
            product = Product.objects.get(id=item["product_id"])
            result_total += (int(product.price) * int(item["quantity"]))
            order_item = OrderItem(
                order_id = order.id,
                product_id = product.id,
                quantity = item["quantity"],
                unit_price = product.price,
                price = int(product.price) * int(item["quantity"])
            )
            order_item.save()

        order.total = result_total
        order.save()

        return Response({"status": "order has been added", "slug": order.slug}, 201)




class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = SingleOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Manager').exists(): #manager
            return Order.objects.all()
        return Order.objects.all().filter(user=self.request.user)


# single order item
class SingleOrderItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]



# newsteller
class NewslellerViews(generics.ListCreateAPIView):
    queryset = Newsteller.objects.all()
    serializer_class = NewstellerSerializer
