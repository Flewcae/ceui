# Generated by Django 3.2.25 on 2025-02-26 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Dosya Adı')),
                ('file', models.FileField(upload_to='task_files', verbose_name='Dosya')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Yüklenme Anı')),
            ],
        ),
        migrations.CreateModel(
            name='ImageStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Resim Adı')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Resim')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Yüklenme Anı')),
            ],
        ),
        migrations.CreateModel(
            name='ReportStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.TextField(verbose_name='Rapor Açıklaması')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Anı')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Anı')),
            ],
        ),
        migrations.CreateModel(
            name='ReviseStack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('canceled', 'İptal Edildi'), ('working', 'Üzerine Çalışılıyor'), ('answer_waiting', 'Cevap Bekleniyor'), ('revise', 'Revize'), ('completed', 'Tamamlandı')], max_length=50, verbose_name='Durum')),
                ('desc', models.TextField(verbose_name='Revize Açıklaması')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Anı')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Anı')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Görev Adı')),
                ('status', models.CharField(choices=[('canceled', 'İptal Edildi'), ('working', 'Üzerine Çalışılıyor'), ('revise_done', 'Çalışma Tamamlandı'), ('completed', 'Görev Tamamlandı')], max_length=50, verbose_name='Durum')),
                ('deadline', models.DateField(verbose_name='Son Tarih')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Anı')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Güncellenme Anı')),
            ],
        ),
    ]
