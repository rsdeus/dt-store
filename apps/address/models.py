from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.db import models as geomodels


class Address(models.Model):

    STATES = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    COUNTRY = [
        ('BR', 'Brasil'),
    ]

    locality = models.CharField('Localidade', max_length=255, blank=True)
    street_number = models.CharField('Número', max_length=20, blank=True)
    complement = models.CharField('Complemento', max_length=255, blank=True)
    neighborhood = models.CharField('Bairro', max_length=100, blank=True)
    postal_code = models.CharField('CEP', max_length=8, blank=True)
    city = models.CharField('Cidade', max_length=165, blank=True, null=True)
    state = models.CharField('Estado', max_length=165, choices=STATES, blank=True, null=True)
    country = models.CharField('País', max_length=40, choices=COUNTRY, blank=True, null=True)
    geolocation = geomodels.PointField(blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['locality', 'street_number', 'neighborhood', 'city', 'state', 'country']

    def __str__(self):
        full_address = ''
        locality = self.locality
        street_number = self.street_number
        complement = self.complement
        neighborhood = self.neighborhood
        postal_code = self.postal_code
        city = self.city
        state = self.state
        country = self.country

        if locality:
            full_address = '%s' % locality
        if street_number:
            full_address += ', %s' % street_number
        if complement:
            full_address += ', %s' % complement
        if neighborhood:
            full_address += '- %s' % neighborhood
        if postal_code:
            full_address += '- %s' % postal_code
        if city:
            full_address += '- %s' % city
        if state:
            full_address += '- %s' % state
        if country:
            full_address += '- %s' % country

        return (full_address)

    def get_city(self):
        return(self.city + ', ' + self.state + ', ' + self.country)

    def get_geolocation(self):
        return(self.geolocation)
