"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from clientes.views import Home,Sobre,Promo,Info ,Ajuda ,Cliente_Create, Editar_Cadastro, cardapio_categoria, adicionar_ao_pedido, resumo_pedido, finalizar_pedido,BuscaCliente,Logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name="pag_inicial"),
    path('cadastro/', Cliente_Create.as_view(), name="cadastro"),
    path('editar/', Editar_Cadastro.as_view(), name="editar"),
    path('cardapio/<str:categoria>/', cardapio_categoria, name='cardapio_categoria'),
    path('adicionar_ao_pedido/', adicionar_ao_pedido, name='adicionar_ao_pedido'),
    path('resumo_pedido/', resumo_pedido, name='resumo_pedido'),
    path('finalizar_pedido/', finalizar_pedido, name='finalizar_pedido'),
    path('login/', BuscaCliente.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('sobre/', Sobre.as_view(), name = "sobre"),
    path('promo/', Promo.as_view(), name = "promo"),
    path('info/', Info.as_view(), name = "info"),
    path('ajuda/', Ajuda.as_view(), name = "ajuda"),  
]