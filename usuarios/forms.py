
from django import forms
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    # Campos para a senha, usando o widget de senha para esconder o texto
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        # Usa o modelo de usuário que você criou
        model = User
        # Os campos que vão aparecer no formulário
        fields = ('email', 'username')

    def clean(self):
        # Esta função garante que as duas senhas são iguais
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data