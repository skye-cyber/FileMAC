from django.contrib import admin
from .models import ProcessingJob, ProcessedFile


@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ("job_id", "tool_id", "user", "status", "progress", "created_at")
    list_filter = ("status", "tool_id", "created_at")
    search_fields = ("job_id", "tool_id", "user__username")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("job_id", "user", "tool_id", "status", "progress")}),
        ("Files", {"fields": ("input_files", "output_files")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
        ("Error", {"fields": ("error_message",), "classes": ("collapse",)}),
    )


@admin.register(ProcessedFile)
class ProcessedFileAdmin(admin.ModelAdmin):
    list_display = (
        "original_name",
        "processed_name",
        "job",
        "file_size",
        "processed_at",
    )
    list_filter = ("job__tool_id", "processed_at")
    search_fields = ("original_name", "processed_name", "job__job_id")
    readonly_fields = ("processed_at",)
