# Generated by Django 3.2.18 on 2024-01-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuracion',
            name='lista',
        ),
        migrations.AddField(
            model_name='catalogo',
            name='lista',
            field=models.JSONField(blank=True, null=True),
        ),
    ]