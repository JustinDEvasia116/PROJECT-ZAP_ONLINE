# Generated by Django 4.0.8 on 2022-10-15 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER', '0010_alter_accounts_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x000001E8F06D4AF0>', max_length=200),
        ),
    ]
