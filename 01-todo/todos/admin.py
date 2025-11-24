from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'due_date']
    search_fields = ['title', 'description']
