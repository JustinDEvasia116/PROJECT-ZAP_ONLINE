# Generated by Django 4.0.8 on 2022-11-16 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER', '0020_alter_accounts_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x00000214CB7BF370>', max_length=200),
        ),
    ]