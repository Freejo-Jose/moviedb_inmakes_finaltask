# Generated by Django 5.0.3 on 2024-03-13 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviedb', '0004_alter_category_pict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='released',
            field=models.DateField(blank=True),
        ),
    ]
