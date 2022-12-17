from django.db import models
from account.models import User, profile
from account.utils import send_notification
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(profile, related_name="profile", on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            #update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                if self.is_approved:
                    # send a notification
                    mail_subject = 'Congratulations! You Restaurant has been approved'
                    template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved
                    }
                    send_notification(mail_subject, template, context)
                else:
                    # send a notification
                    mail_subject = "we're sorry! You are not eligible for publishing your food menu on our restaurant"
                    template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved
                    }
                    send_notification(mail_subject, template, context)
        return super(Vendor, self).save(*args, **kwargs)
