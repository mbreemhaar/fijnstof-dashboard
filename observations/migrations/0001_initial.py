# Generated by Django 4.2.3 on 2023-08-02 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('municipalities', '0005_alter_municipality_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_community_id', models.IntegerField()),
                ('latitude', models.DecimalField(decimal_places=3, max_digits=6)),
                ('longitude', models.DecimalField(decimal_places=3, max_digits=6)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='municipalities.municipality')),
            ],
        ),
    ]
