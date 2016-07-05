from django.contrib import admin

# Register your models here.
from tktv.form.models import FormData, Form


class FormAdmin(admin.ModelAdmin):
    list_display = ('id','submenu','name','title','type')

class FormDataAdmin(admin.ModelAdmin):
    list_display = ('id','user','form','value')

admin.site.register(Form, FormAdmin)
admin.site.register(FormData, FormDataAdmin)