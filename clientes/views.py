
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, View
from .models import Cliente, Cardapio
from .form import ClienteForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


#Trabalhando com sessoes
class BuscaCliente(View):
    #metodo que renderiza nosso formulario de autenticação
    def get(self, request):
        return render(request, 'clientes/login.html')
    
    #A partir daqui vamos:
    #Identificar o email e o cpf do formulario, 
    #identificar o cliente e criar a sessao
    def post(self, request):
        email = request.POST.get('email')#Guarda email digitado no formulario
        telefone = request.POST.get('telefone')#Guarda telefone digitado no formulario

        if email and telefone: #verifica se o email e telefone existem
            #Guada as informações dos clientes (nosso_cliente)
            nosso_cliente = Cliente.objects.filter(email=email, telefone=telefone).first() #Pega o primerio cliente com o email e cpf
            if nosso_cliente: 
                #Vamos criar as sessoes
                request.session['nome_cliente'] = nosso_cliente.nome
                titulo = 'Cliente encontrado!'
                return render(request, 'clientes/home_cliente.html',{'cliente':nosso_cliente, 'title':titulo})

            else: 
                erro_message = "Nenhum cliente encontrado."
                return render(request, 'clientes/login.html', {'mensagem':erro_message})
        else: 
            erro_message = "Por favor, informe um email e cpf para consulta"
            return render(request, 'clientes/login.html', {'mensagem':erro_message})


#Classe que encerra a sessão
class Logout(View):
    #Metodo que verifica e encerra a sessão
    def get(self, request):
        if 'nome_cliente' in request.session:
            del request.session['nome_cliente']
        erro_message = 'Você foi desconectado!'
        return render(request, 'clientes/login.html', {'mensagem': erro_message})




# Página Inicial
class Home(ListView):
    def get(self, request):
        return render(request, 'clientes/home_cliente.html')
    
# Sobre Nós
class Sobre(ListView):
    def get(self, request):
        return render(request, 'clientes/sobrenos.html')
    
# Promoções
class Promo(ListView):
    def get(self, request):
        return render(request, 'clientes/promo.html')
    
# Informações
class Info(ListView):
    def get(self, request):
        return render(request, 'clientes/info.html')

# Ajuda
class Ajuda(ListView):
    def get(self, request):
        return render(request, 'clientes/ajuda.html')

# Cadastro
class Cliente_Create(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/forms_cliente.html'
    success_url = reverse_lazy('pag_inicial')

# Editar Cadastro
class Editar_Cadastro(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/forms_cliente.html'
    success_url = reverse_lazy('form_cadastro')

# Exibe cardápio por categoria
def cardapio_categoria(request, categoria):
    pratos = Cardapio.objects.filter(categoria=categoria)
    return render(request, 'cardapio.html', {'categoria': categoria, 'pratos': pratos})

# Exibe todos os pratos
def cardapio_todos(request):
    pratos = Cardapio.objects.all()
    return render(request, 'cardapio.html', {'pratos': pratos, 'categoria': 'Todos'})

# Adiciona ao pedido
def adicionar_ao_pedido(request):
    if request.method == 'POST':
        pedido = request.session.get('pedido', {})

        for prato in Cardapio.objects.all():
            qty = request.POST.get(f'quantidade_{prato.id}')
            try:
                quantidade = int(qty)
            except (TypeError, ValueError):
                quantidade = 0

            if quantidade > 0:
                pedido[str(prato.id)] = pedido.get(str(prato.id), 0) + quantidade

        request.session['pedido'] = pedido
        request.session.modified = True

        return redirect(request.META.get('HTTP_REFERER', 'pag_inicial'))

# Mostra resumo do pedido
def resumo_pedido(request):
    pedido = request.session.get('pedido', {})
    itens_pedido = []
    total_itens = 0
    for prato_id, quantidade in pedido.items():
        prato = get_object_or_404(Cardapio, id=int(prato_id))
        itens_pedido.append({'prato': prato, 'quantidade': quantidade})
        total_itens += quantidade
    return render(request, 'resumo_pedido.html', {
        'itens_pedido': itens_pedido,
        'total_itens': total_itens,
    })
    


def finalizar_pedido(request):
    if request.method == 'POST':
        pedido = request.session.get('pedido', {})
        if not pedido:
            messages.warning(request, 'Nenhum item no pedido para finalizar.')
            return redirect('resumo_pedido')

        # Aqui você pode salvar no banco ou enviar e-mail etc.
        request.session['pedido'] = {}  # Limpa o pedido
        request.session.modified = True
        messages.success(request, 'Pedido finalizado com sucesso!')
        return redirect('pag_inicial')
    else:
        return redirect('resumo_pedido')
    
""" def form_valid(self, form):
        response = super(Cliente_Create, self).method()

        # Cria um usuário para login usando email como username e telefone como senha
        email = form.cleaned_data['email']
        telefone = form.cleaned_data['telefone']
        nome = form.cleaned_data['nome']

        if not User.objects.filter(username=email).exists():
            User.objects.create(
                username=email,
                email=email,
                first_name=nome,
                password=make_password(telefone)  # senha criptografada
            )

        return response
 """

        

        