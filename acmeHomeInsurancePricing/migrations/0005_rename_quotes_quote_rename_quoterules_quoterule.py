# Generated by Django 4.2.6 on 2023-10-14 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acmeHomeInsurancePricing', '0004_state_monthly_tax'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Quotes',
            new_name='Quote',
        ),
        migrations.RenameModel(
            old_name='QuoteRules',
            new_name='QuoteRule',
        ),
    ]