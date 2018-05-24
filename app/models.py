from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .utils.storage import Sexs
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
import uuid


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """New User model"""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Profile(models.Model):
    """ Cette classe représente le profil de l'utilisateur"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=500, blank=True)
    sex = models.CharField(max_length=25, choices=[(tag, tag.value) for tag in Sexs], default=Sexs.MALE)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProductCategory(models.Model):
    """ The product category class stores the different categories of products """
    name_en = models.CharField(max_length=100, null=False, blank=False, default= 'dummy name')
    name_fr = models.CharField(max_length=100, null = False, blank=False, default= 'Nom par défaut')
    description_en = models.TextField(null=False, blank = False, default='A dummy description')
    description_fr = models.TextField(null=False, blank = False, default='Description par défaut')
    is_default = models.BooleanField(default = False)

    def __str__(self):
        return self.name_en



class Product(models.Model):

    def get_default_product_category():
        categories = ProductCategory.objects.all().filter(is_default = True)

        if len(categories) > 0:
            return categories[0]

    name_fr = models.CharField(max_length=100, blank = False, null=False, default='dummy name')
    description_fr = models.TextField(blank = False, null=False, default="A product")
    name_en = models.CharField(max_length=100, blank = False, null=False, default='dummy name')
    description_en = models.TextField(blank = False, null=False, default="A product")
    #le prix normal ouu par defaut du produit
    normal_price = models.FloatField(blank = False, null=False, default=0)
    #le prix actuel du produit
    price = models.FloatField(blank = False, null=False, default=0)
    sale = models.BooleanField(default = False, null=False)
    sold = models.BooleanField(default = False, null=False)
    new = models.BooleanField(default = True, null=False)
    discount = models.FloatField(blank = True, null=False, default=0)
    stock = models.IntegerField(blank = False, null=False, default=0)
    comming = models.BooleanField(default=False)
    category = models.ForeignKey(ProductCategory, default = get_default_product_category, on_delete=models.SET_DEFAULT)
    main_picture = models.ImageField(blank = False, null=False, default='img/logo.png')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    last_updated_at = models.DateTimeField(null = True, auto_now_add=True)
    def image_tag(self):
        return mark_safe('<img src="%s" width="250" class="img image-responsive" />' % (self.main_picture.url))
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.name_en


class ProductReview(models.Model):
    pass


class ProductImage(models.Model):

    uploaded_at = models.DateTimeField(auto_now_add=True)
    path = models.ImageField()
    product = models.ForeignKey('Product', null=True, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe('<img src="%s" width="250" class="img image-responsive" />' % (self.path.url))
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.path.url
    



