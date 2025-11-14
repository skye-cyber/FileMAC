# multimedia_cli/formats
from .colors import fg, bg, rs


RESET = rs

SUPPORTED_DOC_FORMATS = f"""
|---------------------------------------------------------------------------
|{bg.BBLUE}Input format{RESET}                    |{bg.BBLUE}Output format{RESET}                             |
|________________________________|__________________________________________|
|   xlsx    {fg.BYELLOW}-------------------->{RESET}|csv txt doc/docx db(sql)                  |
|                                |                                          |
|   doc/docx{fg.BYELLOW}-------------------->{RESET}|txt pdf ppt/pptx audio(ogg)               |
|                                |                                          |
|   txt     {fg.BYELLOW}-------------------->{RESET}|pdf docx/doc audio(ogg)                   |
|                                |                                          |
|   pdf     {fg.BYELLOW}-------------------->{RESET}|doc/docx txt audio(ogg)                   |
|                                |                                          |
|   pptx/ppt{fg.BYELLOW}-------------------->{RESET}|doc/docx                                  |
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
|  {bg.BBLUE}Supported I/O formats {RESET}      |
|==============================|
|          {fg.CYAN} wav {fg.BYELLOW}               |
|          {fg.CYAN} mp3 {fg.BYELLOW}               |
|          {fg.CYAN} ogg {fg.BYELLOW}               |
|          {fg.CYAN} flv {fg.BYELLOW}               |
|          {fg.CYAN} ogv {fg.BYELLOW}               |
|          {fg.CYAN} mov {fg.BYELLOW}               |
|          {fg.CYAN} webm {fg.BYELLOW}              |
|          {fg.CYAN} aac {fg.BYELLOW}-------------->|{bg.IMAGENTA}Pending Implementation{RESET}{fg.BYELLOW}
|          {fg.CYAN} bpf {fg.BYELLOW}-------------->|{bg.IMAGENTA}Pending Implementation{RESET}{fg.BYELLOW}
|          {fg.CYAN} m4a {fg.BYELLOW}               |
|          {fg.CYAN} raw {fg.BYELLOW}               |
|          {fg.CYAN} aiff {fg.BYELLOW}              |
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
|x| {bg.BBLUE}Supported I/O formats{RESET}             |x|
|x|-----------------------------------{fg.BYELLOW}|x|
|x|               {fg.BMAGENTA} MP4 {fg.BYELLOW}               |x|
|x|               {fg.BMAGENTA} AVI {fg.BYELLOW}               |x|
|x|               {fg.BMAGENTA} OGV {fg.BYELLOW}-------------->|x|{fg.IMAGENTA}Pending Implementation{RESET}{fg.BYELLOW}
|x|               {fg.BMAGENTA} WEBM{fg.BYELLOW}               |x|
|x|               {fg.BMAGENTA} MOV {fg.BYELLOW}               |x|
|x|               {fg.BMAGENTA} MKV {fg.BYELLOW}               |x|
|x|               {fg.BMAGENTA} FLV {fg.BYELLOW}               |x|
|x|               {fg.BMAGENTA} WMV {fg.BYELLOW}-------------->|x|{fg.IMAGENTA}Pending Implementation{RESET}{fg.BYELLOW}
|,|___________________.BMAGENTA________________|,|{fg.BYELLOW}
"""

SUPPORTED_IMAGE_FORMATS = {
    "JPEG": ".jpeg",  # Joint Photographic Experts Group -Lossy compression
    "JPG": ".jpg",  # Joint Photographic Experts Group - not lossy
    "PNG": ".png",
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
    "PICT": ".pct",
    "PS": ".ps",  # PostSciript
    "POSTSCRIPT": ".ps",
}

SUPPORTED_IMAGE_FORMATS_SHOW = f"""
__________________________________________
|x|{bg.BBLUE}Supported I/O formats{RESET}                |x|
|x|_____________________________________{fg.BYELLOW}|x|
|x|               {fg.BMAGENTA} JPEG {fg.BYELLOW}                |x|
|x|               {fg.BMAGENTA} PNG  {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} GIF  {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} BMP  {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} DIB  {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} TIFF {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} PIC  {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} EXR  {fg.FMAGENTA}---------------->|x|{fg.FCYAN} Pending Implementation{RESET}{fg.BYELLOW}
|x|               {fg.BMAGENTA} PDF  {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} WebP {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} ICNS {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} PSD  {fg.FMAGENTA}---------------->|x|{fg.FCYAN} Pending Implementation{RESET}{fg.BYELLOW}
|x|               {fg.BMAGENTA} SVG  {fg.FMAGENTA}---------------->|x|{fg.FCYAN} Pending Implementation{RESET}{fg.BYELLOW}
|x|               {fg.BMAGENTA} EPS  {fg.BYELLOW}                 |x|
|x|               {fg.BMAGENTA} Postscript {fg.FMAGENTA}---------->|x|{fg.FCYAN} Pending Implementation{RESET}{fg.BYELLOW}
|x|               {fg.BMAGENTA} PICT {fg.FMAGENTA}---------------->|x|{fg.FCYAN} Pending Implementation{RESET}{fg.BYELLOW}
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
