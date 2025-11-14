import cairosvg


class SVGConverter:
    """
    A utility class for converting SVG files to various formats using CairoSVG.
    Supported formats: PNG, PDF, SVG (optimized).
    """

    @staticmethod
    def to_png(input_svg: str, output_path: str, is_string: bool = False):
        """
        Convert SVG to PNG.
        :param input_svg: Path to SVG file or raw SVG string.
        :param output_path: Output PNG file path.
        :param is_string: Set True if input_svg is raw SVG data.
        """
        if is_string:
            cairosvg.svg2png(bytestring=input_svg.encode(), write_to=output_path)
        else:
            cairosvg.svg2png(url=input_svg, write_to=output_path)

    @staticmethod
    def to_pdf(input_svg: str, output_path: str, is_string: bool = False):
        """
        Convert SVG to PDF.
        :param input_svg: Path to SVG file or raw SVG string.
        :param output_path: Output PDF file path.
        :param is_string: Set True if input_svg is raw SVG data.
        """
        if is_string:
            cairosvg.svg2pdf(bytestring=input_svg.encode(), write_to=output_path)
        else:
            cairosvg.svg2pdf(url=input_svg, write_to=output_path)

    @staticmethod
    def to_svg(input_svg: str, output_path: str, is_string: bool = False):
        """
        Convert/Optimize SVG to SVG.
        :param input_svg: Path to SVG file or raw SVG string.
        :param output_path: Output SVG file path.
        :param is_string: Set True if input_svg is raw SVG data.
        """
        if is_string:
            cairosvg.svg2svg(bytestring=input_svg.encode(), write_to=output_path)
        else:
            cairosvg.svg2svg(url=input_svg, write_to=output_path)
