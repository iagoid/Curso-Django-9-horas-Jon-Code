from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import ContactForm

def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        nome = request.POST.get('nome', '')
        email = request.POST.get('email', '')
        mensagem  = request.POST.get('mensagem', '')
        email = EmailMessage(
            "Mensagem do Blog Django",
            "De {} <{}> Escrever \n\n {}".format(nome, email, mensagem),
            "não-responder@inbox.mailtrap.io",
            ["iagoid01@gmail.com"],
            reply_to=[email]
        )
        try:
            email.send()
            send = True
        except:
            send = False

    send = None
    context = {
        'form': form,
        'success': send,
    }
    return render(request, 'contact/contact.html', context)
