# Generated by Django 3.2 on 2021-05-11 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='myclinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_id', models.CharField(max_length=80)),
                ('clin_name', models.CharField(max_length=30)),
                ('clin_pincode', models.IntegerField()),
                ('clin_city', models.CharField(max_length=15)),
                ('clin_state', models.CharField(max_length=15)),
                ('clin_fulladdress', models.CharField(max_length=500)),
                ('clin_start_time', models.TimeField()),
                ('clin_closing_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='mycontactus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cs_name', models.CharField(max_length=30)),
                ('cs_email', models.EmailField(max_length=254)),
                ('cs_address', models.TextField()),
                ('cs_phone', models.CharField(max_length=10)),
                ('cs_msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='mydisease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dies_name', models.CharField(max_length=30)),
                ('dies_description', models.CharField(max_length=100)),
                ('dies_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='myhelp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_sub', models.CharField(max_length=30)),
                ('help_msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='myhospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_id', models.CharField(max_length=80)),
                ('hosp_name', models.CharField(max_length=30)),
                ('hosp_pincode', models.IntegerField()),
                ('hosp_city', models.CharField(max_length=15)),
                ('hosp_state', models.CharField(max_length=15)),
                ('hosp_fulladdress', models.CharField(max_length=500)),
                ('hosp_no_of_beds', models.IntegerField()),
                ('hosp_no_of_rooms', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='mymessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mess_from', models.CharField(max_length=30)),
                ('mess_to', models.CharField(max_length=30)),
                ('mess_date', models.DateField()),
                ('mess_time', models.TimeField()),
                ('mess_message', models.CharField(max_length=1000)),
                ('mess_attachment', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='mypatient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=30)),
                ('pat_name', models.CharField(max_length=30)),
                ('pat_email', models.EmailField(max_length=254)),
                ('pat_pass', models.CharField(max_length=40)),
                ('pat_contact', models.CharField(max_length=10, null=True)),
                ('pat_pincode', models.IntegerField(null=True)),
                ('pat_street', models.CharField(max_length=30, null=True)),
                ('pat_city', models.CharField(max_length=20, null=True)),
                ('pat_state', models.CharField(max_length=20, null=True)),
                ('pat_dob', models.DateField(max_length=8, null=True)),
                ('pat_bloodgroup', models.CharField(max_length=3, null=True)),
                ('pat_age', models.IntegerField(null=True)),
                ('pat_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='myregister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reg_name', models.CharField(max_length=30)),
                ('reg_email', models.EmailField(max_length=254)),
                ('reg_phone', models.CharField(max_length=10)),
                ('reg_pass', models.CharField(max_length=40)),
                ('reg_cpass', models.CharField(max_length=40)),
                ('reg_bloodgroup', models.CharField(blank=True, max_length=10, null=True)),
                ('reg_city', models.CharField(blank=True, max_length=15, null=True)),
                ('reg_address', models.TextField(blank=True, max_length=1000, null=True)),
                ('reg_dob', models.DateField(blank=True, max_length=8, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='myreview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rev_sub', models.CharField(max_length=30)),
                ('rev_msg', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='mydoctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_id', models.CharField(max_length=20)),
                ('doc_name', models.CharField(max_length=30)),
                ('doc_email', models.EmailField(max_length=254)),
                ('doc_contact', models.CharField(max_length=10)),
                ('doc_experience', models.IntegerField()),
                ('doc_pincode', models.IntegerField()),
                ('doc_city', models.CharField(max_length=20)),
                ('doc_state', models.CharField(max_length=20)),
                ('qualification', models.TextField()),
                ('specialization', models.CharField(max_length=80)),
                ('doc_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('clinic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.myclinic')),
                ('hospital_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.myhospital')),
            ],
        ),
    ]
