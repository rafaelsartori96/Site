from django import forms
from django.forms.fields import Field
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError

from banco_de_provas.models import Prova

class ProvaForm(forms.ModelForm):
    materia = forms.CharField(label="Matéria",
                               max_length=10,
                               help_text= "Ex: MC102",
                               )
    semestre = forms.CharField(label="Semestre",
                                max_length=10,
                                help_text= "Ex: 2014s1, 2015s2, 2016fer",
                                required=False
                                )
    tipo = forms.CharField(label="Tipo",
                            max_length=10,
                            help_text= "Ex: p1, p2_res, teste1, exame, lista",
                            )
    professor = forms.CharField(label="Professor",
                                max_length=50,
                                help_text="Nome do professor que está ministrando a matéria",
                                required=False
                                )
    file = forms.FileField(label="Arquivo",
                           help_text="Dê preferencia para arquivos PDF"
                          )

    class Meta:
        model = Prova
        fields = ('materia', 'semestre', 'tipo', 'professor', 'file')
