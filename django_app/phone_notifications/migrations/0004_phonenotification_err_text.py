# Generated by Django 4.2.4 on 2023-09-04 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phone_notifications', '0003_alter_phonenotification_mailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenotification',
            name='err_text',
            field=models.TextField(default=None, null=True),
        ),
    ]