from django.contrib import admin

# Register your models here.
from .models import Tour
from django.contrib import admin
from .models import MonthlyPick

admin.site.register(Tour)



@admin.register(MonthlyPick)
class MonthlyPickAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'month')
    list_filter = ('month', 'country')
    search_fields = ('city', 'country', 'description')
