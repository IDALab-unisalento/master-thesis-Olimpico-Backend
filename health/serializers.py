from rest_framework import serializers
from health.models import Hospital, Doctor, Patient, Health_Data, ECG_Entry, Health_classification_entry, \
    Mortality_classification_entry, Health_classification_result, Mortality_classification_result, \
    ECG_classification_result


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id', 'name', 'country', 'city', 'province', 'address', 'postal_code', 'phone_number', 'email')


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
        'id', 'name', 'surname', 'username', 'password', 'profile_photo', 'birthday', 'specialization', 'phone_number',
        'email', 'patients', 'hospital')


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
        'id', 'name', 'surname', 'sex', 'hypertensive', 'diabetes', 'username', 'password', 'profile_photo', 'birthday',
        'fiscal_code', 'phone_number', 'email', 'doctors')


class Health_DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health_Data
        fields = (
        'id', 'datetime', 'heartbeat', 'systole', 'diastole', 'oxygen_saturation', 'breathing_rate', 'blood_glucose',
        'temperature', 'chest_pain_type',
        'serum_cholestoral', 'exercise_induced_angina', 'ST_depress_induced_by_exercise_relative_to_rest',
        'health_classification',
        'bmi', 'atrial_fibrillation', 'leucocyte', 'urea_nitrogen', 'anion_gap', 'bicarbonate', 'lactic_acid',
        'mortality_risk', 'ECG_classification',
        'hospitalization_risk', 'patient')


class ECG_EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ECG_Entry
        fields = ('id', 'value', 'ECG_classification', 'health_data')


class Health_Classification_EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Health_classification_entry
        fields = ('intercept', 'age', 'sex', 'chest_pain_type', 'blood_pressure', 'serum_cholestoral',
                  'blood_sugar', 'ecg_classification', 'heartbeat', 'exercise_induced_angina',
                  'ST_depress_induced_by_exercise_relative_to_rest', 'health_classification', 'health_data')


class Mortality_Classification_EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mortality_classification_entry
        fields = (
        'intercept', 'age', 'sex', 'bmi', 'hypertensive', 'atrial_fibrillation', 'diabetes', 'heartbeat', 'systole',
        'diastole', 'breathing_rate', 'temperature', 'oxygen_saturation',
        'leucocyte', 'urea_nitrogen', 'blood_glucose', 'anion_gap', 'bicarbonate', 'lactic_acid', 'mortality_risk',
        'health_data')


class HealthClass_ResultSerializer(serializers.Serializer):
    class Meta:
        model = Health_classification_result
        fields = ("id", "theta", "precision")


class MortalityClass_ResultSerializer(serializers.Serializer):
    class Meta:
        model = Mortality_classification_result
        fields = ("id", "theta", "recall")


class ECGClass_ResultSerializer(serializers.Serializer):
    class Meta:
        model = ECG_classification_result
        fields = ("id", "theta", "precision")
