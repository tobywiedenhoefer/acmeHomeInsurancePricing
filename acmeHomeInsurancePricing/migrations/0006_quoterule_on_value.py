# Generated by Django 4.2.6 on 2023-10-14 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acmeHomeInsurancePricing', '0005_rename_quotes_quote_rename_quoterules_quoterule'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoterule',
            name='on_value',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]