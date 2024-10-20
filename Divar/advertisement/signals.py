from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    categories = ['Car', 'RealEstate', 'Others']
    for category_name in categories:
        Category.objects.get_or_create(name=category_name)
