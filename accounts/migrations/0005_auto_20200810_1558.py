# Generated by Django 3.0.8 on 2020-08-10 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200810_1556'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tags',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='accounts.Tag'),
        ),
    ]
