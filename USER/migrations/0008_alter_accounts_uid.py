# Generated by Django 4.0.8 on 2022-10-15 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER', '0007_alter_accounts_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000002165ABD4AF0>', max_length=200),
        ),
    ]