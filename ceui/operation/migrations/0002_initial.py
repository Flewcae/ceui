# Generated by Django 3.2.25 on 2025-02-26 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_initial'),
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='appointeds',
            field=models.ManyToManyField(related_name='user_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Görevliler'),
        ),
        migrations.AddField(
            model_name='task',
            name='appointer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Görevlendiren'),
        ),
        migrations.AddField(
            model_name='task',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat', verbose_name='Görev Sohbeti'),
        ),
        migrations.AddField(
            model_name='task',
            name='revises',
            field=models.ManyToManyField(related_name='task_revises', to='operation.ReviseStack', verbose_name='Görev Revizeleri'),
        ),
        migrations.AddField(
            model_name='task',
            name='updator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_tasks_updated', to=settings.AUTH_USER_MODEL, verbose_name='Güncelleyen'),
        ),
        migrations.AddField(
            model_name='revisestack',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_revises_created', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan'),
        ),
        migrations.AddField(
            model_name='revisestack',
            name='files',
            field=models.ManyToManyField(related_name='revised_files', to='operation.FileStack', verbose_name='Revize Dosyaları'),
        ),
        migrations.AddField(
            model_name='revisestack',
            name='images',
            field=models.ManyToManyField(related_name='revised_images', to='operation.ImageStack', verbose_name='Revize Resimleri'),
        ),
        migrations.AddField(
            model_name='revisestack',
            name='updator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_revises_updated', to=settings.AUTH_USER_MODEL, verbose_name='Güncelleyen'),
        ),
        migrations.AddField(
            model_name='reportstack',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reports_created', to=settings.AUTH_USER_MODEL, verbose_name='Oluşturan'),
        ),
        migrations.AddField(
            model_name='reportstack',
            name='files',
            field=models.ManyToManyField(related_name='report_files', to='operation.FileStack', verbose_name='Rapor Dosyaları'),
        ),
        migrations.AddField(
            model_name='reportstack',
            name='images',
            field=models.ManyToManyField(related_name='report_images', to='operation.ImageStack', verbose_name='Rapor Resimleri'),
        ),
        migrations.AddField(
            model_name='reportstack',
            name='revise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation.revisestack', verbose_name='Revize'),
        ),
        migrations.AddField(
            model_name='reportstack',
            name='updator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_reports_updated', to=settings.AUTH_USER_MODEL, verbose_name='Güncelleyen'),
        ),
        migrations.AddField(
            model_name='imagestack',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_images_uploaded', to=settings.AUTH_USER_MODEL, verbose_name='Yükleyen'),
        ),
        migrations.AddField(
            model_name='filestack',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_files_uploaded', to=settings.AUTH_USER_MODEL, verbose_name='Yükleyen'),
        ),
    ]
