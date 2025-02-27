from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission



class Perm(models.Model):
    YETKİ_CHOICES = (
        ('view', 'Görüntüleme'),
        ('add', 'Ekleme'),
        ('change', 'Düzenleme'),
        ('delete', 'Silme'),
    )
    SAYFA_CHOICES = (

        ('filestack','Dosya Ekleri'),
        ('revisestack','Revizeler'),
        ('reportstack', 'Raporlar'),
        ('task','Görevler'),
        ('chat', 'Sohbetler'),
        ('customuser', 'Kullanıcılar'),
        ('auths', "Yetkilendirmeler"),
    )
    page = models.CharField(max_length=30, choices=SAYFA_CHOICES)
    view = models.BooleanField(("Görüntüleme"))
    add = models.BooleanField(("Ekleme"))
    change = models.BooleanField(("Düzenleme"))
    delete = models.BooleanField(("Silme"))

class Auths(models.Model):
    group = models.ForeignKey(Group, verbose_name=("Grup"), on_delete=models.CASCADE)
    perms = models.ManyToManyField(Perm, verbose_name=("Yetkiler"))

    def save(self, *args, **kwargs):
        # Önce mevcut izinleri temizle
        self.group.permissions.clear()  # Tüm izinleri sil
        
        # Sonrasında yeni izinleri ekleyin
        super().save(*args, **kwargs)  # Önce kaydet

        permission_types = ["add", "change", "delete", "view"]
        for yetki in self.perms.all():
            for perm_type in permission_types:
                if getattr(yetki, perm_type, False):
                    codename = f"{perm_type}_{yetki.page}"
                    permission = Permission.objects.filter(codename=codename).first()
                    if permission:
                        self.group.permissions.add(permission)

            