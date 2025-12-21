# inventario/models.py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): return self.nombre

class Producto(models.Model):
    codigo_barras = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    def __str__(self): return self.nombre

