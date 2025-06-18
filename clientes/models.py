from django.db import models

class Cliente(models.Model):
    # Campos que representam as colunas da tabela 'Cliente' no banco de dados
    nome = models.CharField(max_length=100) # Nome do cliente, string de até 100 caracteres
    endereco = models.CharField(max_length=200) # Endereço completo do cliente, string de até 200 caracteres
    telefone = models.CharField(max_length=20, blank=True, null=True) # Telefone do cliente, opcional (blank=True, null=True)
    email = models.EmailField(unique=True) # Email do cliente, deve ser único e formatado como email
    data_cadastro = models.DateTimeField(auto_now_add=True) # Data e hora do cadastro, preenchido automaticamente na criação

    def __str__(self):
        """
        Método que retorna uma representação amigável do objeto Cliente.
        Isso é útil no painel administrativo do Django e ao depurar.
        """
        return f"{self.nome} {self.telefone} ({self.email})"

    class Meta:
        """
        A classe Meta é uma classe interna que fornece metadados sobre o modelo.
        """
        verbose_name = "Cliente" # Nome singular amigável para o modelo no painel administrativo
        verbose_name_plural = "Clientes" # Nome plural amigável para o modelo no painel administrativo
        ordering = ['nome', 'telefone'] # Define a ordem padrão dos registros ao consultá-los
        # Os registros serão ordenados primeiro pelo nome, depois pelo sobrenome.

    # clientes/models.py



# clientes/models.py

class Cardapio(models.Model):
    principal = models.CharField(max_length=100)
    acompanhamento = models.CharField(max_length=100)
    categoria = models.CharField(
max_length=20,
        choices=[('comum', 'Comum'), ('saudavel', 'Saudável'), ('low_carb', 'Low Carb')]
    )

    def __str__(self):
        return f"{self.principal} com {self.acompanhamento} ({self.get_categoria_display()})"


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    cardapio = models.ForeignKey(Cardapio, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.cardapio.principal}"