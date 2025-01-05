from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=50, unique=True)
    precio_contado = models.DecimalField(max_digits=10, decimal_places=2)
    precio_credito = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
