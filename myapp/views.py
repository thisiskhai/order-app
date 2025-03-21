from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime
import openpyxl
from .forms import ProductImportForm


from .models import Product, OrderEntry
from .forms import ProductAdminForm, ProductStaffForm, StaffCreateForm

# =======================
# ✅ Kiểm tra quyền hạn
# =======================
def is_admin(user):
    return user.is_superuser

def is_staff_user(user):
    return user.is_staff and not user.is_superuser

# =======================
# ✅ Trang danh sách sản phẩm (User thường & Staff)
# =======================
@login_required
def product_list(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.is_staff:
        return redirect('staff_product_list')
    else:
        return redirect('staff_login')

# =======================
# ✅ CRUD sản phẩm (Admin)
# =======================
@login_required
@user_passes_test(is_admin)
def admin_product_list(request):
    products = Product.objects.all()
    form = ProductAdminForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Sản phẩm đã được thêm.")
        return redirect('admin_product_list')

    return render(request, 'admin_product_list.html', {'products': products, 'form': form})


@login_required
@user_passes_test(lambda user: user.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductAdminForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật sản phẩm thành công!")
            return redirect('all_products')
    else:
        form = ProductAdminForm(instance=product)

    return render(request, 'product_form.html', {'form': form, 'product': product})


@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Sản phẩm đã bị xoá.")
    return redirect('admin_product_list')


# =======================
# ✅ Đăng nhập / đăng xuất staff
# =======================
def staff_login(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user)

            # ✅ Kiểm tra nếu có `next` URL
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            # ✅ Chuyển hướng dựa trên quyền
            return redirect('admin_dashboard' if user.is_superuser else 'staff_product_list')

        else:
            messages.error(request, "Bạn không có quyền truy cập.")

    return render(request, 'staff_login.html', {'form': form})

@login_required
def staff_logout(request):
    logout(request)
    return redirect('staff_login')


# =======================
# ✅ Dashboard Admin (Thêm nhân viên + Lọc đơn hàng)
# =======================
@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_dashboard(request):
    staff_list = User.objects.filter(is_staff=True, is_superuser=False)
    staff_orders = [
        {
            'staff': staff,
            'total_quantity': sum(entry.order_quantity for entry in OrderEntry.objects.filter(staff=staff))
        }
        for staff in staff_list
    ]

    staff_form = StaffCreateForm(request.POST or None, prefix='staff')
    product_form = ProductAdminForm(request.POST or None, prefix='product')
    import_form = ProductImportForm(request.POST or None, request.FILES or None, prefix='import')

    # Thêm nhân viên
    if request.method == 'POST' and 'add_staff' in request.POST:
        if staff_form.is_valid():
            staff_form.save()
            messages.success(request, "Đã thêm nhân viên mới.")
            return redirect('admin_dashboard')

    # Thêm sản phẩm thủ công
    if request.method == 'POST' and 'add_product' in request.POST:
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Đã thêm sản phẩm mới.")
            return redirect('admin_dashboard')

    # Thêm sản phẩm từ Excel
    if request.method == 'POST' and 'import_excel' in request.POST:
        if import_form.is_valid():
            excel_file = import_form.cleaned_data['excel_file']
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            added_products = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                name, available_at_store, order_quantity, unit = row
                Product.objects.create(
                    name=name,
                    available_at_store=bool(available_at_store),
                    order_quantity=int(order_quantity),
                    unit=unit
                )
                added_products += 1

            messages.success(request, f"Đã thêm {added_products} sản phẩm từ file Excel.")
            return redirect('admin_dashboard')
    products = Product.objects.all().order_by('-created_at')  # mới nhất ở trên cùng

    return render(request, 'admin_dashboard.html', {
        'staff_orders': staff_orders,
        'staff_form': staff_form,
        'product_form': product_form,
        'import_form': import_form,
        'products': products,
    })


# =======================
# ✅ Xoá nhân viên (Admin)
# =======================
@login_required
@user_passes_test(is_admin)
def delete_staff(request, staff_id):
    staff = get_object_or_404(User, pk=staff_id, is_staff=True, is_superuser=False)
    staff.delete()
    messages.success(request, f"Đã xoá nhân viên {staff.username}.")
    return redirect('admin_dashboard')


# =======================
# ✅ Nhân viên nhập số lượng sản phẩm
# =======================
@login_required
@user_passes_test(lambda user: user.is_staff and not user.is_superuser)
def staff_product_list(request):
    products = Product.objects.all()
    staff_orders = {entry.product.id: entry for entry in OrderEntry.objects.filter(staff=request.user)}

    if request.method == 'POST':
        for product in products:
            quantity = request.POST.get(f'quantity_{product.id}')
            if quantity:
                try:
                    quantity = int(quantity)
                    if quantity > 0:
                        if product.id in staff_orders:
                            order = staff_orders[product.id]
                            order.order_quantity = quantity
                            order.save()
                            messages.success(request, f"Đã cập nhật {quantity} x {product.name}.")
                        else:
                            OrderEntry.objects.create(
                                product=product,
                                staff=request.user,
                                order_quantity=quantity
                            )
                            messages.success(request, f"Đã đặt {quantity} x {product.name}.")
                    else:
                        messages.error(request, "Số lượng phải lớn hơn 0.")
                except ValueError:
                    messages.error(request, "Số lượng phải là số.")

        return redirect('staff_product_list')

    return render(request, 'staff_product_list.html', {
        'products': products,
        'staff_orders': staff_orders
    })



# =======================
# ✅ Xem đơn hàng của từng nhân viên
# =======================
@login_required
@user_passes_test(is_admin)
def staff_order_detail(request, staff_id):
    staff = get_object_or_404(User, pk=staff_id, is_staff=True, is_superuser=False)
    entries = OrderEntry.objects.filter(staff=staff).select_related('product').order_by('-created_at')
    total_quantity = sum(entry.order_quantity for entry in entries)

    return render(request, 'staff_order_detail.html', {
        'staff': staff,
        'entries': entries,
        'total_quantity': total_quantity
    })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def manage_products(request):
    products = Product.objects.all()
    product_form = ProductAdminForm(request.POST or None, prefix='product')
    import_form = ProductImportForm(request.POST or None, request.FILES or None, prefix='import')

    # Thêm sản phẩm thủ công
    if request.method == 'POST' and 'add_product' in request.POST:
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Đã thêm sản phẩm mới.")
            return redirect('manage_products')

    # Import sản phẩm từ Excel
    if request.method == 'POST' and 'import_excel' in request.POST:
        if import_form.is_valid():
            excel_file = import_form.cleaned_data['excel_file']
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
            added_products = 0

            for row in sheet.iter_rows(min_row=2, values_only=True):
                name, available_at_store, order_quantity, unit = row
                Product.objects.create(
                    name=name,
                    available_at_store=bool(available_at_store),
                    order_quantity=int(order_quantity),
                    unit=unit
                )
                added_products += 1

            messages.success(request, f"Đã thêm {added_products} sản phẩm từ file Excel.")
            return redirect('manage_products')

    return render(request, 'manage_products.html', {
        'products': products,
        'product_form': product_form,
        'import_form': import_form,
    })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def all_products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'all_products.html', {'products': products})
