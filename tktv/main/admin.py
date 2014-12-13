from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User
from tktv.main.models import UserProfile, UserGrade, Main, TopLogo, TopBannerLeft, TopBannerRight, SideBannerLeft, \
    SideBannerRight, SubMenu, MainMenu

# Register your models here.

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

class UserAdmin(AuthUserAdmin):
    list_display = ('id','username','first_name','is_active','date_joined')
    inlines = [UserProfileInline]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user','src','grade')

class UserGradeAdmin(admin.ModelAdmin):
    list_display = ('id','grade')

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id','name')

class TopLogoAdmin(admin.ModelAdmin):
    list_display = ('id','src','url')

class TopBannerLeftAdmin(admin.ModelAdmin):
    list_display = ('id','src','url')

class TopBannerRightAdmin(admin.ModelAdmin):
    list_display = ('id','src','url')

class SideBannerLeftAdmin(admin.ModelAdmin):
    list_display = ('id','src','url')

class SideBannerRightAdmin(admin.ModelAdmin):
    list_display = ('id','src','url')

class MainAdmin(admin.ModelAdmin):
    list_display = ('id','title')
    inlines = [TopLogoInline, TopBannerLeftInline, TopBannerRightInline, SideBannerLeftInline, SideBannerRightInline]

class MainMenuAdmin(admin.ModelAdmin):
    list_display = ('id','name','order','url')

class SubMenuAdmin(admin.ModelAdmin):
    list_display = ('id','main_menu','name','order','url')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserGrade, UserGradeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TopLogo, TopLogoAdmin)
admin.site.register(TopBannerLeft, TopBannerLeftAdmin)
admin.site.register(TopBannerRight, TopBannerRightAdmin)
admin.site.register(SideBannerLeft, SideBannerLeftAdmin)
admin.site.register(SideBannerRight, SideBannerRightAdmin)
admin.site.register(Main, MainAdmin)
admin.site.register(MainMenu, MainMenuAdmin)
admin.site.register(SubMenu, SubMenuAdmin)