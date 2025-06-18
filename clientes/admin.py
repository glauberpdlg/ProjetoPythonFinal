from django.contrib import admin

# clientes/admin.py
from .models import Cliente # Importa o modelo Cliente que você acabou de criar

# Registra o modelo Cliente no painel administrativo do Django
admin.site.register(Cliente)

from .models import Cardapio

admin.site.register(Cardapio)

