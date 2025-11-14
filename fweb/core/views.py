import os
import json
import tempfile
import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Import CLI functionality
import sys
import argparse
from pathlib import Path
from .config import TOOL_CONFIGS

# Add the CLI module to the path
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logger = logging.getLogger("fweb")


def Dashboard(request):
    """Main dashboard view"""
    return render(
        request,
        "core/dashboard.html",
        {
            "category_icon": "tachometer-alt",
            "category_color": "blue",
            "category_description": "File management and processing dashboard",
        },
    )


def Results(request):
    """Results page view"""
    return render(request, "core/results.html")


def CategoryTools(request, category):
    """Category-specific tools view"""
    category = category.lower()
    config = TOOL_CONFIGS.get(category, TOOL_CONFIGS["document"])

    return render(
        request,
        "core/tools/base_tools.html",
        {
            "category": category,
            "category_icon": config["icon"],
            "category_color": config["color"],
            "category_description": config["description"],
            "tools": config["tools"],
        },
    )


def BatchProcessing(request):
    """Batch processing dashboard"""
    return render(
        request,
        "core/tools/base_tools.html",
        {
            "category": "batch",
            "category_icon": TOOL_CONFIGS["batch"]["icon"],
            "category_color": TOOL_CONFIGS["batch"]["color"],
            "category_description": TOOL_CONFIGS["batch"]["description"],
            "tools": TOOL_CONFIGS["batch"]["tools"],
        },
    )


# Processing views
@csrf_exempt
@require_http_methods(["POST"])
def process_tool(request, tool_id):
    """Process files using the specified tool"""
    try:
        # Get uploaded files
        files = request.FILES.getlist("files")
        if not files:
            return JsonResponse({"error": "No files uploaded"}, status=400)

        # Get form data
        form_data = request.POST.dict()

        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            file_paths = []
            for file in files:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, "wb") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                file_paths.append(file_path)

            # Process based on tool ID
            result = process_with_cli(tool_id, file_paths, form_data, temp_dir)

            if result["success"]:
                return JsonResponse(
                    {
                        "success": True,
                        "message": result["message"],
                        "results": result.get("results", []),
                        "download_urls": result.get("download_urls", []),
                    }
                )
            else:
                return JsonResponse(
                    {"success": False, "error": result["error"]}, status=500
                )

    except Exception as e:
        logger.error(f"Error processing tool {tool_id}: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)


def process_with_cli(tool_id, file_paths, form_data, temp_dir):
    """Bridge function to call CLI functionality"""
    try:
        # Import your CLI modules
        from filemac.main import Argsmain  # Adjust import based on your structure

        # Map tool_id to CLI arguments
        cli_args = map_tool_to_cli_args(tool_id, file_paths, form_data)

        # Execute CLI command
        result = execute_cli_command(cli_args, temp_dir)

        return result

    except Exception as e:
        logger.error(f"CLI processing error: {str(e)}")
        return {"success": False, "error": str(e)}


def map_tool_to_cli_args(tool_id, file_paths, form_data):
    """Map web tool to CLI arguments"""
    arg_mapping = {
        "convert_doc": {
            "args": ["--convert_doc"]
            + file_paths
            + ["-tf", form_data.get("target_format", "pdf")],
            "extras": ["--use_extras"] if form_data.get("use_extras") else [],
        },
        "convert_image": {
            "args": ["--convert_image"]
            + file_paths
            + ["-tf", form_data.get("target_format", "png")],
            "extras": [],
        },
        "convert_audio": {
            "args": ["--convert_audio"]
            + file_paths
            + ["-tf", form_data.get("target_format", "mp3")],
            "extras": [],
        },
        "convert_video": {
            "args": ["--convert_video"]
            + file_paths[0]
            + ["-tf", form_data.get("target_format", "mp4")],
            "extras": [],
        },
        "ocr": {
            "args": ["--OCR"] + file_paths,
            "extras": ["-sep", form_data.get("separator", "\\n")]
            if form_data.get("separator")
            else [],
        },
        "pdf_join": {
            "args": ["--pdfjoin"] + file_paths,
            "extras": ["--order", form_data.get("order", "AAB")]
            if form_data.get("order")
            else [],
        },
        "audio_join": {"args": ["--AudioJoin"] + file_paths, "extras": []},
        "extract_audio": {"args": ["-xA", file_paths[0]], "extras": []},
        "analyze_video": {"args": ["-Av", file_paths[0]], "extras": []},
        "resize_image": {
            "args": ["--resize_image"] + file_paths,
            "extras": ["-t_size", form_data.get("target_size")]
            if form_data.get("target_size")
            else [],
        },
        "image2pdf": {
            "args": ["--image2pdf"] + file_paths,
            "extras": ["--sort"] if form_data.get("sort") else [],
        },
        "image2word": {"args": ["--image2word"] + file_paths, "extras": []},
        "image2gray": {"args": ["--image2gray"] + file_paths, "extras": []},
    }

    mapping = arg_mapping.get(tool_id, {"args": [], "extras": []})
    return mapping["args"] + mapping["extras"]


def execute_cli_command(cli_args, temp_dir):
    """Execute the CLI command with the given arguments"""
    try:
        # This is where you'll integrate with your actual CLI code
        # For now, let's create a mock implementation

        # Import your CLI argument handler
        from filemac.main import Cmd_arg_Handler, argsOPMaper

        # Mock execution - replace with actual CLI call
        print(f"Executing CLI command: filemac {' '.join(cli_args)}")

        # Here you would actually call your CLI functionality
        # For demonstration, we'll create mock results

        results = []
        download_urls = []

        for file_path in cli_args[1:]:  # Skip the command argument
            if os.path.isfile(file_path):
                # Create mock output file
                output_file = file_path + ".converted"
                with open(output_file, "w") as f:
                    f.write(f"Converted version of {file_path}")

                results.append(
                    {
                        "original_name": os.path.basename(file_path),
                        "converted_name": os.path.basename(output_file),
                        "status": "success",
                        "size": "1.2 MB",
                    }
                )
                download_urls.append(f"/download/{os.path.basename(output_file)}")

        return {
            "success": True,
            "message": f"Processed {len(results)} files successfully",
            "results": results,
            "download_urls": download_urls,
        }

    except Exception as e:
        logger.error(f"CLI execution error: {str(e)}")
        return {"success": False, "error": str(e)}


# File download view
def download_file(request, filename):
    """Serve processed files for download"""
    file_path = os.path.join(settings.MEDIA_ROOT, "processed", filename)

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response["Content-Disposition"] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found", status=404)


# Progress tracking view
@csrf_exempt
def get_progress(request, job_id):
    """Get processing progress for a job"""
    # Implement progress tracking logic
    return JsonResponse({"progress": 50, "status": "Processing..."})


# Tool configuration API
def get_tool_config(request, tool_id):
    """Get configuration for a specific tool"""
    # Find tool configuration
    for category, config in TOOL_CONFIGS.items():
        for tool in config["tools"]:
            if tool["id"] == tool_id:
                return JsonResponse({"tool": tool, "category": category})

    return JsonResponse({"error": "Tool not found"}, status=404)
