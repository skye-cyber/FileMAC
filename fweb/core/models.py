from django.db import models
from django.contrib.auth.models import User


class ProcessingJob(models.Model):
    JOB_STATUS = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    job_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tool_id = models.CharField(max_length=50)
    input_files = models.JSONField()  # List of input file paths
    output_files = models.JSONField(default=list)  # List of output file paths
    status = models.CharField(max_length=20, choices=JOB_STATUS, default="pending")
    progress = models.IntegerField(default=0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.job_id} - {self.tool_id} - {self.status}"


class ProcessedFile(models.Model):
    job = models.ForeignKey(ProcessingJob, on_delete=models.CASCADE)
    original_name = models.CharField(max_length=255)
    processed_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_name} -> {self.processed_name}"
