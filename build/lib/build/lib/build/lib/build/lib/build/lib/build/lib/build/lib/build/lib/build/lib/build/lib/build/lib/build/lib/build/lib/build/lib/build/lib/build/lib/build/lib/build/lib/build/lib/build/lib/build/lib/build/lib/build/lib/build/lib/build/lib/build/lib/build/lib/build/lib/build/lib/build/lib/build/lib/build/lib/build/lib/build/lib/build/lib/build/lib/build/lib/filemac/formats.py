# multimedia_cli/formats.py
from .colors import CYAN, DBLUE, DMAGENTA, DYELLOW, RESET

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
SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "ogg",
                           "flv", "avi", "ogv", "matroska", "mov", "webm",
                           "aac", "bpf", "aiff", "flac"]
SUPPORTED_AUDIO_FORMATS_SHOW = f'''
|==============================|
|  {DBLUE}Supported I/O formats {RESET}      |
|==============================|
|          {CYAN} wav {DYELLOW}               |
|          {CYAN} mp3 {DYELLOW}               |
|          {CYAN} ogg {DYELLOW}               |
|          {CYAN} flv {DYELLOW}               |
|          {CYAN} ogv {DYELLOW}               |
|          {CYAN} matroska {DYELLOW}          |
|          {CYAN} mov {DYELLOW}               |
|          {CYAN} webm {DYELLOW}              |
|          {CYAN} aac {DYELLOW}               |
|          {CYAN} bpf {DYELLOW}               |
--------------------------------
'''

SUPPORTED_VIDEO_FORMATS = ["MP4",
                           "AVI",
                           "OGV",
                           "WEBM",
                           "MOV",
                           "MKV",
                           "FLV",
                           "WMV"]

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
    "JPEG": ".jpg",
    "PNG": ".png",
    "GIF": ".gif",
    "BM": ".bmp",
    "TIFF": ".tiff",
    "EXR": ".exr",
    "PDF": ".pdf",
    "WebP": ".webp",
    "ICNS": ".icns",
    "PSD": ".psd",
    "SVG": ".svg",
    "EPS": ".eps",
    "PostSciript": ".ps"}

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
