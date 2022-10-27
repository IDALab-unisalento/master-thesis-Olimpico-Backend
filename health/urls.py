from django.urls import path
from . import views

urlpatterns = [
    path('hospital/', views.hospitalAPI),
    path('hospital/<int:id>',views.hospitalAPI),
    path('doctor/', views.doctorAPI),
    path('doctor/<int:id>',views.doctorAPI),
    path('patient/', views.patientAPI),
    path('patient/<int:id>', views.patientAPI),
    path('health_data/', views.health_dataAPI),
    path('patient_health_data/', views.patient_health_dataAPI),
    path('doctor_patient/', views.doctorsPatientsAPI),
    path('health_data/<int:id>', views.health_dataAPI),
    path('ecg_entry/', views.ecg_entryAPI),
    path('ecg_entry/<int:id>', views.ecg_entryAPI),
    path('login/', views.user_loginAPI),
    path('health_class_param/', views.health_classAPI),
    path('health_class_param/<int:id>', views.health_classAPI),
    path('mort_class_param/', views.mortality_classAPI),
    path('mort_class_param/<int:id>', views.mortality_classAPI),
    path('ecg_class_param/', views.ecg_classAPI),
    path('ecg_class_param/<int:id>', views.ecg_classAPI),
    path('dead_class/', views.mortality_entryAPI),
    path('health_class/', views.health_entryAPI),
]