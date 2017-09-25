from django.contrib import admin

# Register your models here.
from tktv.page.models import Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('id','submenu','con','date_updated')


admin.site.register(Page, PageAdmin)