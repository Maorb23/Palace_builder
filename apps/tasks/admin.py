from django.contrib import admin
from .models import Task, DailySession

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'complexity', 'order', 'is_completed')
    list_filter = ('category', 'is_completed')
    search_fields = ('title',)

@admin.register(DailySession)
class DailySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'palace_theme', 'is_completed')
    list_filter = ('is_completed', 'palace_theme')
    search_fields = ('user__username',) 