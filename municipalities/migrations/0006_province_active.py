# Generated by Django 4.2.3 on 2023-08-02 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('municipalities', '0005_alter_municipality_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='province',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
