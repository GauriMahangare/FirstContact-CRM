# Generated by Django 3.2 on 2021-05-20 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_auto_20210411_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='expiry_month',
            field=models.CharField(blank=True, choices=[('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')], max_length=2, verbose_name='Card Expiry Month'),
        ),
    ]
