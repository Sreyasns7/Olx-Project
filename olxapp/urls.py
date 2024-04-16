from django.urls import path
from .import views  



urlpatterns = [
    path('',views.index,name='index'),
    path('login', views.main_login, name='login'),
    path('register/', views.registration_view, name='registration_view'),
    path('approve_disapprove_users',views.approve_disapprove_users,name='approve_disapprove_users'),
    path('user_details',views.user_details,name='user_details'),
    path('delete_user_details',views.delete_user_details,name='delete_user_details'),
    path('logout',views.logout,name='logout'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('edit_user_details/<int:user_id>/', views.edit_user_details, name='edit_user_details'),
    path('add_categories/', views.add_categories, name='add_categories'),
    path('product_categories/', views.product_categories, name='product_categories'),
    path('subcategories_by_category/<int:category_id>/', views.subcategories_by_category, name='subcategories_by_category'),
    path('products_by_subcategory/<int:subcategory_id>/', views.products_by_subcategory, name='products_by_subcategory'),
    path('add_product/', views.add_product, name='add_product'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('user/products/', views.user_products, name='user_products'),
    path('user/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('user/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('messaging/<int:user_id>/', views.messaging, name='messaging'),
    path('send_message/<int:user_id>/', views.send_message, name='send_message'),
    path('user_list/', views.user_list, name='user_list'),

    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    path('cart_remove/<int:pk>',views.cart_remove,name='cart_remove'),
    path('cart_view',views.cart_view,name='cart_view'),
    path('increment/<int:pk>',views.increment,name='increment'),
    path('decrement/<int:pk>',views.decrement,name='decrement'),
    # path('checkout',views.checkout,name='checkout'),
    path('checkout_process',views.checkout_process,name='checkout_process'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('user_orders/', views.user_orders, name='user_orders'),

    path('products/', views.product_list, name='product_list'),
    path('products/delete/<int:product_id>/', views.user_delete_product, name='user_delete_product'),

    path('order-list/', views.order_list, name='order_list'),
    path('feedback-list/', views.feedback_list, name='feedback_list'),
    path('user/<int:user_id>/', views.view_user_details, name='view_user_details'),
    path('search/', views.product_search, name='product_search'),
    path('seller/orders/', views.seller_order_details, name='seller_order_details'),


]









    
