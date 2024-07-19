from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()


class SavedAds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_ads_user')
    category_name = models.CharField(max_length=100)
    ads_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.email +' ' + self.category_name + self.ads_id
    

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    MyAds = models.JSONField(blank=True, null=True)
    Saved_Ads = models.ManyToManyField(SavedAds)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

