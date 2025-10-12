# multimedia_cli/formats
from .colors import fg, bg, rs


RESET = rs

SUPPORTED_DOC_FORMATS = f"""
|---------------------------------------------------------------------------
|{bg.BBLUE_BG}Input format{RESET}                    |{bg.BBLUE_BG}Output format{RESET}                             |
|________________________________|__________________________________________|
|   xlsx    {fg.BYELLOW_FG}-------------------->{RESET}|csv txt doc/docx db(sql)                  |
|                                |                                          |
|   doc/docx{fg.BYELLOW_FG}-------------------->{RESET}|txt pdf ppt/pptx audio(ogg)               |
|                                |                                          |
|   txt     {fg.BYELLOW_FG}-------------------->{RESET}|pdf docx/doc audio(ogg)                   |
|                                |                                          |
|   pdf     {fg.BYELLOW_FG}-------------------->{RESET}|doc/docx txt audio(ogg)                   |
|                                |                                          |
|   pptx/ppt{fg.BYELLOW_FG}-------------------->{RESET}|doc/docx                                  |
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
|  {bg.BBLUE_BG}Supported I/O formats {RESET}      |
|==============================|
|          {fg.CYAN_FG} wav {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} mp3 {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} ogg {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} flv {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} ogv {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} mov {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} webm {fg.BYELLOW_FG}              |
|          {fg.CYAN_FG} aac {fg.BYELLOW_FG}-------------->|{bg.IMAGENTA_BG}Pending Implementation{RESET}{fg.BYELLOW_FG}
|          {fg.CYAN_FG} bpf {fg.BYELLOW_FG}-------------->|{bg.IMAGENTA_BG}Pending Implementation{RESET}{fg.BYELLOW_FG}
|          {fg.CYAN_FG} m4a {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} raw {fg.BYELLOW_FG}               |
|          {fg.CYAN_FG} aiff {fg.BYELLOW_FG}              |
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
|x| {bg.BBLUE_BG}Supported I/O formats{RESET}             |x|
|x|-----------------------------------{fg.BYELLOW_FG}|x|
|x|               {fg.BMAGENTA_FG} MP4 {fg.BYELLOW_FG}               |x|
|x|               {fg.BMAGENTA_FG} AVI {fg.BYELLOW_FG}               |x|
|x|               {fg.BMAGENTA_FG} OGV {fg.BYELLOW_FG}-------------->|x|{fg.IMAGENTA_FG}Pending Implementation{RESET}{fg.BYELLOW_FG}
|x|               {fg.BMAGENTA_FG} WEBM{fg.BYELLOW_FG}               |x|
|x|               {fg.BMAGENTA_FG} MOV {fg.BYELLOW_FG}               |x|
|x|               {fg.BMAGENTA_FG} MKV {fg.BYELLOW_FG}               |x|
|x|               {fg.BMAGENTA_FG} FLV {fg.BYELLOW_FG}               |x|
|x|               {fg.BMAGENTA_FG} WMV {fg.BYELLOW_FG}-------------->|x|{fg.IMAGENTA_FG}Pending Implementation{RESET}{fg.BYELLOW_FG}
|,|___________________.BMAGENTA_FG________________|,|{fg.BYELLOW_FG}
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
|x|{bg.BBLUE_BG}Supported I/O formats{RESET}                |x|
|x|_____________________________________{fg.BYELLOW_FG}|x|
|x|               {fg.BMAGENTA_FG} JPEG {fg.BYELLOW_FG}                |x|
|x|               {fg.BMAGENTA_FG} PNG  {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} GIF  {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} BMP  {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} DIB  {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} TIFF {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} PIC  {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} EXR  {fg.FMAGENTA_FG}---------------->|x|{fg.FCYAN_FG} Pending Implementation{RESET}{fg.BYELLOW_FG}
|x|               {fg.BMAGENTA_FG} PDF  {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} WebP {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} ICNS {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} PSD  {fg.FMAGENTA_FG}---------------->|x|{fg.FCYAN_FG} Pending Implementation{RESET}{fg.BYELLOW_FG}
|x|               {fg.BMAGENTA_FG} SVG  {fg.FMAGENTA_FG}---------------->|x|{fg.FCYAN_FG} Pending Implementation{RESET}{fg.BYELLOW_FG}
|x|               {fg.BMAGENTA_FG} EPS  {fg.BYELLOW_FG}                 |x|
|x|               {fg.BMAGENTA_FG} Postscript {fg.FMAGENTA_FG}---------->|x|{fg.FCYAN_FG} Pending Implementation{RESET}{fg.BYELLOW_FG}
|x|               {fg.BMAGENTA_FG} PICT {fg.FMAGENTA_FG}---------------->|x|{fg.FCYAN_FG} Pending Implementation{RESET}{fg.BYELLOW_FG}
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
