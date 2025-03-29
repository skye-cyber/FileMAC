# multimedia_cli/formats.py
from utils.colors import foreground, background

fcl = foreground()
bcl = background()
RESET = fcl.RESET

SUPPORTED_DOC_FORMATS = f"""
|---------------------------------------------------------------------------
|{bcl.BBLUE_BG}Input format{RESET}                    |{bcl.BBLUE_BG}Output format{RESET}                             |
|________________________________|__________________________________________|
|   xlsx    {fcl.BYELLOW_FG}-------------------->{RESET}|csv txt doc/docx db(sql)                  |
|                                |                                          |
|   doc/docx{fcl.BYELLOW_FG}-------------------->{RESET}|txt pdf ppt/pptx audio(ogg)               |
|                                |                                          |
|   txt     {fcl.BYELLOW_FG}-------------------->{RESET}|pdf docx/doc audio(ogg)                   |
|                                |                                          |
|   pdf     {fcl.BYELLOW_FG}-------------------->{RESET}|doc/docx txt audio(ogg)                   |
|                                |                                          |
|   pptx/ppt{fcl.BYELLOW_FG}-------------------->{RESET}|doc/docx                                  |
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
|  {bcl.BBLUE_BG}Supported I/O formats {RESET}      |
|==============================|
|          {fcl.CYAN_FG} wav {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} mp3 {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} ogg {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} flv {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} ogv {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} mov {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} webm {fcl.BYELLOW_FG}              |
|          {fcl.CYAN_FG} aac {fcl.BYELLOW_FG}-------------->|{bcl.IMAGENTA_BG}Pending Implementation{RESET}{fcl.BYELLOW_FG}
|          {fcl.CYAN_FG} bpf {fcl.BYELLOW_FG}-------------->|{bcl.IMAGENTA_BG}Pending Implementation{RESET}{fcl.BYELLOW_FG}
|          {fcl.CYAN_FG} m4a {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} raw {fcl.BYELLOW_FG}               |
|          {fcl.CYAN_FG} aiff {fcl.BYELLOW_FG}              |
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
|x| {bcl.BBLUE_BG}Supported I/O formats{RESET}             |x|
|x|-----------------------------------{fcl.BYELLOW_FG}|x|
|x|               {fcl.BMAGENTA_FG} MP4 {fcl.BYELLOW_FG}               |x|
|x|               {fcl.BMAGENTA_FG} AVI {fcl.BYELLOW_FG}               |x|
|x|               {fcl.BMAGENTA_FG} OGV {fcl.BYELLOW_FG}-------------->|x|{fcl.IMAGENTA_FG}Pending Implementation{RESET}{fcl.BYELLOW_FG}
|x|               {fcl.BMAGENTA_FG} WEBM{fcl.BYELLOW_FG}               |x|
|x|               {fcl.BMAGENTA_FG} MOV {fcl.BYELLOW_FG}               |x|
|x|               {fcl.BMAGENTA_FG} MKV {fcl.BYELLOW_FG}               |x|
|x|               {fcl.BMAGENTA_FG} FLV {fcl.BYELLOW_FG}               |x|
|x|               {fcl.BMAGENTA_FG} WMV {fcl.BYELLOW_FG}-------------->|x|{fcl.IMAGENTA_FG}Pending Implementation{RESET}{fcl.BYELLOW_FG}
|,|___________________.BMAGENTA_FG________________|,|{fcl.BYELLOW_FG}
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
|x|{bcl.BBLUE_BG}Supported I/O formats{RESET}                |x|
|x|_____________________________________{fcl.BYELLOW_FG}|x|
|x|               {fcl.BMAGENTA_FG} JPEG {fcl.BYELLOW_FG}                |x|
|x|               {fcl.BMAGENTA_FG} PNG  {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} GIF  {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} BMP  {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} DIB  {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} TIFF {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} PIC  {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} EXR  {fcl.FMAGENTA_FG}---------------->|x|{fcl.FCYAN_FG} Pending Implementation{RESET}{fcl.BYELLOW_FG}
|x|               {fcl.BMAGENTA_FG} PDF  {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} WebP {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} ICNS {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} PSD  {fcl.FMAGENTA_FG}---------------->|x|{fcl.FCYAN_FG} Pending Implementation{RESET}{fcl.BYELLOW_FG}
|x|               {fcl.BMAGENTA_FG} SVG  {fcl.FMAGENTA_FG}---------------->|x|{fcl.FCYAN_FG} Pending Implementation{RESET}{fcl.BYELLOW_FG}
|x|               {fcl.BMAGENTA_FG} EPS  {fcl.BYELLOW_FG}                 |x|
|x|               {fcl.BMAGENTA_FG} Postscript {fcl.FMAGENTA_FG}---------->|x|{fcl.FCYAN_FG} Pending Implementation{RESET}{fcl.BYELLOW_FG}
|x|               {fcl.BMAGENTA_FG} PICT {fcl.FMAGENTA_FG}---------------->|x|{fcl.FCYAN_FG} Pending Implementation{RESET}{fcl.BYELLOW_FG}
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
