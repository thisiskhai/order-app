from django import forms
from .models import Product, OrderEntry
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# ✅ Full form for admin (superuser)
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'unit']  # ❌ 'order_quantity' is excluded

# ✅ Quantity input form for staff only
class ProductStaffForm(forms.ModelForm):
    order_quantity = forms.IntegerField(min_value=1, required=True)

    class Meta:
        model = OrderEntry  # ✅ Use `OrderEntry` instead of `Product`
        fields = ['order_quantity']

class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

from django import forms
from django.contrib.auth.models import User

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
            'username': '',  # Remove default Django help text
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


class ProductImportForm(forms.Form):
    excel_file = forms.FileField(label='Choose Excel file (.xlsx)')


