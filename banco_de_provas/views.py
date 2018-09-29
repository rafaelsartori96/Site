from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.core.mail import EmailMessage

import json

from banco_de_provas.forms import ProvaForm
from banco_de_provas.models import Prova

config = json.load(open('config.json'))

FROM_EMAIL = config['EMAIL_NAME'] + ' <' + config['EMAIL_HOST_USER'] + '>'
MSG_ADICAO_PROVA ="""
    Uma prova foi inserida no banco de provas.
    Visite a página http://www.caco.ic.unicamp.br/adminbanco_de_provas/prova/{0}/
    e revise as informações antes de aprovar.

    Matéria     : {1}
    Semestre    : {2}
    Tipo        : {3}
    Professor   : {4}

    """
MSG_AGRADECIMENTO="""
    Obrigado por contribuir com o banco de provas.
    """

# Views relativas ao banco de provas
def BancoView(request):
    busca = request.GET.get('search')

    #Faz busca
    resultados = ""
    if(busca):
        resultados = busca_BP(busca)

    return render(request, 'banco_provas.html', {'resultados':resultados})


@csrf_protect
def enviar(request):
    if request.method == 'GET':
        return render(request, 'form_bp.html', {"form": ProvaForm})

    # Caso a requisao seja post...
    # (Talvez seja melhor ser explicitamente post, e isso acontece em mais
    #  locais do código)
    form = ProvaForm(request.POST, request.FILES)

    print("Form : " + str(form))

    if form.is_valid():
        # Salva a prova no banco de prova
        prova = form.save()

        print(prova)

        # Para envio do email
        sjt = '[CACo][Banco de Provas] Adição de prova no Banco de Provas'
        msg = MSG_ADICAO_PROVA.format(prova.id, prova.materia, prova.semestre,
                                      prova.tipo, prova.professor)

        # Faz um novo email
        email = EmailMessage(
            sjt,
            msg,
            FROM_EMAIL,
            ['caco@ic.unicamp.br']
        )

        # Caso esteja no modo debug, nao envia o email, apenas imprime na tela
        try:
            email.send()

            return render(request, 'obrigado.html', {'mensagem': MSG_AGRADECIMENTO})
        except Exception as inst:
            print("Erro ao enviar email membros")
            print(type(inst))
            print(inst)
    else:
        print(form.errors.as_data())
        return render(request, 'form_bp.html', {"form": ProvaForm})


# Implementa a busca no banco de provas. Para entender leia a documentação sobre objetos Q em django
def busca_BP(busca):
    query_final = Q()
    palavras = busca.split()
    for palavra in palavras:
        query = Q(materia__icontains=palavra) | Q(tipo__icontains=palavra) | Q(professor__icontains=palavra) | Q(semestre__icontains=palavra)
        query_final = query & query_final


    return Prova.objects.filter(query_final).filter(aprovado=True).all().order_by('-semestre')
