from django.db import models


class Health_Data(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)
    heartbeat = models.IntegerField()
    systole = models.FloatField()  # resting blood pressure
    diastole = models.FloatField()
    oxygen_saturation = models.FloatField()
    breathing_rate = models.FloatField()
    blood_glucose = models.FloatField()
    temperature = models.FloatField()
    # -------------------------------------------------
    # health classification
    chest_pain_type = models.IntegerField()  # tipo ti dolore toracico
    serum_cholestoral = models.FloatField()
    exercise_induced_angina = models.IntegerField()
    ST_depress_induced_by_exercise_relative_to_rest = models.FloatField()
    health_classification = models.FloatField()
    # --------------------------------------------------
    # mortality classification
    bmi = models.FloatField()
    atrial_fibrillation = models.IntegerField()
    leucocyte = models.FloatField()
    urea_nitrogen = models.FloatField()
    anion_gap = models.FloatField()
    bicarbonate = models.FloatField()
    lactic_acid = models.FloatField()
    mortality_risk = models.FloatField()
    # ----------------------------------------------------
    ECG_classification = models.IntegerField(null=True)
    hospitalization_risk = models.FloatField(null=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, default=0)


class ECG_Entry(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.JSONField()
    ECG_classification = models.IntegerField(null=True)
    health_data = models.OneToOneField(
        Health_Data,
        on_delete=models.SET_NULL,
        null=True
    )


class Mortality_classification_entry(models.Model):
    intercept = models.IntegerField()
    age = models.IntegerField()
    sex = models.IntegerField()
    bmi = models.FloatField()
    hypertensive = models.IntegerField()
    atrial_fibrillation = models.IntegerField()
    diabetes = models.IntegerField()
    heartbeat = models.IntegerField()
    systole = models.FloatField()  # resting blood pressure
    diastole = models.FloatField()
    breathing_rate = models.IntegerField()
    temperature = models.FloatField()
    oxygen_saturation = models.IntegerField()
    leucocyte = models.FloatField()
    urea_nitrogen = models.FloatField()
    blood_glucose = models.FloatField()
    anion_gap = models.FloatField()
    bicarbonate = models.FloatField(null=True)
    lactic_acid = models.FloatField()
    mortality_risk = models.FloatField(null=True)
    health_data = models.OneToOneField(
        Health_Data,
        on_delete=models.SET_NULL,
        null=True
    )


class Health_classification_entry(models.Model):
    intercept = models.IntegerField()
    age = models.IntegerField()
    sex = models.IntegerField()
    chest_pain_type = models.IntegerField()  # tipo ti dolore toracico
    blood_pressure = models.FloatField()  # resting blood pressure
    serum_cholestoral = models.FloatField()
    blood_sugar = models.IntegerField()  # 1 if blood_sugar > 120
    ecg_classification = models.IntegerField()
    heartbeat = models.IntegerField()
    exercise_induced_angina = models.IntegerField()
    ST_depress_induced_by_exercise_relative_to_rest = models.FloatField()
    health_classification = models.FloatField()
    health_data = models.OneToOneField(
        Health_Data,
        on_delete=models.SET_NULL,
        null=True
    )


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    surname = models.CharField(max_length=500)
    sex = models.IntegerField() #1 if man, 0 if woman
    hypertensive = models.IntegerField()
    diabetes = models.IntegerField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=30)
    profile_photo = models.CharField(max_length=1000)
    birthday = models.DateField()
    fiscal_code = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    doctors = models.ManyToManyField("Doctor")


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    surname = models.CharField(max_length=500)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=30)
    profile_photo = models.CharField(max_length=1000)
    birthday = models.DateField()
    specialization = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField()
    patients = models.ManyToManyField("Patient", blank=True)
    hospital = models.ForeignKey("Hospital", on_delete=models.CASCADE, default=0)


class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    province = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=500)

class Health_classification_result(models.Model):
    id = models.AutoField(primary_key=True)
    theta = models.JSONField()
    precision = models.FloatField()

class Mortality_classification_result(models.Model):
    id = models.AutoField(primary_key=True)
    theta = models.JSONField()
    recall = models.FloatField()

class ECG_classification_result(models.Model):
    id = models.AutoField(primary_key=True)
    theta = models.JSONField()
    precision = models.FloatField()