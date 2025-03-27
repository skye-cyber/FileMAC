# multimedia_cli/formats.py
from utils.colors import (
    CYAN,
    BBLUE,
    BMAGENTA,
    BYELLOW,
    FCYAN,
    FYELLOW,
    IMAGENTA,
    RESET,
)

SUPPORTED_DOC_FORMATS = f"""
|---------------------------------------------------------------------------
|{BBLUE}Input format{RESET}                    |{BBLUE}Output format{RESET}                             |
|________________________________|__________________________________________|
|   xlsx    {BYELLOW}-------------------->{RESET}|csv txt doc/docx db(sql)                  |
|                                |                                          |
|   doc/docx{BYELLOW}-------------------->{RESET}|txt pdf ppt/pptx audio(ogg)               |
|                                |                                          |
|   txt     {BYELLOW}-------------------->{RESET}|pdf docx/doc audio(ogg)                   |
|                                |                                          |
|   pdf     {BYELLOW}-------------------->{RESET}|doc/docx txt audio(ogg)                   |
|                                |                                          |
|   pptx/ppt{BYELLOW}-------------------->{RESET}|doc/docx                                  |
|                                                                           |
|___________________________________________________________________________|
"""


# Add supported input and output formats for each media type
SUPPORTED_AUDIO_FORMATS = [
    "wav",  # Waveform Audio File Format
    "mp3",  # MPEG Audio Layer III
    "ogg",
    "flv",
    "ogv",
    "webm",
    "aiff",
    "flac",
    "m4a",
    "raw",
    "bpf",
    "aac",
]  # Advanced Audio Codec]  (Free Lossless Audio Codec)

SUPPORTED_AUDIO_FORMATS_DIRECT = [
    "mp3",
    "wav",
    "raw",
    "ogg",
    "aiff",
    "flac",
    "flv",  # Flash Video
    "webm",
    "ogv",
]  # Video
SUPPORTED_AUDIO_FORMATS_SHOW = f"""
|==============================|
|  {BBLUE}Supported I/O formats {RESET}      |
|==============================|
|          {CYAN} wav {BYELLOW}               |
|          {CYAN} mp3 {BYELLOW}               |
|          {CYAN} ogg {BYELLOW}               |
|          {CYAN} flv {BYELLOW}               |
|          {CYAN} ogv {BYELLOW}               |
|          {CYAN} mov {BYELLOW}               |
|          {CYAN} webm {BYELLOW}              |
|          {CYAN} aac {BYELLOW}-------------->|{IMAGENTA}Pending Implementation{RESET}{BYELLOW}
|          {CYAN} bpf {BYELLOW}-------------->|{IMAGENTA}Pending Implementation{RESET}{BYELLOW}
|          {CYAN} m4a {BYELLOW}               |
|          {CYAN} raw {BYELLOW}               |
|          {CYAN} aiff {BYELLOW}              |
--------------------------------

"""

SUPPORTED_VIDEO_FORMATS = [
    "MP4",  # MPEG-4 part 14 Bitrate - 860kb/s
    "AVI",  # Audio Video Interleave
    "OGV",
    "WEBM",
    "MOV",  # QuickTime video Bitrate - 1.01mb/s
    "MKV",  # Matroska video - MKV is known for its support of high-quality content. Bitrate-1.01mb/s
    "FLV",  # Flash video Bitrate
    "WMV",
]


Video_codecs = {
    "MP4": "mpeg4",
    "AVI": "rawvideo",
    # "OGV": "avc",
    "WEBM": "libvpx",
    "MOV": "mpeg4",  # QuickTime video
    "MKV": "mpeg4",  # Matroska video
    "FLV": "flv",
    # "WMV": "WMV"
}
SUPPORTED_VIDEO_FORMATS_SHOW = f"""
,_______________________________________,
|x| {BBLUE}Supported I/O formats{RESET}             |x|
|x|-----------------------------------{BYELLOW}|x|
|x|               {BMAGENTA} MP4 {BYELLOW}               |x|
|x|               {BMAGENTA} AVI {BYELLOW}               |x|
|x|               {BMAGENTA} OGV {BYELLOW}-------------->|x|{IMAGENTA}Pending Implementation{RESET}{BYELLOW}
|x|               {BMAGENTA} WEBM{BYELLOW}               |x|
|x|               {BMAGENTA} MOV {BYELLOW}               |x|
|x|               {BMAGENTA} MKV {BYELLOW}               |x|
|x|               {BMAGENTA} FLV {BYELLOW}               |x|
|x|               {BMAGENTA} WMV {BYELLOW}-------------->|x|{IMAGENTA}Pending Implementation{RESET}{BYELLOW}
|,|___________________________________|,|{BYELLOW}
"""

SUPPORTED_IMAGE_FORMATS = {
    "JPEG": ".jpeg",  # Joint Photographic Experts Group -Lossy compression
    "JPG": ".jpg",
    "PNG": ".png",  # Joint Photographic Experts Group - not lossy
    "GIF": ".gif",  # Graphics Interchange Format
    "BMP": ".bmp",  # Windows BMP image
    "DIB": ".dib",  # Windows BMP image
    "TIFF": ".tiff",  # Tagged Image File Format A flexible and high-quality image format that supports lossless compression
    "PIC": ".pic",
    "PDF": ".pdf",
    "WEBP": ".webp",
    "EPS": ".eps",
    "ICNS": ".icns",  # MacOS X icon
    # Waiting Implementation 👇
    "PSD": ".psd",
    "SVG": ".svg",  # Scalable vector Graphics
    "EXR": ".exr",
    "DXF": ".dxf",  # Autocad format 2D
    "PICT": "pct",
    "PS": ".ps",  # PostSciript
    "POSTSCRIPT": ".ps",
}

SUPPORTED_IMAGE_FORMATS_SHOW = f"""
__________________________________________
|x|{BBLUE}Supported I/O formats{RESET}                |x|
|x|_____________________________________{BYELLOW}|x|
|x|               {BMAGENTA} JPEG {BYELLOW}                |x|
|x|               {BMAGENTA} PNG  {BYELLOW}                 |x|
|x|               {BMAGENTA} GIF  {BYELLOW}                 |x|
|x|               {BMAGENTA} BMP  {BYELLOW}                 |x|
|x|               {BMAGENTA} DIB  {BYELLOW}                 |x|
|x|               {BMAGENTA} TIFF {BYELLOW}                 |x|
|x|               {BMAGENTA} PIC  {BYELLOW}                 |x|
|x|               {BMAGENTA} EXR  {FYELLOW}---------------->|x|{FCYAN} Pending Implementation{RESET}{BYELLOW}
|x|               {BMAGENTA} PDF  {BYELLOW}                 |x|
|x|               {BMAGENTA} WebP {BYELLOW}                 |x|
|x|               {BMAGENTA} ICNS {BYELLOW}                 |x|
|x|               {BMAGENTA} PSD  {FYELLOW}---------------->|x|{FCYAN} Pending Implementation{RESET}{BYELLOW}
|x|               {BMAGENTA} SVG  {FYELLOW}---------------->|x|{FCYAN} Pending Implementation{RESET}{BYELLOW}
|x|               {BMAGENTA} EPS  {BYELLOW}                 |x|
|x|               {BMAGENTA} Postscript {FYELLOW}---------->|x|{FCYAN} Pending Implementation{RESET}{BYELLOW}
|x|               {BMAGENTA} PICT {FYELLOW}---------------->|x|{FCYAN} Pending Implementation{RESET}{BYELLOW}
|_|_____________________________________|x|
"""

SUPPORTED_DOCUMENT_FORMATS = [
    "pdf",
    "doc",
    "docx",
    "csv",
    "xlsx",
    "xls",
    "ppt",
    "pptx",
    "txt",
    "ogg",
    "mp3",
    "audio",
]
