from django.db import models


class CsvOptions(models.Model):
    option = models.CharField(max_length=100,
                              choices=[('Control type', 'Typ kontroli'), ('Metod and norm', 'Norma i metoda pobrania'),
                                       ('Research status', 'Status badania'), ('Research', 'Badanie'), ('Sampling', 'Próbka'),
                                       ('Type', 'Typ'), ('Wijhars', 'WIJHARS'), ('Delivery Way','Sposób dostarczania')], default='')
    mode = models.CharField(max_length=100, choices=[('Write', 'Zapisz do csv'), ('Read', 'Odczytaj z csv')], default='Write')
