# Generated by Django 3.1.5 on 2021-01-27 21:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20210127_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='system_user', to=settings.AUTH_USER_MODEL),
        ),
    ]