# Generated by Django 4.2.4 on 2023-09-04 17:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('access_expired_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('refresh_expired_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
