from django.contrib import admin

# Register your models here.
from tktv.board.models import BoardImg, Board, BoardReply


class BoardImgInline(admin.StackedInline):
    model = BoardImg
    can_delete = True

class BoardAdmin(admin.ModelAdmin):
    list_display = ('id','submenu','user','title','con','hits','is_headline','date_updated')
    inlines = [BoardImgInline]


class BoardImgAdmin(admin.ModelAdmin):
    list_display = ('id','board','src','is_visible')


class BoardReplyAdmin(admin.ModelAdmin):
    list_display = ('id','board','user','con','date_updated')

admin.site.register(Board, BoardAdmin)
admin.site.register(BoardImg, BoardImgAdmin)
admin.site.register(BoardReply, BoardReplyAdmin)