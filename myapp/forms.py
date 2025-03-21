from django import forms
from .models import Product, OrderEntry
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# ✅ Form đầy đủ cho admin (superuser)
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'available_at_store', 'unit']  # ❌ Loại bỏ 'order_quantity'

# ✅ Form chỉ nhập số lượng cho nhân viên (staff)
class ProductStaffForm(forms.ModelForm):
    order_quantity = forms.IntegerField(min_value=1, required=True)

    class Meta:
        model = OrderEntry  # ✅ Chuyển sang `OrderEntry` thay vì `Product`
        fields = ['order_quantity']

class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(label="Tên đăng nhập", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mật khẩu", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class StaffCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']  # ❌ Không có 'email'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        if commit:
            user.save()
        return user

class ProductImportForm(forms.Form):
    excel_file = forms.FileField(label='Chọn file Excel (.xlsx)')
