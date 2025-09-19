
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    """
    Função que lida com o cadastro de novos usuários.
    """
    if request.method == 'POST':
        # Se a requisição for POST (usuário enviou o formulário)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Se os dados forem válidos, cria o usuário
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Loga o usuário e redireciona para a página inicial
            login(request, user)
            return redirect('home')  # 'home' deve ser a URL da página inicial do seu projeto
    else:
        # Se a requisição for GET (primeiro acesso à página)
        form = CustomUserCreationForm()
    
    # Renderiza o template de cadastro, passando o formulário para ele
    return render(request, 'usuarios/register.html', {'form': form})
