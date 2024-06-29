# multimedia_cli/formats.py
from .colors import CYAN, DBLUE, DMAGENTA, DYELLOW, IMAGENTA, RESET

SUPPORTED_DOC_FORMATS = f"""
|---------------------------------------------------------------------------
|{DBLUE}Input format{RESET}                    |{DBLUE}Output format{RESET}                             |
|________________________________|__________________________________________|
|   xlsx    {DYELLOW}-------------------->{RESET}|csv txt doc/docx db(sql)                  |
|                                |                                          |
|   doc/docx{DYELLOW}-------------------->{RESET}|txt pdf ppt/pptx audio(ogg)               |
|                                |                                          |
|   txt     {DYELLOW}-------------------->{RESET}|pdf docx/doc audio(ogg)                   |
|                                |                                          |
|   pdf     {DYELLOW}-------------------->{RESET}|doc/docx txt audio(ogg)                   |
|                                |                                          |
|   pptx/ppt{DYELLOW}-------------------->{RESET}|doc/docx                                  |
|                                                                           |
|___________________________________________________________________________|
"""


def p():
    print(SUPPORTED_DOC_FORMATS)


# Add supported input and output formats for each media type
SUPPORTED_AUDIO_FORMATS = ["wav",  # Waveform Audio File Format
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
                           "aac"]  # Advanced Audio Codec]  (Free Lossless Audio Codec)

SUPPORTED_AUDIO_FORMATS_DIRECT = ["mp3",
                                  "wav",
                                  "raw",
                                  "ogg",
                                  "aiff",
                                  "flac",
                                  "flv",  # Flash Video
                                  "webm",
                                  "ogv"]  # Video
SUPPORTED_AUDIO_FORMATS_SHOW = f'''
|==============================|
|  {DBLUE}Supported I/O formats {RESET}      |
|==============================|
|          {CYAN} wav {DYELLOW}               |
|          {CYAN} mp3 {DYELLOW}               |
|          {CYAN} ogg {DYELLOW}               |
|          {CYAN} flv {DYELLOW}               |
|          {CYAN} ogv {DYELLOW}               |
|          {CYAN} mov {DYELLOW}               |
|          {CYAN} webm {DYELLOW}              |
|          {CYAN} aac {DYELLOW}-------------->|{IMAGENTA}Pending Implementation{RESET}{DYELLOW}
|          {CYAN} bpf {DYELLOW}-------------->|{IMAGENTA}Pending Implementation{RESET}{DYELLOW}
|          {CYAN} m4a {DYELLOW}               |
|          {CYAN} raw {DYELLOW}               |
|          {CYAN} aiff {DYELLOW}              |
--------------------------------

'''

SUPPORTED_VIDEO_FORMATS = ["MP4",  # MPEG-4 part 14 Bitrate - 860kb/s
                           "AVI",  # Audio Video Interleave
                           "OGV",
                           "WEBM",
                           "MOV",  # QuickTime video Bitrate - 1.01mb/s
                           "MKV",  # Matroska video - MKV is known for its support of high-quality content. Bitrate-1.01mb/s
                           "FLV",  # Flash video Bitrate
                           "WMV"]


Video_codecs = {
                    "MP4": "mpeg4",
                    "AVI": "rawvideo",
                    # "OGV": "avc",
                    "WEBM": "libvpx",
                    "MOV": "mpeg4",  # QuickTime video
                    "MKV": "mpeg4",  # Matroska video
                    "FLV": "flv"
                    # "WMV": "WMV"
                }
SUPPORTED_VIDEO_FORMATS_SHOW = f'''
,_______________________________________,
|x| {DBLUE}Supported I/O formats{RESET}             |x|
|x|-----------------------------------{DYELLOW}|x|
|x|               {DMAGENTA} MP4 {DYELLOW}               |x|
|x|               {DMAGENTA} AVI {DYELLOW}               |x|
|x|               {DMAGENTA} OGV {DYELLOW}               |x|
|x|               {DMAGENTA} WEBM{DYELLOW}               |x|
|x|               {DMAGENTA} MOV {DYELLOW}               |x|
|x|               {DMAGENTA} MKV {DYELLOW}               |x|
|x|               {DMAGENTA} FLV {DYELLOW}               |x|
|x|               {DMAGENTA} WMV {DYELLOW}               |x|
|,|___________________________________|,|{DYELLOW}
'''

SUPPORTED_IMAGE_FORMATS = {
    "JPEG": ".jpg",  # Joint Photographic Experts Group -Lossy compression
    "PNG": ".png",  # Joint Photographic Experts Group - not lossy
    "GIF": ".gif",  # Graphics Interchange Format
    "BM": ".bmp",
    "BMP": ".dib",
    "DXF": ".dxf",  # Autocad format 2D
    "TIFF": ".tiff",  # Tagged Image File Format A flexible and high-quality image format that supports lossless compression
    "EXR": ".exr",
    "pic": ".pic",
    "pict": "pct",
    "PDF": ".pdf",
    "WebP": ".webp",
    "ICNS": ".icns",
    "PSD": ".psd",
    "SVG": ".svg",  # Scalable vector Graphics
    "EPS": ".eps",
    "PostSciript": ".ps",
    "PS": ".ps"}

SUPPORTED_IMAGE_FORMATS_SHOW = f'''
__________________________________________
|x|{DBLUE}Supported I/O formats{RESET}                |x|
|x|_____________________________________{DYELLOW}|x|
|x|               {DMAGENTA} JPEG {DYELLOW}                |x|
|x|               {DMAGENTA} PNG {DYELLOW}                 |x|
|x|               {DMAGENTA} GIF {DYELLOW}                 |x|
|x|               {DMAGENTA} BM {DYELLOW}                  |x|
|x|               {DMAGENTA} TIFF {DYELLOW}                |x|
|x|               {DMAGENTA} EXR {DYELLOW}                 |x|
|x|               {DMAGENTA} PDF {DYELLOW}                 |x|
|x|               {DMAGENTA} WebP{DYELLOW}                 |x|
|x|               {DMAGENTA} ICNS {DYELLOW}                |x|
|x|               {DMAGENTA} PSD {DYELLOW}                 |x|
|x|               {DMAGENTA} SVG {DYELLOW}                 |x|
|x|               {DMAGENTA} EPS {DYELLOW}                 |x|
|x|               {DMAGENTA} Postscript {DYELLOW}          |x|
|_|_____________________________________|x|
'''

SUPPORTED_DOCUMENT_FORMATS = ['pdf', 'doc', 'docx', 'csv', 'xlsx', 'xls',
                              'ppt', 'pptx', 'txt', 'ogg', 'mp3', 'audio']
