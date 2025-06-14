from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    """
    View para a página inicial do site.
    Acessível para todos os usuários, autenticados ou não.
    """
    context = {
        'title': 'SteamRF - Início'
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard(request):
    """
    View para o painel do usuário.
    Acessível apenas para usuários autenticados.
    """
    context = {
        'title': 'SteamRF - Painel'
    }
    return render(request, 'core/dashboard.html', context)
