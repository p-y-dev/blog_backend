# Generated by Django 2.2 on 2019-04-15 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date_birth',
            field=models.DateField(default='1900-01-01', verbose_name='Дата рождения'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='sex',
            field=models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], default='male', max_length=12, verbose_name='Пол'),
            preserve_default=False,
        ),
    ]
