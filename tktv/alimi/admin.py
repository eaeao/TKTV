from django.contrib import admin

# Register your models here.
from tktv.alimi.models import Shop, ShopDevice


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id','sid','password','name','alimi_url','event_url')

class ShopDeviceAdmin(admin.ModelAdmin):
    list_display = ('id','sid','uid','is_admin')

admin.site.register(Shop, ShopAdmin)
admin.site.register(ShopDevice, ShopDeviceAdmin)