from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Doctor,Patient,Comment,Questionaire
from .forms import DoctorAdminChangeForm, DoctorAdminCreationForm
# Register your models here.


 
admin.site.site_header = 'Predict Koa Admin Panel'
admin.site.site_title = 'Predict Koa'

admin.site.unregister(Group)
admin.site.register(Doctor)
admin.site.register(Patient)   
admin.site.register(Questionaire)
admin.site.register(Comment)