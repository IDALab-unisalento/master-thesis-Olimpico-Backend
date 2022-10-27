from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from health.models import Hospital, Doctor, Patient, Health_Data, ECG_Entry, Health_classification_entry, Mortality_classification_entry
from health.serializers import HospitalSerializer, DoctorSerializer, PatientSerializer, Health_DataSerializer, \
    ECG_EntrySerializer, Health_Classification_EntrySerializer, Mortality_Classification_EntrySerializer
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
import math
import csv

@csrf_exempt
def hospitalAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            hospitals = Hospital.objects.all()
            hospitals_serializer = HospitalSerializer(hospitals, many=True)
            return JsonResponse(hospitals_serializer.data, safe=False)
        else:
            hospital = Hospital.objects.get(id=id)
            hospital_serializer = HospitalSerializer(hospital)
            return JsonResponse(hospital_serializer.data, safe=False)
    elif request.method == 'POST':
        hospital_data = JSONParser().parse(request)
        hospitals_serializer = HospitalSerializer(data=hospital_data)
        if hospitals_serializer.is_valid():
            hospitals_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to add", safe=False)
    elif request.method == 'PUT':
        hospital_data = JSONParser().parse(request)
        hospital = Hospital.objects.get(id=hospital_data['id'])
        hospital_serializer = HospitalSerializer(hospital, data=hospital_data)
        if hospital_serializer.is_valid():
            hospital_serializer.save()
            return JsonResponse("Update successfully", safe=False)
        return JsonResponse("Failed to update", safe=False)
    elif request.method == 'DELETE':
        hospital = Hospital.objects.get(id=id)
        hospital.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def health_classAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            import csv
            resp =  []
            with open(r"C:\Users\solimpico\Desktop\health_project\health\AI\parameters\health_parameters.csv", newline="", encoding="ISO-8859-1") as filecsv:
                lettore = csv.reader(filecsv, delimiter=",")
                for row in lettore:
                    for element in row:
                        resp.append(element)
            return JsonResponse(resp, safe=False)
        else:
            return JsonResponse("Bad Request", safe=False)
    else:
        return JsonResponse("Bad Request", safe=False)

@csrf_exempt
def mortality_classAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            import csv
            resp = []
            with open(r"C:\Users\solimpico\Desktop\health_project\health\AI\parameters\mortality_parameters.csv",
                      newline="", encoding="ISO-8859-1") as filecsv:
                lettore = csv.reader(filecsv, delimiter=",")
                for row in lettore:
                    for element in row:
                        resp.append(element)
            return JsonResponse(resp, safe=False)
        else:
            return JsonResponse("Bad Request", safe=False)
    else:
        return JsonResponse("Bad Request", safe=False)

@csrf_exempt
def ecg_classAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            import csv
            resp = []
            with open(r"C:\Users\solimpico\Desktop\health_project\health\AI\parameters\ecg_parameters.csv",
                      newline="", encoding="ISO-8859-1") as filecsv:
                lettore = csv.reader(filecsv, delimiter=",")
                for row in lettore:
                    for element in row:
                        resp.append(element)
            return JsonResponse(resp, safe=False)
        else:
            return JsonResponse("Bad Request", safe=False)
    else:
        return JsonResponse("Bad Request", safe=False)

@csrf_exempt
def doctorAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            doctors = Doctor.objects.all()
            doctors_serializer = DoctorSerializer(doctors, many=True)
            return JsonResponse(doctors_serializer.data, safe=False)
        else:
            doctor = Doctor.objects.get(id=id)
            doctor_serializer = DoctorSerializer(doctor)
            return JsonResponse(doctor_serializer.data, safe=False)
    elif request.method == 'POST':
        doctor_data = JSONParser().parse(request)
        doctors_serializer = DoctorSerializer(data=doctor_data)
        if doctors_serializer.is_valid():
            doctors_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        print(doctors_serializer.errors)
        return JsonResponse("Failed to add", safe=False)
    elif request.method == 'PUT':
        doctor_data = JSONParser().parse(request)
        doctor = Doctor.objects.get(id=doctor_data['id'])
        doctor_serializer = DoctorSerializer(doctor, data=doctor_data)
        if doctor_serializer.is_valid():
            doctor_serializer.save()
            return JsonResponse("Update successfully", safe=False)
        return JsonResponse("Failed to update", safe=False)
    elif request.method == 'DELETE':
        doctor = Doctor.objects.get(id=id)
        doctor.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def patient_health_dataAPI(request):
    if request.method == 'POST':
        patientId = JSONParser().parse(request)
        health_data = Health_Data.objects.all().filter(patient=patientId['id'])
        health_data_serializer = Health_DataSerializer(health_data, many=True)
        return JsonResponse(health_data_serializer.data, safe=False)

@csrf_exempt
def doctorsPatientsAPI(request):
    if request.method == 'POST':
        doctorId = JSONParser().parse(request)
        doctor = Doctor.objects.get(id=doctorId['id'])
        patients = Patient.objects.all().filter(doctors=doctor)
        patient_serializer = PatientSerializer(patients, many=True)
        print(patients)
        return JsonResponse(patient_serializer.data, safe=False)

@csrf_exempt
def health_dataAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            health_data_saved = Health_Data.objects.all()
            health_data_serializer = Health_DataSerializer(health_data_saved, many=True)
            return JsonResponse(health_data_serializer.data, safe=False)
        else:
            health_data_saved = Health_Data.objects.get(id=id)
            health_data_serializer = Health_DataSerializer(health_data_saved)
            return JsonResponse(health_data_serializer.data, safe=False)
    elif request.method == 'POST':
        health_data = JSONParser().parse(request)
        health_data_serializer = Health_DataSerializer(data=health_data)
        if health_data_serializer.is_valid():
            health_data_saved = health_data_serializer.save()
            patient = Patient.objects.get(id = health_data_saved.patient.id)

            #aggiorno health_classification_entry
            health_c_e = Health_classification_entry()
            health_c_e.intercept = 1
            health_c_e.age = math.trunc((date.today() - patient.birthday).days/365)
            health_c_e.sex = patient.sex
            health_c_e.chest_pain_type = health_data_saved.chest_pain_type
            health_c_e.blood_pressure= health_data_saved.systole
            health_c_e.serum_cholestoral = health_data_saved.serum_cholestoral
            if(health_data_saved.blood_glucose>120):
                health_c_e.blood_sugar = 1
            else:
                health_c_e.blood_sugar=0
            if(health_data_saved.ECG_classification==1):
                health_c_e.ecg_classification=0
            elif health_data_saved.ECG_classification==3:
                health_c_e.ecg_classification=1
            else:
                health_c_e.ecg_classification=2
            health_c_e.heartbeat = health_data_saved.heartbeat
            health_c_e.exercise_induced_angina = health_data_saved.exercise_induced_angina
            health_c_e.ST_depress_induced_by_exercise_relative_to_rest = health_data_saved.ST_depress_induced_by_exercise_relative_to_rest
            if(health_data_saved.health_classification>=0.5):
                health_c_e.health_classification = 1
            else:
                health_c_e.health_classification = 0
            health_c_e.health_data = health_data_saved
            health_c_e.save()
            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\health_dataset.csv', 'w',newline='') as csvfile:
                writer = csv.writer(csvfile)
                for entry in Health_classification_entry.objects.all().values_list('intercept','age', 'sex',
                                                                                  'chest_pain_type','blood_pressure',
                                                                                  'serum_cholestoral','blood_sugar',
                                                                                  'ecg_classification','heartbeat',
                                                                                  'exercise_induced_angina',
                                                                                  'ST_depress_induced_by_exercise_relative_to_rest',
                                                                                  'health_classification'):
                    writer.writerow(entry)

            #aggiorno mortality_classification_entry
            mortality_c_e = Mortality_classification_entry()
            mortality_c_e.intercept=1
            mortality_c_e.age = math.trunc((date.today() - patient.birthday).days/365)
            if(patient.sex==1):
                mortality_c_e.sex=1
            if(patient.sex==0):
                patient.sex=2
            mortality_c_e.bmi = health_data_saved.bmi
            mortality_c_e.hypertensive = patient.hypertensive
            mortality_c_e.atrial_fibrillation = health_data_saved.atrial_fibrillation
            mortality_c_e.diabetes = patient.diabetes
            mortality_c_e.heartbeat = health_data_saved.heartbeat
            mortality_c_e.systole = health_data_saved.systole
            mortality_c_e.diastole = health_data_saved.diastole
            mortality_c_e.breathing_rate = health_data_saved.breathing_rate
            mortality_c_e.temperature = health_data_saved.temperature
            mortality_c_e.oxygen_saturation = health_data_saved.oxygen_saturation
            mortality_c_e.leucocyte = health_data_saved.leucocyte
            mortality_c_e.urea_nitrogen = health_data_saved.urea_nitrogen
            mortality_c_e.blood_glucose = health_data_saved.blood_glucose
            mortality_c_e.anion_gap = health_data_saved.anion_gap
            mortality_c_e.lactic_acid = health_data_saved.lactic_acid
            mortality_c_e.bicarbonate = health_data_saved.bicarbonate
            if (health_data_saved.mortality_risk >= 0.5):
                mortality_c_e.mortality_risk = 1
            else:
                mortality_c_e.mortality_risk = 0
            mortality_c_e.health_data = health_data_saved
            mortality_c_e.save()
            #creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\mortality_dataset.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for entry in Mortality_classification_entry.objects.all().values_list('intercept','age','sex','bmi','hypertensive','atrial_fibrillation','diabetes','heartbeat','systole', 'diastole', 'breathing_rate', 'temperature','oxygen_saturation','leucocyte','urea_nitrogen','blood_glucose','anion_gap','bicarbonate','lactic_acid','mortality_risk'):
                    writer.writerow(entry)

            return JsonResponse(health_data_serializer.data, safe=False)
        print(health_data_serializer.errors)
        return JsonResponse("Failed to add", safe=False)
    elif request.method == 'PUT':
        health_data_data = JSONParser().parse(request)
        health_data_saved = Health_Data.objects.get(id=health_data_data['id'])
        health_data_serializer = Health_DataSerializer(health_data_saved, data=health_data_data)
        if health_data_serializer.is_valid():
            health_data_saved = health_data_serializer.save()
            patient = Patient.objects.get(id=health_data_saved.patient.id)
            # aggiorno health_classification_entry
            print(health_data_saved)
            health_c_e = Health_classification_entry.objects.get(health_data=health_data_saved)
            health_c_e.intercept = 1
            health_c_e.age = math.trunc((date.today() - patient.birthday).days / 365)
            health_c_e.sex = patient.sex
            health_c_e.chest_pain_type = health_data_saved.chest_pain_type
            health_c_e.blood_pressure = health_data_saved.systole
            health_c_e.serum_cholestoral = health_data_saved.serum_cholestoral
            if (health_data_saved.blood_glucose > 120):
                health_c_e.blood_sugar = 1
            else:
                health_c_e.blood_sugar = 0
            if (health_data_saved.ECG_classification == 1):
                health_c_e.ecg_classification = 0
            elif health_data_saved.ECG_classification == 3:
                health_c_e.ecg_classification = 1
            else:
                health_c_e.ecg_classification = 2
            health_c_e.heartbeat = health_data_saved.heartbeat
            health_c_e.exercise_induced_angina = health_data_saved.exercise_induced_angina
            health_c_e.ST_depress_induced_by_exercise_relative_to_rest = health_data_saved.ST_depress_induced_by_exercise_relative_to_rest
            if (health_data_saved.health_classification >= 0.5):
                health_c_e.health_classification = 1
            else:
                health_c_e.health_classification = 0
            health_c_e.health_data = health_data_saved
            health_c_e.save()
            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\health_dataset.csv', 'w',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                for entry in Health_classification_entry.objects.all().values_list('intercept', 'age', 'sex',
                                                                                  'chest_pain_type', 'blood_pressure',
                                                                                  'serum_cholestoral', 'blood_sugar',
                                                                                  'ecg_classification', 'heartbeat',
                                                                                  'exercise_induced_angina',
                                                                                  'ST_depress_induced_by_exercise_relative_to_rest',
                                                                                  'health_classification'):
                    writer.writerow(entry)

            # aggiorno mortality_classification_entry
            mortality_c_e = Mortality_classification_entry.objects.get(health_data = health_data_saved)
            mortality_c_e.intercept = 1
            mortality_c_e.age = math.trunc((date.today() - patient.birthday).days / 365)
            mortality_c_e.sex = patient.sex
            mortality_c_e.bmi = health_data_saved.bmi
            mortality_c_e.hypertensive = patient.hypertensive
            mortality_c_e.atrial_fibrillation = health_data_saved.atrial_fibrillation
            mortality_c_e.diabetes = patient.diabetes
            mortality_c_e.heartbeat = health_data_saved.heartbeat
            mortality_c_e.systole = health_data_saved.systole
            mortality_c_e.diastole = health_data_saved.diastole
            mortality_c_e.breathing_rate = health_data_saved.breathing_rate
            mortality_c_e.temperature = health_data_saved.temperature
            mortality_c_e.oxygen_saturation = health_data_saved.oxygen_saturation
            mortality_c_e.leucocyte = health_data_saved.leucocyte
            mortality_c_e.urea_nitrogen = health_data_saved.urea_nitrogen
            mortality_c_e.blood_glucose = health_data_saved.blood_glucose
            mortality_c_e.anion_gap = health_data_saved.anion_gap
            mortality_c_e.lactic_acid = health_data_saved.lactic_acid
            mortality_c_e.bicarbonate = health_data_saved.bicarbonate
            if (health_data_saved.mortality_risk >= 0.5):
                mortality_c_e.mortality_risk = 1
            else:
                mortality_c_e.mortality_risk = 0
            mortality_c_e.health_data = health_data_saved
            mortality_c_e.save()
            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\mortality_dataset.csv', 'w',newline='') as csvfile:
                writer = csv.writer(csvfile)
                for entry in Mortality_classification_entry.objects.all().values_list('intercept', 'age', 'sex', 'bmi',
                                                                                     'hypertensive',
                                                                                     'atrial_fibrillation', 'diabetes',
                                                                                     'heartbeat', 'systole', 'diastole',
                                                                                     'breathing_rate', 'temperature',
                                                                                     'oxygen_saturation', 'leucocyte',
                                                                                     'urea_nitrogen', 'blood_glucose',
                                                                                     'anion_gap', 'bicarbonate','lactic_acid',
                                                                                     'mortality_risk'):
                    writer.writerow(entry)
                    print(health_data_serializer.data)
            return JsonResponse(health_data_serializer.data, safe=False)
        return JsonResponse("Failed to update", safe=False)
    elif request.method == 'DELETE':
        health_data_saved = Health_Data.objects.get(id=id)
        health_data_saved.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def patientAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            patients = Patient.objects.all()
            patients_serializer = PatientSerializer(patients, many=True)
            return JsonResponse(patients_serializer.data, safe=False)
        else:
            patient = Patient.objects.get(id=id)
            patient_serializer = PatientSerializer(patient)
            return JsonResponse(patient_serializer.data, safe=False)
    elif request.method == 'POST':
        patient_data = JSONParser().parse(request)
        patient_serializer = PatientSerializer(data=patient_data)
        patient_serializer.is_valid()
        s = patient_serializer
        if s.is_valid():
            patient_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        print(s.errors)
        return JsonResponse("Failed to add", safe=False)
    elif request.method == 'PUT':
        patient_data = JSONParser().parse(request)
        patient = Patient.objects.get(id=patient_data['id'])
        patient_serializer = PatientSerializer(patient, data=patient_data)
        if patient_serializer.is_valid():
            patient_serializer.save()
            return JsonResponse("Update successfully", safe=False)
        return JsonResponse("Failed to update", safe=False)
    elif request.method == 'DELETE':
        patient = Patient.objects.get(id=id)
        patient.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def ecg_entryAPI(request, id=0):
    if request.method == 'GET':
        if id == 0:
            ecg_entries = ECG_Entry.objects.all()
            ecg_entries_serializer = ECG_EntrySerializer(ecg_entries, many=True)
            return JsonResponse(ecg_entries_serializer.data, safe=False)
        else:
            health_data = Health_Data.objects.get(id=id)
            ecg_entry = ECG_Entry.objects.all()
            for e in ecg_entry:
                if(e.health_data == health_data):
                    ecg_entry_serializer = ECG_EntrySerializer(e)
                    break
            return JsonResponse(ecg_entry_serializer.data, safe=False)
    elif request.method == 'POST':
        ecg_entry_data = JSONParser().parse(request)
        ecg_entry_serializer = ECG_EntrySerializer(data=ecg_entry_data)
        if ecg_entry_serializer.is_valid():
            ecg_entry_saved = ecg_entry_serializer.save()
            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\ecg_dataset.csv', 'a+',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                r = []
                for entry in ecg_entry_saved.value:
                    r.append(entry)
                r.append(ecg_entry_saved.ECG_classification)
                writer.writerow(r)
            return JsonResponse(ecg_entry_serializer.data, safe=False)
        print(ecg_entry_serializer.errors)
        return JsonResponse("Failed to add", safe=False)
    elif request.method == 'PUT':
        ecg_entry_data = JSONParser().parse(request)
        ecg_entry = ECG_Entry.objects.get(id=ecg_entry_data['id'])
        ecg_entry_serializer = ECG_EntrySerializer(ecg_entry, data=ecg_entry_data)
        if ecg_entry_serializer.is_valid():
            ecg_entry_serializer.save()
            # creating csv
            with open(r'C:\Users\solimpico\Desktop\health_project\health\AI\datasets\ecg_dataset.csv', 'a+',
                      newline='') as csvfile:
                writer = csv.writer(csvfile)
                r = []
                for entry in ECG_Entry.objects.get(id=ecg_entry_data['id']).value:
                #for entry in ECG_Entry.objects.all().values_list('value', 'ECG_classification'):
                    r.append(entry)
                r.append(ECG_Entry.objects.get(id=ecg_entry_data['id']).ECG_classification)
                writer.writerow(r)
            return JsonResponse(ecg_entry_serializer.data, safe=False)
        return JsonResponse("Failed to update", safe=False)
    elif request.method == 'DELETE':
        ecg_entry = ECG_Entry.objects.get(id=id)
        ecg_entry.delete()
        return JsonResponse("Deleted Successfully", safe=False)

@csrf_exempt
def user_loginAPI(request):
    if request.method == 'POST':
        login = JSONParser().parse(request)
        try:
            user = Patient.objects.get(username = login['username'])
            type = 'patient'
        except ObjectDoesNotExist:
            try:
                user = Doctor.objects.get(username = login['username'])
                type = 'doctor'
            except ObjectDoesNotExist:
                return JsonResponse("User not found", safe=False)

        if(user.password == login['password']):
            jwt = "qwertyuiopasdfghjklzxcvbnm"
            session = {"id": user.id, "jwt": jwt, "type": type}
            return JsonResponse(session, safe=False)
        else:
            return JsonResponse("Wrong credentials", safe=False)

@csrf_exempt
def health_entryAPI(request):
    if request.method == 'GET':
        health_entries = Health_classification_entry.objects.all()
        health_entries_serializer = Health_Classification_EntrySerializer(health_entries, many=True)
        return JsonResponse(health_entries_serializer.data, safe=False)
    else:
        return JsonResponse("Element not found", safe=False)

@csrf_exempt
def mortality_entryAPI(request):
    if request.method == 'GET':
        mortality_entries = Mortality_classification_entry.objects.all()
        mortality_entries_serializer = Mortality_Classification_EntrySerializer(mortality_entries, many=True)
        return JsonResponse(mortality_entries_serializer.data, safe=False)
    else:
        return JsonResponse("Element not found", safe=False)

#@csrf_exempt
#def hospitalization_entryAPI(request):
#    if request.method == 'GET':
#        hospitalization_entries = Hospitalization_classification_entry.objects.all()
#        hospitalization_entries_serializer = Hospitalization_Classification_EntrySerializer(health_entries, many=True)
#        return JsonResponse(hospitalization_entries_serializer.data, safe=False)
#    else:
#        return JsonResponse("Element not found", safe=False)


