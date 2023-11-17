from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.CategoryView.as_view()),
    path('category/<slug:slug>', views.SingleCategoryView.as_view()),
    path('brand/', views.BrandView.as_view()),
    path('brand/<slug:slug>', views.SingleBrandView.as_view()),
    path('side-menu/', views.SideMenuView.as_view()),
    path('side-menu/<slug:slug>', views.SingleSideMenuView.as_view()),
    path('product/', views.ProductView.as_view()),
    path('product/<slug:slug>', views.SingleProductView.as_view()),
    path('product-image/', views.ProductImagesView.as_view()),
    path('product-image/<int:pk>', views.SingleProductImagesView.as_view()),
    path('feature/', views.KeyFeatureView.as_view()),
    path('feature/<int:pk>', views.SingleKeyFeatureView.as_view()),
    path('single-feature/<int:pk>', views.SingleKeyFieldDelView.as_view()),
    path('specification/', views.SpecificationView.as_view()),
    path('specification/<int:pk>', views.SingleSpecificationView.as_view()),
    path('spec-table/<int:pk>', views.SingleSpecTableView.as_view()),
    path('spec/<int:pk>', views.SingleSpecView.as_view()),
    path('slider/', views.SliderView.as_view()),
    path('slider/<int:pk>', views.SingleSliderView.as_view()),
    path('banner/', views.BannerView.as_view()),
    path('banner/<int:pk>', views.SingleBannerView.as_view()),
    path('review/', views.ReviewView.as_view()),
    path('review/<int:pk>', views.SingleReviewView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('order/<int:pk>', views.SingleOrderView.as_view()),
    path('single-order/<int:pk>', views.SingleOrderItemView.as_view()),
    path('newsletter/', views.NewslellerViews.as_view()),
] 


