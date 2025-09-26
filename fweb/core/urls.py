from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.Dashboard, name="dashboard"),
    path("dashboard/", views.Dashboard, name="get_dashboard"),
    path("tools/<str:category>/", views.CategoryTools, name="category_tools"),
    path("process/batch/", views.BatchProcessing, name="batch_processing"),
    # API endpoints
    path("api/process/<str:tool_id>/", views.process_tool, name="process_tool"),
    path("api/progress/<str:job_id>/", views.get_progress, name="get_progress"),
    path("api/tool/<str:tool_id>/", views.get_tool_config, name="get_tool_config"),
    path("download/<str:filename>/", views.download_file, name="download_file"),
    # Specific tool endpoints (for backward compatibility)
    # path("convert/doc/", views.ConvertDoc, name="convert_doc"),
    # path("convert/image/", views.ConvertImgae, name="convert_image"),
    # path("convert/video/", views.ConvertVideo, name="convert_video"),
    # path("convert/audio/", views.ConvertAudio, name="convert_audio"),
]
