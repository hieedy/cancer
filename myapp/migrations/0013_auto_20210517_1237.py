# Generated by Django 3.2 on 2021-05-17 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_delete_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mydoctor',
            name='doc_contact',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='mypatient',
            name='pat_contact',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='myregister',
            name='reg_phone',
            field=models.CharField(max_length=12),
        ),
    ]
