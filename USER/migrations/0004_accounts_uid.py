# Generated by Django 4.0.8 on 2022-10-11 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER', '0003_remove_accounts_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000023C3AFD4AF0>', max_length=200),
        ),
    ]
