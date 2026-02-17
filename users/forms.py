from django import forms

class RegisterForms(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        password_confirm = data.get("confirm_password")
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return data

class LoginForms(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class UpdateProfileForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    age = forms.IntegerField(required=True)
    image = forms.ImageField(required=False)
