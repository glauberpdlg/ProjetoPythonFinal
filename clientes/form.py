from django import forms 
from .models import Cliente
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome',
            'endereco',
            'telefone',
            'email'
        ]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control","placeholder": "Digite seu nome"}),
            "endereco": forms.TextInput(attrs={"class": "form-control","placeholder": "Digite seu endereço"}),
            "telefone": forms.TextInput(attrs={"class": "form-control","placeholder": "(XX) XXXX-XXXX"}), # Exemplo de placeholder para Telefone
            "email": forms.EmailInput(attrs={"class": "form-control","placeholder": "email@example.com"}), # Usando EmailInput
            "data_cadastro": forms.DateInput(attrs={"class": "form-control","placeholder": "DD/MM/AAAA", 'type': 'date'}), # Usando DateInput e type='date'
        }

class Cliente_Create(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'  # ou outro template
    success_url = '/'  # ou a URL de redirecionamento após o cadastro

    def form_valid(self, form):
        response = super().form_valid(form)

        email = form.cleaned_data['email']
        telefone = form.cleaned_data['telefone']
        nome = form.cleaned_data['nome']

        if not User.objects.filter(username=email).exists():
            User.objects.create(
                username=email,
                email=email,
                first_name=nome,
                password=make_password(telefone)
            )

        return response