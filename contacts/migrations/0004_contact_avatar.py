# Generated by Django 5.0.4 on 2024-04-13 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_remove_contact_avatar_contact_phone2'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='contact'),
        ),
    ]
