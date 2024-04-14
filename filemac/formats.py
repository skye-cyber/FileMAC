# multimedia_cli/formats.py

SUPPORTED_DOC_FORMATS = """
|---------------------------------------------------------------------------
|\033[1;94mInput format\033[0m                    |\033[1;94mOutput format\033[0m                             |
|________________________________|__________________________________________|
|   xlsx    \033[1;93m-------------------->\033[0m|csv txt doc/docx db(sql)                  |
|                                |                                          |
|   doc/docx\033[1;93m-------------------->\033[0m|txt pdf ppt/pptx audio(ogg)               |
|                                |                                          |
|   txt     \033[1;93m-------------------->\033[0m|pdf docx/doc audio(ogg)                   |
|                                |                                          |
|   pdf     \033[1;93m-------------------->\033[0m|doc/docx txt audio(ogg)                   |
|                                |                                          |
|   pptx/ppt\033[1;93m-------------------->\033[0m|doc/docx                                  |
|                                                                           |
|___________________________________________________________________________|
"""


def p():
    print(SUPPORTED_DOC_FORMATS)


# Add supported input and output formats for each media type
SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "ogg",
                           "flv", "avi", "ogv", "matroska", "mov", "webm",
                           "aac", "bpf", "aiff", "flac"]
SUPPORTED_AUDIO_FORMATS_SHOW = '''
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
|  \033[1;94mSupported I/O formats \033[0m    |
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
|          wav               |
|          mp3               |
|          ogg               |
|          flv               |
|          ogv               |
|          matroska          |
|          mov               |
|          webm              |
|          aac               |
|          bpf               |
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
'''

SUPPORTED_VIDEO_FORMATS = ["MP4",
                           "AVI",
                           "OGV",
                           "WEBM",
                           "MOV",
                           "MKV",
                           "FLV",
                           "WMV"]

SUPPORTED_VIDEO_FORMATS_SHOW = '''
,_______________________________________,
|x| \033[1;94mSupported I/O formats\033[0m             |x|
|x|-----------------------------------\033[1;93m|x|
|x|              \033[1;95m MP4 \033[1;93m                |x|
|x|               \033[1;95mAVI \033[1;93m                |x|
|x|               \033[1;95mOGV \033[1;93m                |x|
|x|               \033[1;95mWEBM\033[1;93m                |x|
|x|               \033[1;95mMOV \033[1;93m                |x|
|x|               \033[1;95mMKV \033[1;93m                |x|
|x|               \033[1;95mFLV \033[1;93m                |x|
|x|               \033[1;95mWMV \033[1;93m                |x|
|,|___________________________________|,|\033[1;93m
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

SUPPORTED_IMAGE_FORMATS_SHOW = '''
__________________________________________
|x|\033[1;94mSupported I/O formats\033[0m                |x|
|x|_____________________________________\033[1;93m|x|
|x|               \033[1;95mJPEG\033[1;93m                  |x|
|x|               \033[1;95mPNG\033[1;93m                   |x|
|x|               \033[1;95mGIF\033[1;93m                   |x|
|x|               \033[1;95mBM\033[1;93m                    |x|
|x|               \033[1;95mTIFF\033[1;93m                  |x|
|x|               \033[1;95mEXR\033[1;93m                   |x|
|x|               \033[1;95mPDF\033[1;93m                   |x|
|x|               \033[1;95mWebP\033[1;93m                  |x|
|x|               \033[1;95mICNS \033[1;93m                 |x|
|x|               \033[1;95mPSD \033[1;93m                  |x|
|x|               \033[1;95mSVG \033[1;93m                  |x|
|x|               \033[1;95mEPS\033[1;93m                   |x|
|x|               \033[1;95mPostscript \033[1;93m           |x|
|_|_____________________________________|x|
'''

SUPPORTED_DOCUMENT_FORMATS = [...]
