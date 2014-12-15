# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from tktv.page.models import PageImg, Page


class PageImgInline(admin.StackedInline):
    model = PageImg
    can_delete = True

class PageAdmin(admin.ModelAdmin):
    list_display = ('id','submenu','con','date_updated')
    inlines = [PageImgInline]

admin.site.register(Page, PageAdmin)