from django.contrib import admin

from institucional.models import Ata
from institucional.forms import formsAta

class AdminAta(admin.ModelAdmin):
    form = formsAta
    search_fields = ('title', 'time')

admin.site.register(Ata ,AdminAta)


# Criamos um arquivo JSON com todas as informações das atas para o novo site
import json

# conteudo, data_criacao
# highlights = None

json_lista = []
atas = Ata.objects.all()

for ata in atas:
    json_ = {
        'conteudo': str(ata.content),
        'data_criacao': str(ata.time),
        'highlights': ata.title,
    }

    json_lista.append(json_)

# Agora imprimimos
with open('atas.json', 'w') as arquivo:
    json.dump(json_lista, arquivo)
