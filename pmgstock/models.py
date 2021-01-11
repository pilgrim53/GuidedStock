from django.db import models 


class Stock(models.Model):
   stock_name      = models.CharField(blank=False, null=False, max_length=40)
   ticker          = models.CharField(blank=False, null=False, max_length=10)
   purchase        = models.DecimalField(max_digits=10, decimal_places=2)
   sell_target     = models.DecimalField(max_digits=10, decimal_places=2)
   buy_target      = models.DecimalField(max_digits=10, decimal_places=2)
   shares          = models.IntegerField(default=0)
   current         = models.DecimalField(max_digits=10, decimal_places=2)
   proximity       = models.DecimalField(max_digits=10, decimal_places=2)   
   profit          = models.DecimalField(max_digits=10, decimal_places=2)
   showinform      = models.BooleanField
   username        = models.CharField(max_length=40)


