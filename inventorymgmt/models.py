from django.db import models
import os
from django.dispatch import receiver

# Create your models here.
class Stock(models.Model):
	item_name = models.CharField(max_length=50, blank=False, null=False)
	quantity = models.IntegerField(default='0', blank=False, null=False)
	category = models.CharField(max_length=50, blank=True, null=True)
	brand = models.CharField(max_length=50,  blank=True, null=True)
	price = models.CharField(max_length=10, blank=False, null=True)
	receive_quantity = models.IntegerField(default='0', blank=True, null=True)
	receive_by = models.CharField(max_length=50, blank=True, null=True)
	receive_from = models.CharField(max_length=50, blank=True, null=True)
	issue_quantity = models.IntegerField(default='0', blank=True, null=True)
	issue_by = models.CharField(max_length=50, blank=True, null=True)
	issue_to = models.CharField(max_length=50, blank=True, null=True)
	phone_number = models.CharField(max_length=50, blank=True, null=True)
	created_by = models.CharField(max_length=50, blank=True, null=True)
	reorder_level = models.IntegerField(default='0', blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	image = models.ImageField(upload_to='product_images/', blank=True, null=True)
	export_to_CSV = models.BooleanField(default=False)
    
	class Meta: 
		constraints = [
            models.UniqueConstraint(
                fields=['item_name', 'brand', 'category'],
                name='unique_stock'
            )
        ]
		
	def __str__(self):
		return self.item_name


class StockHistory(models.Model):
    stock_id = models.IntegerField(blank=True, null=True)  
    item_name = models.CharField(max_length=50,blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    receive_quantity = models.IntegerField(blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    receive_from = models.CharField(max_length=100, blank=True, null=True)
    issue_quantity = models.IntegerField(blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)





def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Stock` object is deleted.
    """
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

# Connect the function to post_delete signal
@receiver(models.signals.post_delete, sender=Stock)
def auto_delete_file_on_delete_handler(sender, instance, **kwargs):
    auto_delete_file_on_delete(sender, instance, **kwargs)

# 🚨 Replace old image when a new one is uploaded
@receiver(models.signals.pre_save, sender=Stock)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem when `Stock` object is updated with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Stock.objects.get(pk=instance.pk).image
    except Stock.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if old_file and os.path.isfile(old_file.path):
            os.remove(old_file.path)