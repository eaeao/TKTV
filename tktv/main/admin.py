from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

# Register your models here.
from django.contrib.auth.models import User

from tktv.main.models import UserProfile, TopLogo, TopBannerLeft, TopBannerRight, SideBannerLeft, SideBannerRight, \
    RightBanner, BottomBanner, Main, MainMenu, SubMenu


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = True

class TopLogoInline(admin.StackedInline):
    model = TopLogo
    max_num = 1
    can_delete = True

class TopBannerLeftInline(admin.StackedInline):
    model = TopBannerLeft
    max_num = 1
    can_delete = True

class TopBannerRightInline(admin.StackedInline):
    model = TopBannerRight
    max_num = 1
    can_delete = True

class SideBannerLeftInline(admin.StackedInline):
    model = SideBannerLeft
    max_num = 1
    can_delete = True

class SideBannerRightInline(admin.StackedInline):
    model = SideBannerRight
    max_num = 1
    can_delete = True

class RightBannerInline(admin.StackedInline):
    model = RightBanner
    can_delete = True

class BottomBannerInline(admin.StackedInline):
    model = BottomBanner
    can_delete = True

class UserAdmin(AuthUserAdmin):
    list_display = ('id','username','first_name','is_active','date_joined')
    inlines = [UserProfileInline]

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class MainAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    inlines = [TopLogoInline, TopBannerLeftInline, TopBannerRightInline, SideBannerLeftInline, SideBannerRightInline, RightBannerInline, BottomBannerInline]

class MainMenuAdmin(admin.ModelAdmin):
    list_display = ('id','name','order','url')

class SubMenuAdmin(admin.ModelAdmin):
    list_display = ('id','main_menu','name','order','mode','url','permission_read','permission_write')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Main, MainAdmin)
admin.site.register(MainMenu, MainMenuAdmin)
admin.site.register(SubMenu, SubMenuAdmin)