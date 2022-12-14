# Generated by Django 4.0.6 on 2022-08-04 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('health', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('surname', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('profile_photo', models.CharField(max_length=1000)),
                ('birthday', models.DateField()),
                ('specialization', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='ECG_classification_result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('theta', models.JSONField()),
                ('precision', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Health_classification_result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('theta', models.JSONField()),
                ('precision', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Health_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('heartbeat', models.IntegerField()),
                ('systole', models.FloatField()),
                ('diastole', models.FloatField()),
                ('oxygen_saturation', models.IntegerField()),
                ('breathing_rate', models.IntegerField()),
                ('blood_glucose', models.FloatField()),
                ('temperature', models.FloatField()),
                ('chest_pain_type', models.IntegerField()),
                ('serum_cholestoral', models.FloatField()),
                ('exercise_induced_angina', models.IntegerField()),
                ('ST_depress_induced_by_exercise_relative_to_rest', models.FloatField()),
                ('health_classification', models.FloatField()),
                ('bmi', models.FloatField()),
                ('atrial_fibrillation', models.IntegerField()),
                ('leucocyte', models.FloatField()),
                ('urea_nitrogen', models.FloatField()),
                ('anion_gap', models.FloatField()),
                ('bicarbonate', models.FloatField()),
                ('lactic_acid', models.FloatField()),
                ('mortality_risk', models.FloatField()),
                ('ECG_classification', models.IntegerField(null=True)),
                ('hospitalization_risk', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('country', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=500)),
                ('province', models.CharField(max_length=500)),
                ('address', models.CharField(max_length=500)),
                ('postal_code', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Mortality_classification_result',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('theta', models.JSONField()),
                ('recall', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('surname', models.CharField(max_length=500)),
                ('sex', models.IntegerField()),
                ('hypertensive', models.IntegerField()),
                ('diabetes', models.IntegerField()),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('profile_photo', models.CharField(max_length=1000)),
                ('birthday', models.DateField()),
                ('fiscal_code', models.CharField(max_length=500)),
                ('phone_number', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('doctors', models.ManyToManyField(to='health.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Mortality_classification_entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intercept', models.IntegerField()),
                ('age', models.IntegerField()),
                ('sex', models.IntegerField()),
                ('bmi', models.FloatField()),
                ('hypertensive', models.IntegerField()),
                ('atrial_fibrillation', models.IntegerField()),
                ('diabetes', models.IntegerField()),
                ('heartbeat', models.IntegerField()),
                ('systole', models.FloatField()),
                ('diastole', models.FloatField()),
                ('breathing_rate', models.IntegerField()),
                ('temperature', models.FloatField()),
                ('oxygen_saturation', models.IntegerField()),
                ('leucocyte', models.FloatField()),
                ('urea_nitrogen', models.FloatField()),
                ('blood_glucose', models.FloatField()),
                ('anion_gap', models.FloatField()),
                ('lactic_acid', models.FloatField()),
                ('mortality_risk', models.FloatField(null=True)),
                ('health_data', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='health.health_data')),
            ],
        ),
        migrations.AddField(
            model_name='health_data',
            name='patient',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='health.patient'),
        ),
        migrations.CreateModel(
            name='Health_classification_entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intercept', models.IntegerField()),
                ('age', models.IntegerField()),
                ('sex', models.IntegerField()),
                ('chest_pain_type', models.IntegerField()),
                ('blood_pressure', models.FloatField()),
                ('serum_cholestoral', models.FloatField()),
                ('blood_sugar', models.IntegerField()),
                ('ecg_classification', models.IntegerField()),
                ('heartbeat', models.IntegerField()),
                ('exercise_induced_angina', models.IntegerField()),
                ('ST_depress_induced_by_exercise_relative_to_rest', models.FloatField()),
                ('health_classification', models.FloatField()),
                ('health_data', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='health.health_data')),
            ],
        ),
        migrations.CreateModel(
            name='ECG_Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.JSONField()),
                ('ECG_classification', models.IntegerField(null=True)),
                ('health_data', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='health.health_data')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='health.hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='patients',
            field=models.ManyToManyField(blank=True, to='health.patient'),
        ),
    ]
