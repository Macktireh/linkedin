import os
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

User = get_user_model()

def rename_img(instance, filename):
    upload_to = 'image_profile'
    ext = filename.split('.')[-1]
    filename = f"{instance.user.first_name}_{instance.user.pk}_{instance.date_updated.strftime('%d-%m-%Y %H%M%S')}.{ext}"
    folder = f"{instance.user.first_name}_{instance.user.pk}"
    return os.path.join(folder, upload_to, filename)

def pseudo_rename(instance, filename):
    upload_to = 'image_profile'
    ext = filename.split('.')[-1]
    filename = f"{instance.user.first_name}_{instance.user.pk}_{instance.date_updated}.{ext}"
    return os.path.join(upload_to, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    pseudo = models.CharField(_("non d'utilisateur"), max_length=48, blank=True, unique=True)
    bio = models.CharField(_("titre du profil"), max_length=250, blank=True)
    img_profile = models.ImageField(_("photo de profile"), upload_to=rename_img, blank=True, null=True)
    img_bg = models.ImageField(_("photo de couverture"), upload_to=rename_img, blank=True, null=True)
    birth_date = models.DateField(_("date de naissence"), null=True, blank=True)
    gender = models.CharField(_("sexe"), max_length=15, blank=True, choices=(('M', 'Male'), ('F', 'Female')))
    phone = models.CharField(_("téléphone"), max_length=20, blank=True)
    adress = models.CharField(_("adresse"), max_length=128, blank=True)
    town = models.CharField(_("ville"), max_length=68, blank=True)
    region = models.CharField(_("région"), max_length=68, blank=True)
    zipcode = models.CharField(_("code postal"), max_length=22, blank=True)
    country = models.CharField(_("pays"), max_length=45, blank=True)
    description = models.TextField(_("description"), blank=True)
    link_linkedin = models.URLField(_("lien de votre profile linkedin"), blank=True)
    link_gitthub = models.URLField(_("lien de votre profile gitthub"), blank=True)
    link_twitter = models.URLField(_("lien de votre twitter"), blank=True)
    link_mysite = models.URLField(_("lien de votre de site web"), blank=True)
    number_views = models.IntegerField(_('Nombre de vue profil'), default=0, blank=True, null=True)
    date_updated = models.DateTimeField(_("date de modification"), auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        if instance.first_name is not None or instance.first_name != '':
            instance.profile.pseudo = f'{instance.first_name}{instance.pk}'
            instance.profile.save()
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.profile.pseudo == '':
        if instance.first_name is not None or instance.first_name != '':
            instance.profile.pseudo = f'{instance.first_name}{instance.pk}'.lower()
            instance.profile.save()
    instance.profile.save()