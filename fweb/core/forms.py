from django import forms


class FileUploadForm(forms.Form):
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}), required=True
    )
    target_format = forms.ChoiceField(required=False)
    use_extras = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        tool_config = kwargs.pop("tool_config", {})
        super().__init__(*args, **kwargs)

        # Dynamically set choices based on tool
        if "format_choices" in tool_config:
            self.fields["target_format"].choices = tool_config["format_choices"]


class DocumentConversionForm(FileUploadForm):
    isolate = forms.CharField(required=False, max_length=50)
    threads = forms.IntegerField(required=False, min_value=1, max_value=10, initial=3)
    preserve_quality = forms.BooleanField(required=False, initial=True)


class ImageConversionForm(FileUploadForm):
    quality = forms.IntegerField(required=False, min_value=1, max_value=100, initial=85)
    width = forms.IntegerField(required=False, min_value=1)
    height = forms.IntegerField(required=False, min_value=1)
    size_limit = forms.CharField(required=False, max_length=20)


class AudioConversionForm(FileUploadForm):
    bitrate = forms.ChoiceField(
        choices=[
            ("128", "128 kbps"),
            ("192", "192 kbps"),
            ("256", "256 kbps"),
            ("320", "320 kbps"),
        ],
        initial="192",
    )
    sample_rate = forms.ChoiceField(
        choices=[("44100", "44.1 kHz"), ("48000", "48 kHz"), ("96000", "96 kHz")],
        initial="44100",
    )


class VideoConversionForm(FileUploadForm):
    quality = forms.ChoiceField(
        choices=[
            ("high", "High Quality"),
            ("medium", "Medium Quality"),
            ("low", "Low Quality"),
            ("original", "Original Quality"),
        ],
        initial="medium",
    )
    resolution = forms.ChoiceField(
        choices=[
            ("original", "Original"),
            ("4k", "4K (3840x2160)"),
            ("1080p", "1080p (1920x1080)"),
            ("720p", "720p (1280x720)"),
        ],
        initial="original",
    )


class OCRForm(FileUploadForm):
    language = forms.ChoiceField(
        choices=[
            ("eng", "English"),
            ("spa", "Spanish"),
            ("fra", "French"),
            ("deu", "German"),
            ("multi", "Multiple Languages"),
        ],
        initial="eng",
    )
    output_format = forms.ChoiceField(
        choices=[
            ("txt", "Plain Text"),
            ("docx", "Word Document"),
            ("pdf", "PDF Document"),
        ],
        initial="txt",
    )
    preserve_layout = forms.BooleanField(required=False, initial=True)
