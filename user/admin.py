from django.contrib import admin
from .models import Album, Cart, Category, Music, Group_music, Rate_music, Bill
# Register your models here.
class InlineGroup_music(admin.TabularInline):
    model = Group_music
class AlbumAdmin(admin.ModelAdmin):
    inlines = [InlineGroup_music]
    list_display = ['Name', 'Description']
    list_filter = ['Name']
    search_fields = ['Name']
admin.site.register(Album, AlbumAdmin)
class MusicAdmin(admin.ModelAdmin):
    inlines = [InlineGroup_music]
    list_display = ['Name', 'Singer', 'CategoryID']
    list_filter = ['Singer']
    search_fields = ['Name']
admin.site.register(Music, MusicAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Description']
    list_filter = ['Name']
    search_fields = ['Name']
admin.site.register(Category, CategoryAdmin)
class Rate_musicAdmin(admin.ModelAdmin):
    list_display = ['UserID', 'Music_ID']
    list_filter = ['Music_ID']
    search_fields = ['Music_ID']
admin.site.register(Rate_music, Rate_musicAdmin)
class BillAdmin(admin.ModelAdmin):
    list_display = ['Date', 'Shipped', 'UserID']
    list_filter = ['Shipped']
    search_fields = ['Date']
admin.site.register(Bill, BillAdmin)