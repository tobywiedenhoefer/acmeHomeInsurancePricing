# Generated by Django 4.2.6 on 2023-10-13 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acmeHomeInsurancePricing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_subtotal', models.FloatField()),
                ('monthly_taxes', models.FloatField()),
            ],
        ),
    ]
