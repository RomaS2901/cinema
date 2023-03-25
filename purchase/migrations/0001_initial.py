# Generated by Django 4.1.7 on 2023-03-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(choices=[('PR', 'Purchase'), ('RT', 'Return')], max_length=2)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
