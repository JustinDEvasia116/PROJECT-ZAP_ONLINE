# Generated by Django 4.0.8 on 2022-10-15 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ADMIN', '0003_subcategory_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory',
        ),
    ]
