
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib import messages

User = get_user_model() 


def register(request):
    """
    Função que lida com o cadastro de novos usuários sem usar forms.
    """
    if request.method == 'POST':
        # Pega os dados diretamente do POST
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Valida campos obrigatórios
        if not username or not email or not password or not password2:
            messages.error(request, "Todos os campos são obrigatórios.")
        elif password != password2:
            messages.error(request, "As senhas não coincidem.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Este nome de usuário já existe.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Este email já está cadastrado.")
        else:
            # Cria o usuário
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # Loga o usuário automaticamente
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial

    # Se não for POST ou houver erro, renderiza o template
    return render(request, 'usuarios/register.html')
