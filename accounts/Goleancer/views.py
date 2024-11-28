from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.contrib.auth.decorators import login_required

#forms.register
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label="Confirm Password"
    )
#register
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            })
        }
#validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

# Register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registrasi berhasil!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'Goleancer/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login berhasil!')
            return redirect('dashboard')  # Sesuaikan URL tujuan setelah login
        else:
            messages.error(request, 'Username atau password salah')
    return render(request, 'Goleancer/login.html')
#landingpage view
def landingpage_view(request):
    return render(request, 'Goleancer/landingpage.html')  
#classes view
def classes_view(request):
    return render(request, 'Goleancer/classes.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        user.first_name = request.POST.get('name')
        profile.phone = request.POST.get('phone')
        user.save()
        profile.save()
        messages.success(request, "Profil berhasil diperbarui!")
        return redirect('update_profile')
    return render(request, 'Goleancer/profile.html')

#settings view
def settings_view(request):
    return render(request, 'acc_app/settings.html')
#dashboard view
@login_required
def dashboard_view(request):
    return render(request, 'Goleancer/dashboard.html')  # Halaman dashboard

def logout_view(request):
    logout(request)
    return redirect('Goleancer/landingpage.html')  # Setelah logout, arahkan ke halaman login