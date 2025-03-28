from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Product, OrderEntry, Category

# ✅ Form quản lý sản phẩm cho admin
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'unit', 'category']
        labels = {
            'name': 'Product Name',
            'unit': 'Unit',
            'category': 'Category',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-select'}),      # ✅ Dropdown
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

# ✅ Form đặt hàng cho nhân viên
class ProductStaffForm(forms.ModelForm):
    order_quantity = forms.IntegerField(min_value=1, required=True)

    class Meta:
        model = OrderEntry
        fields = ['order_quantity']

# ✅ Form đăng nhập cho staff (có Bootstrap)
class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# ✅ Form tạo nhân viên mới (admin)
class StaffCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Username',
        }
        help_texts = {
            'username': '',  # ✅ Xoá hint mặc định của Django
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        if commit:
            user.save()
        return user

# ✅ Form upload file Excel
class ProductImportForm(forms.Form):
    excel_file = forms.FileField(label='Choose Excel file (.xlsx)')
