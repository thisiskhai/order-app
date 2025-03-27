from django.urls import path
from .views import (
    admin_batch_detail,
    admin_order_batches,
    admin_product_list,
    all_products,
    product_list,
    product_update,
    product_delete,
    staff_login,
    staff_logout,
    staff_order_history,
    staff_product_list,
    admin_dashboard,
    delete_staff,
    staff_order_detail,
    manage_products, 
    toggle_order_status,
)

urlpatterns = [
    path('', product_list, name='product_list'),

    # ✅ CRUD sản phẩm
    path('dashboard/products/', admin_product_list, name='admin_product_list'),
    path('dashboard/products/edit/<uuid:uuid>/', product_update, name='product_update'),
    path('dashboard/products/delete/<uuid:uuid>/', product_delete, name='product_delete'),

    # ✅ Staff login/logout
    path('staff/login/', staff_login, name='staff_login'),
    path('staff/logout/', staff_logout, name='staff_logout'),
    path('staff/order-history/', staff_order_history, name='staff_order_history'),
    path('staff/products/', staff_product_list, name='staff_product_list'),

    # ✅ Dashboard admin
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/staff/<int:staff_id>/orders/', admin_order_batches, name='admin_order_batches'),
    path('dashboard/staff/<int:staff_id>/orders/<str:timestamp>/', admin_batch_detail, name='admin_batch_detail'),
    path('dashboard/staff/<int:staff_id>/batch/<str:timestamp>/', admin_batch_detail, name='admin_batch_detail'),
    path('dashboard/staff/<int:staff_id>/', staff_order_detail, name='staff_order_detail'),
    path('dashboard/staff/delete/<int:staff_id>/', delete_staff, name='delete_staff'),

    # ✅ Product management
    path('dashboard/manage-products/', manage_products, name='manage_products'),
    path('dashboard/all-products/', all_products, name='all_products'),
    path('dashboard/toggle-order-status/<int:order_id>/', toggle_order_status, name='toggle_order_status'),
]
