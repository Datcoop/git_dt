from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export import resources,fields,widgets
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.contrib.auth.hashers import make_password

# Register your models here.

class UserResource(resources.ModelResource):

    def before_import_row(self,row, **kwargs):
        password = row['password']
        row['password'] = make_password(password)

    class Meta: 
        model = User

        exclude = ('id', )
        import_id_fields = ['username'] 

class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    list_display = ('username','dni')
    search_fields = ['username','dni']
    resource_class = UserResource 

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )

#Registrar  Usuarios en el panel administrativo

admin.site.register(Task, TaskAdmin)

admin.site.register(Contacto)

admin.site.register(Tasas)


