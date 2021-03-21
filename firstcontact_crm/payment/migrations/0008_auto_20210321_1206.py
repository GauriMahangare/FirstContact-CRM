# Generated by Django 3.0.12 on 2021-03-21 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_auto_20210321_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='freeTrialEndDate',
            field=models.DateTimeField(null=True, verbose_name='Free Trial End Date'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='nextPaymentDueDate',
            field=models.DateTimeField(null=True, verbose_name='Next Payment Due'),
        ),
    ]
