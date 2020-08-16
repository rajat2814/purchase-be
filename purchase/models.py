from datetime import datetime

from django.db import models


# Create your models here.
class PurchaseModel(models.Model):
    purchaser_name = models.CharField(max_length=256)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return '{0}-{1}'.format(self.purchaser_name, self.quantity)


class PurchaseStatusModel(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('verified', 'Verified'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered')
    )

    purchase = models.ForeignKey(PurchaseModel)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)
    created_at = models.DateTimeField()

    def __str__(self):
        return '{0} - {1}'.format(self.purchase, self.status)

    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.now()
        super(PurchaseStatusModel, self).save(*args, **kwargs)
