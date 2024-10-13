from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class GasUtilCustomers(models.Model):
    csr_employee_ref = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gas_util_csr_employee')
    customer_ref = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gas_util_customer')
    unique_customer_tracking_id = models.CharField(max_length=50, blank=True)
    created_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gas_util_customer'



class GasUtilServiceRequest(models.Model):
    customer_ref = models.ForeignKey(GasUtilCustomers, on_delete=models.CASCADE)
    type_of_service = models.CharField(max_length=100, blank=False, null=False)
    service_request_details = models.CharField(max_length=100, blank=False, null=False)
    status = models.IntegerField(default=0, blank=False, null=False)
    created_on = models.DateTimeField(auto_now=True)
    resolved_on = models.DateTimeField(default=timezone.now())
    service_paid_on = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = 'gas_util_service_request'



class GasUtilServiceRequestAttachments(models.Model):
    gas_util_service_request_ref = models.ForeignKey(GasUtilServiceRequest, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='attachments')

    class Meta:
        db_table = 'gas_util_service_request_attachments'