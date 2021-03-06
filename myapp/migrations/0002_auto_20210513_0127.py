# Generated by Django 3.2 on 2021-05-12 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myhospital',
            old_name='hosp_no_of_beds',
            new_name='hosp_contact',
        ),
        migrations.RemoveField(
            model_name='myhospital',
            name='hosp_no_of_rooms',
        ),
        migrations.AlterField(
            model_name='mydoctor',
            name='clinic_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.myclinic'),
        ),
        migrations.AlterField(
            model_name='mydoctor',
            name='hospital_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.myhospital'),
        ),
    ]
