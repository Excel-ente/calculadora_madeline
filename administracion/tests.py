from django.test import TestCase

# Create your tests here.
from administracion.models import Receta

def ActualizacionIntermediaria():
    recetas = Receta.objects.all()

    for receta in recetas:
        receta.save()