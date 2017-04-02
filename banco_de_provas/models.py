from django.db import models

# Salva o arquivo com um nome regular
def nomedoarquivo(instance,filename):
    return("banco_de_provas/" +  '-'.join([instance.materia, instance.tipo,instance.semestre,instance.professor]) + filename[-4:])


# Modelo do banco de provas
class Prova(models.Model):
    file = models.FileField(upload_to=nomedoarquivo)
    materia = models.CharField(max_length=10)
    semestre = models.CharField(max_length=10)
    professor = models.CharField(max_length=50,blank=True)
    tipo = models.CharField(max_length=15)
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return self.materia + " " + self.tipo + " " + self.professor + " " +  self.semestre

    def save(self, force_insert=False, force_update=False):
        self.materia = self.materia.lower().replace(' ','').replace('-','')
        self.semestre = self.semestre.lower().replace(' ','_').replace('-','_')
        self.professor = self.professor.lower().replace(' ','_').replace('-','_')
        self.tipo = self.tipo.replace(' ','_').replace('-','_')
        super(Prova, self).save(force_insert, force_update)
