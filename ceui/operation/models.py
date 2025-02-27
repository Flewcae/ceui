from django.db import models

class FileStack(models.Model): 
    name = models.CharField(verbose_name="Dosya Adı", max_length=50)
    file = models.FileField(verbose_name="Dosya", upload_to='task_files', max_length=100)
    uploaded_by = models.ForeignKey(
        "user.CustomUser", verbose_name="Yükleyen", related_name='user_files_uploaded',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    uploaded_at = models.DateTimeField(verbose_name='Yüklenme Anı', auto_now_add=True)

    def __str__(self):
        return self.name


class ImageStack(models.Model): 
    name = models.CharField(verbose_name="Resim Adı", max_length=50)
    image = models.ImageField(verbose_name="Resim", upload_to='images/')
    uploaded_by = models.ForeignKey(
        "user.CustomUser", verbose_name="Yükleyen", related_name='user_images_uploaded',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    uploaded_at = models.DateTimeField(verbose_name='Yüklenme Anı', auto_now_add=True)

    def __str__(self):
        return self.name


class ReviseStack(models.Model):
    REVISE_SITUATIONS = (
        ('canceled', 'İptal Edildi'),
        ('working', 'Üzerine Çalışılıyor'),
        ('answer_waiting', 'Cevap Bekleniyor'),
        ('revise', 'Revize'),
        ('completed', 'Tamamlandı'),
    )

    status = models.CharField(verbose_name="Durum", choices=REVISE_SITUATIONS, max_length=50)
    desc = models.TextField(verbose_name="Revize Açıklaması")
    files = models.ManyToManyField(FileStack, verbose_name="Revize Dosyaları", related_name='revised_files')
    images = models.ManyToManyField(ImageStack, verbose_name="Revize Resimleri", related_name='revised_images')

    creator = models.ForeignKey(
        "user.CustomUser", verbose_name="Oluşturan", related_name="user_revises_created",
        on_delete=models.CASCADE
    )
    updator = models.ForeignKey(
        "user.CustomUser", verbose_name="Güncelleyen", related_name="user_revises_updated",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name='Oluşturulma Anı', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Güncellenme Anı', auto_now=True)


class ReportStack(models.Model):
    revise = models.ForeignKey(ReviseStack, verbose_name="Revize", on_delete=models.CASCADE)
    desc = models.TextField(verbose_name="Rapor Açıklaması")
    files = models.ManyToManyField(FileStack, verbose_name="Rapor Dosyaları", related_name='report_files')
    images = models.ManyToManyField(ImageStack, verbose_name="Rapor Resimleri", related_name='report_images')

    creator = models.ForeignKey(
        "user.CustomUser", verbose_name="Oluşturan", related_name="user_reports_created",
        on_delete=models.CASCADE
    )
    updator = models.ForeignKey(
        "user.CustomUser", verbose_name="Güncelleyen", related_name="user_reports_updated",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name='Oluşturulma Anı', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Güncellenme Anı', auto_now=True)


class Task(models.Model):

    TASK_SITUATIONS = (
        ('canceled', 'İptal Edildi'),
        ('working', 'Üzerine Çalışılıyor'),
        ('revise_done', 'Çalışma Tamamlandı'),
        ('completed', 'Görev Tamamlandı'),
    )

    name = models.CharField(verbose_name="Görev Adı", max_length=50)
    status = models.CharField(verbose_name="Durum", choices=TASK_SITUATIONS, max_length=50)
    deadline = models.DateField(verbose_name="Son Tarih")
    revises = models.ManyToManyField(ReviseStack, verbose_name="Görev Revizeleri", related_name="task_revises")
    chat = models.ForeignKey("chat.Chat", verbose_name="Görev Sohbeti", on_delete=models.CASCADE)
    appointeds = models.ManyToManyField("user.CustomUser", verbose_name="Görevliler", related_name="user_tasks")
    appointer = models.ForeignKey("user.CustomUser", verbose_name="Görevlendiren", on_delete=models.CASCADE)

    updator = models.ForeignKey(
        "user.CustomUser", verbose_name="Güncelleyen", related_name="user_tasks_updated",
        on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name='Oluşturulma Anı', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Güncellenme Anı', auto_now=True)
