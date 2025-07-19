from typing import Literal

from fpdf import FPDF

from constants import (
    DISPLAY_WIDTH_PX,
    DISPLAY_HEIGHT_PX,
    DISPLAY_DIAGONAL_INCH,
    LINE_HEIGHT, PDF_FORMAT,
    PDF_INCH_UNIT, PDF_MARGIN_MM,
    PDF_MM_UNIT,
    PDF_PT_UNIT, PDF_PX_UNIT, PDF_TAB_WHITE_SPACE,
    H1_SIZE_PT,
    H2_SIZE_PT,
    H3_SIZE_PT,
    TEXT_SIZE_PT,
)

class PDF:
    """
    A class to create a PDF document using the FPDF library.
    """

    def __init__(
        self,
        unit: Literal["pt", "mm", "cm", "in"] | float = PDF_MM_UNIT,
        page_format: Literal["", "a3", "A3", "a4", "A4", "a5", "A5", "letter", "Letter", "legal", "Legal"] | tuple[float, float] = PDF_FORMAT,
        margin_mm: float = PDF_MARGIN_MM,
        tabs_white_space: int = PDF_TAB_WHITE_SPACE,
        line_height: float = LINE_HEIGHT
    ):
        """
        Initialize the PDF document with a specified format.

        Args:
            unit (Literal["pt", "mm", "cm", "in"] | float): The unit of measurement for the PDF document.
            page_format (Literal["", "a3", "A3", "a4", "A4", "a5", "A5", "letter", "Letter", "legal", "Legal"] | tuple[float, float]): The format of the PDF document.
            margin_mm (float): The margin in millimeters for the PDF document.
            tabs_white_space (int): The number of whitespaces per tab.
        """
        self.__unit = unit
        self.__tabs_white_space = tabs_white_space
        self.__line_height = line_height
        self.pdf = FPDF(unit=unit, format=page_format)
        self.pdf.set_auto_page_break(auto=True, margin=margin_mm)
        self.pdf.set_margins(left=margin_mm, top=margin_mm, right=margin_mm)

        # Initialize the PPI
        self.__ppi = None

        # Initialize the current font size in px
        self.__current_font_size = None

        # Main regular and bold fonts
        self.__main_regular_font = None
        self.__main_bold_font = None

    @staticmethod
    def calculate_ppi(
        display_width_px: int = DISPLAY_WIDTH_PX,
        display_height_px: int = DISPLAY_HEIGHT_PX,
        display_diagonal_inch: float = DISPLAY_DIAGONAL_INCH
    ) -> float:
        """
        Calculate the PPI (dots per inch) of a display based on its dimensions.

        Args:
            display_width_px (int): The width of the display in pixels.
            display_height_px (int): The height of the display in pixels.
            display_diagonal_inch (float): The diagonal size of the display in inches.
        """
        return (
            (display_width_px ** 2 + display_height_px ** 2) ** 0.5
        ) / display_diagonal_inch

    @staticmethod
    def mm_to_px(mm: float, ppi: float) -> float:
        """
        Convert millimeters to pixels based on the PPI.

        Args:
            mm (float): The measurement in millimeters.
            ppi (float): The PPI of the display.

        Returns:
            float: The equivalent measurement in pixels.
        """
        return mm * ppi / 25.4

    @staticmethod
    def mm_to_pt(mm: float) -> float:
        """
        Convert millimeters to points based on the PPI.

        Args:
            mm (float): The measurement in millimeters.

        Returns:
            float: The equivalent measurement in points.
        """
        return mm * 72 / 25.4

    @staticmethod
    def mm_to_in(mm: float) -> float:
        """
        Convert millimeters to inches.

        Args:
            mm (float): The measurement in millimeters.

        Returns:
            float: The equivalent measurement in inches.
        """
        return mm / 25.4

    @staticmethod
    def px_to_mm(px: float, ppi: float) -> float:
        """
        Convert pixels to millimeters based on the PPI.

        Args:
            px (float): The measurement in pixels.
            ppi (float): The PPI of the display.

        Returns:
            float: The equivalent measurement in millimeters.
        """
        return px * 25.4 / ppi

    @staticmethod
    def px_to_pt(px: float, ppi: float) -> float:
        """
        Convert pixels to points based on the PPI.

        Args:
            px (float): The measurement in pixels.
            ppi (float): The PPI of the display.

        Returns:
            float: The equivalent measurement in points.
        """
        return px * 72 / ppi

    @staticmethod
    def px_to_in(px: float, ppi: float) -> float:
        """
        Convert pixels to inches based on the PPI.

        Args:
            px (float): The measurement in pixels.
            ppi (float): The PPI of the display.

        Returns:
            float: The equivalent measurement in inches.
        """
        return px / ppi * 25.4

    @staticmethod
    def pt_to_px(pt: float, ppi: float) -> float:
        """
        Convert points to pixels based on the PPI.

        Args:
            pt (float): The measurement in points.
            ppi (float): The PPI of the display.

        Returns:
            float: The equivalent measurement in pixels.
        """
        return pt * ppi / 72

    @staticmethod
    def pt_to_mm(pt: float) -> float:
        """
        Convert points to millimeters.

        Args:
            pt (float): The measurement in points.

        Returns:
            float: The equivalent measurement in millimeters.
        """
        return pt * 25.4 / 72

    @staticmethod
    def pt_to_in(pt: float) -> float:
        """
        Convert points to inches.

        Args:
            pt (float): The measurement in points.

        Returns:
            float: The equivalent measurement in inches.
        """
        return pt * 72 / 25.4

    @property
    def ppi(self):
        """
        Get the PPI of the PDF document.

        Returns:
            float: The PPI of the PDF document.
        """
        return self.__ppi

    @ppi.setter
    def ppi(self, value: float):
        """
        Set the PPI of the PDF document.

        Args:
            value (float): The PPI value to set.
        """
        if value is None:
            raise ValueError("PPI cannot be None.")
        if value <= 0:
            raise ValueError("PPI must be a positive number.")
        self.__ppi = value

    @property
    def document_size(self):
        """
        Get the size of the PDF document in points.

        Returns:
            tuple: The width and height of the PDF document in points.
        """
        return self.pdf.w, self.pdf.h

    def _check_ppi(self):
        """
        Check if the PPI is set, if not calculate it.
        """
        if self.ppi is None:
            raise ValueError(
                "PPI is not set. Please calculate PPI using calculate_ppi() method."
            )

    def _convert_unit_to_pt(self, value: float, unit: str) -> float:
        """
        Convert a value in the current unit to points.

        Args:
            value (float): The value to convert.
            unit (str): The unit of the value.

        Returns:
            float: The value converted to points.
        """
        if unit == PDF_PT_UNIT:
            return value
        elif unit == PDF_MM_UNIT:
            return self.pt_to_mm(value)
        elif unit == PDF_INCH_UNIT:
            return self.pt_to_in(value)
        elif unit == PDF_PX_UNIT:
            self._check_ppi()
            return self.pt_to_px(value, self.ppi)
        else:
            raise ValueError(f"Unsupported unit: {unit}")

    def _convert_unit_to_px(self, value: float, unit: str) -> float:
        """
        Convert a value in the current unit to pixels.

        Args:
            value (float): The value to convert.
            unit (str): The unit of the value.

        Returns:
            float: The value converted to pixels.
        """
        if unit == PDF_PT_UNIT:
            self._check_ppi()
            return self.pt_to_px(value, self.ppi)
        elif unit == PDF_MM_UNIT:
            self._check_ppi()
            return self.mm_to_px(value, self.ppi)
        elif unit == PDF_INCH_UNIT:
            self._check_ppi()
            return self.px_to_in(value, self.ppi)
        elif unit == PDF_PX_UNIT:
            return value
        else:
            raise ValueError(f"Unsupported unit: {unit}")

    def _convert_unit_to_mm(self, value: float, unit: str) -> float:
        """
        Convert a value in the current unit to millimeters.

        Args:
            value (float): The value to convert.
            unit (str): The unit of the value.

        Returns:
            float: The value converted to millimeters.
        """
        if unit == PDF_PT_UNIT:
            return self.pt_to_mm(value)
        elif unit == PDF_MM_UNIT:
            return value
        elif unit == PDF_INCH_UNIT:
            return self.mm_to_in(value)
        elif unit == PDF_PX_UNIT:
            self._check_ppi()
            return self.px_to_mm(value, self.ppi)
        else:
            raise ValueError(f"Unsupported unit: {unit}")

    def _convert_unit_to_in(self, value: float, unit: str) -> float:
        """
        Convert a value in the current unit to inches.

        Args:
            value (float): The value to convert.
            unit (str): The unit of the value.

        Returns:
            float: The value converted to inches.
        """
        if unit == PDF_PT_UNIT:
            return self.pt_to_in(value)
        elif unit == PDF_MM_UNIT:
            return self.mm_to_in(value)
        elif unit == PDF_INCH_UNIT:
            return value
        elif unit == PDF_PX_UNIT:
            self._check_ppi()
            return self.px_to_in(value, self.ppi)
        else:
            raise ValueError(f"Unsupported unit: {unit}")

    def _convert_unit_to_document_unit(self, value: float, unit: str) -> float:
        """
        Convert a value in the current unit to the document's unit.

        Args:
            value (float): The value to convert.
            unit (str): The unit of the value.

        Returns:
            float: The value converted to the document's unit.
        """
        if self.__unit == PDF_PT_UNIT:
            return self._convert_unit_to_pt(value, unit)
        elif self.__unit == PDF_MM_UNIT:
            return self._convert_unit_to_mm(value, unit)
        elif self.__unit == PDF_INCH_UNIT:
            return self._convert_unit_to_in(value, unit)
        elif self.__unit == PDF_PX_UNIT:
            self._check_ppi()
            return self._convert_unit_to_px(value, unit)
        else:
            raise ValueError(f"Unsupported document unit: {self.__unit}")

    def add_page(self):
        """
        Add a new page to the PDF document.
        """
        self.pdf.add_page()

    def add_font(
        self,
        family: str,
        style: Literal["", "B", "I"] = '',
        filename: str = '',
        uni: bool = False,
        set_as_main: bool = False
    ):
        """
        Add a font to the PDF document.

        Args:
            family (str): The font family name.
            style (Literal["", "B", "I"]): The font style (e.g., 'B' for bold).
            filename (str): The path to the font file.
            uni (bool): Whether to use Unicode encoding.
            set_as_main (bool): Whether to set this font as the main regular or bold font.
        """
        if set_as_main:
            if style == '':
                self.__main_regular_font = family
            elif style == 'B':
                self.__main_bold_font = family
            else:
                raise ValueError("Only regular and bold styles can be set as main fonts.")

        self.pdf.add_font(family, style, filename, uni=uni)

    def set_font(
        self,
        family: str,
        style: Literal["", "B", "I", "U", "BU", "UB", "BI", "IB", "IU", "UI", "BIU", "BUI", "IBU", "IUB", "UBI", "UIB"] = '',
        size: int = TEXT_SIZE_PT,
        unit: str = PDF_PT_UNIT,
    ):
        """
        Set the font for the PDF document.

        Args:
            family (str): The font family name.
            style (Literal["", "B", "I", "U", "BU", "UB", "BI", "IB", "IU", "UI", "BIU", "BUI", "IBU", "IUB", "UBI", "UIB"]): The font style.
            size (int): The font size.
            unit (str): The unit of the font size.
        """
        size_pt = int(self._convert_unit_to_pt(size, unit))
        self.__current_font_size = size_pt
        self.pdf.set_font(family, style, size_pt)

    def set_text_color(
        self,
        r: int = 0,
        g: int = 0,
        b: int = 0
    ):
        """
        Set the multi_cell color for the PDF document.

        Args:
            r (int): Red component of the color (0-255).
            g (int): Green component of the color (0-255).
            b (int): Blue component of the color (0-255).
        """
        self.pdf.set_text_color(r, g, b)

    def set_fill_color(
        self,
        r: int = 0,
        g: int = 0,
        b: int = 0
    ):
        """
        Set the fill color for the PDF document.

        Args:
            r (int): Red component of the color (0-255).
            g (int): Green component of the color (0-255).
            b (int): Blue component of the color (0-255).
        """
        self.pdf.set_fill_color(r, g, b)

    def ln(self, height: float = 0, unit: str = PDF_PT_UNIT):
        """
        Move the cursor to the next line in the PDF document.

        Args:
            height (float): The height of the line.
            unit (str): The unit of the height.
        """
        self.pdf.ln(self._convert_unit_to_document_unit(height, unit))

    def newline(self):
        """
        Add a new line to the PDF document.
        """
        self.ln(self.__current_font_size)

    def cell(
        self,
        width: float,
        height: float = 0,
        unit: str = PDF_PT_UNIT,
        txt: str = '',
        border: Literal[0, 1] | bool | str = 0,
        newline: bool = False,
        align: str = '',
        fill: bool = False
    ):
        """
        Add a cell to the PDF document.

        Args:
            width (float): The width of the cell.
            height (float): The height of the cell.
            unit (str): The unit of the width and height.
            txt (str): The text to display in the cell.
            border (Literal[0, 1] | bool | str): Border style of the cell.
            newline (bool): Line break after the cell.
            align (str): Text alignment within the cell.
            fill (bool): Whether to fill the cell background.
        """
        # Convert the width and height to document unit
        width = self._convert_unit_to_document_unit(width, unit)
        height = self._convert_unit_to_document_unit(height, unit)

        self.pdf.cell(
            w=width,
            h=height * self.__line_height,
            text=txt,
            border=border,
            align=align,
            fill=fill
        )

        if newline:
            self.newline()

    def multi_cell(
        self,
        txt: str = '',
        border: Literal[0, 1] | bool | str = 0,
        align: str = '',
        fill: bool = False,
        tabs: int|None = None,
    ):
        """
        Add a multi-cell to the PDF document.

        Args:
            txt (str): The text to display.
            border (Literal[0, 1] | bool | str): Border style of the text.
            align (str): Text alignment.
            fill (bool): Whether to fill the background.
            tabs (int|None): Optional tabs for text alignment.
            newline (bool): Whether to add a new line after the text.
        """
        tabs_str = ''
        if tabs is not None:
            tabs_str = "".join(
                " " for _ in range(tabs * self.__tabs_white_space)
            )

        # Convert the height to document unit
        height = self._convert_unit_to_document_unit(
            self.__current_font_size,
            PDF_PT_UNIT
        )

        self.pdf.multi_cell(
            w=0,
            h=height * self.__line_height,
            text=tabs_str + txt if tabs_str else txt,
            border=border,
            align=align,
            fill=fill
        )
        self.newline()

    def text(
        self,
        txt: str = '',
        border: Literal[0, 1] | bool | str = 0,
        align: str = '',
        fill: bool = False,
        tabs: int|None = None,
    ):
        """
        Add text to the PDF document.

        Args:
            txt (str): The text to display.
            border (Literal[0, 1] | bool | str): Border style of the text.
            align (str): Text alignment.
            fill (bool): Whether to fill the background.
            tabs (int|None): Optional tabs for text alignment.
        """
        if self.__main_regular_font:
            self.set_font(self.__main_regular_font, '', TEXT_SIZE_PT)
        self.multi_cell(txt, border, align, fill, tabs)

    def h1(
        self,
        txt: str = '',
        border: Literal[0, 1] | bool | str = 0,
        align: str = '',
        fill: bool = False,
        tabs: int|None = None
    ):
        """
        Add a level 1 heading to the PDF document.

        Args:
            txt (str): The text of the heading.
            border (Literal[0, 1] | bool | str): Border style of the heading.
            align (str): Text alignment.
            fill (bool): Whether to fill the background.
            tabs (int|None): Optional tabs for text alignment.
        """
        if self.__main_bold_font:
            self.set_font(self.__main_bold_font, 'B', H1_SIZE_PT)
        self.multi_cell(txt, border, align, fill, tabs)

    def h2(
        self,
        txt: str = '',
        border: Literal[0, 1] | bool | str = 0,
        align: str = '',
        fill: bool = False,
        tabs: int|None = None
    ):
        """
        Add a level 2 heading to the PDF document.

        Args:
            txt (str): The text of the heading.
            border (Literal[0, 1] | bool | str): Border style of the heading.
            align (str): Text alignment.
            fill (bool): Whether to fill the background.
            tabs (int|None): Optional tabs for text alignment.
        """
        if self.__main_bold_font:
            self.set_font(self.__main_bold_font, 'B', H2_SIZE_PT)
        self.multi_cell(txt, border, align, fill, tabs)

    def h3(
        self,
        txt: str = '',
        border: Literal[0, 1] | bool | str = 0,
        align: str = '',
        fill: bool = False,
        tabs: int|None = 1
    ):
        """
        Add a level 3 heading to the PDF document.

        Args:
            txt (str): The text of the heading.
            border (Literal[0, 1] | bool | str): Border style of the heading.
            align (str): Text alignment.
            fill (bool): Whether to fill the background.
            tabs (int|None): Optional tabs for text alignment.
        """
        if self.__main_bold_font:
            self.set_font(self.__main_bold_font, 'B', H3_SIZE_PT)
        self.multi_cell(txt, border, align, fill, tabs)

    def output(
        self,
        file_name: str,
    ):
        """
        Save the PDF document to a file.

        Args:
            file_name (str): The name of the output PDF file.
        """
        self.pdf.output(file_name)

