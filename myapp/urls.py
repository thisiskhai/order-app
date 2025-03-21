from django.urls import path
from .views import (
    admin_product_list,
    all_products,
    product_list,
    product_update,
    product_delete,
    staff_login,
    staff_logout,
    staff_product_list,
    admin_dashboard,
    delete_staff,
    staff_order_detail,
    manage_products, 
)

urlpatterns = [
    # ✅ Trang chính mặc định cho staff sau khi login
    path('', product_list, name='product_list'),

    # ✅ CRUD sản phẩm (chỉ admin, tránh trùng với /admin mặc định của Django)
    path('dashboard/products/', admin_product_list, name='admin_product_list'),
    path('dashboard/products/edit/<int:pk>/', product_update, name='product_update'),
    path('dashboard/products/delete/<int:pk>/', product_delete, name='product_delete'),

    # ✅ Đăng nhập / đăng xuất nhân viên
    path('staff/login/', staff_login, name='staff_login'),
    path('staff/logout/', staff_logout, name='staff_logout'),

    # ✅ Trang nhập sản phẩm cho nhân viên
    path('staff/products/', staff_product_list, name='staff_product_list'),

    # ✅ Trang Dashboard chính (admin)
    path('dashboard/', admin_dashboard, name='admin_dashboard'),

    # ✅ Quản lý nhân viên (admin)
    path('dashboard/staff/<int:staff_id>/', staff_order_detail, name='staff_order_detail'),
    path('dashboard/staff/delete/<int:staff_id>/', delete_staff, name='delete_staff'),

    # ✅ Quản lý sản phẩm nâng cao (thêm mới, import sản phẩm...)
    path('dashboard/manage-products/', manage_products, name='manage_products'),

    # ✅ Xem tất cả sản phẩm (admin)
    path('dashboard/all-products/', all_products, name='all_products'),
]
