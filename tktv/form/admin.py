from django.contrib import admin

# Register your models here.
from tktv.form.models import Form, FormData, FormImage


class FormAdmin(admin.ModelAdmin):
    list_display = ('id','submenu','name','title','type')

class FormDataAdmin(admin.ModelAdmin):
    list_display = ('id','form','value','date_created')

class FormImageAdmin(admin.ModelAdmin):
    list_display = ('id','form','src')

admin.site.register(Form, FormAdmin)
admin.site.register(FormData, FormDataAdmin)
admin.site.register(FormImage, FormImageAdmin)