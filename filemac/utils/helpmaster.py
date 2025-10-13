from .utils.colors import fg, rs


RESET = rs


def pdf_combine_help():
    options = f"""
        _________________________
        {fg.BWHITE}|Linear: {fg.YELLOW}AA/BB/AAB/BBA{RESET}  |
        {fg.BWHITE}|Shifted: {fg.YELLOW}AB/BA/ABA/BAB{RESET} |
        _________________________"""

    helper = f"""\n\t---------------------------------------------------------------------------------------------
        {fg.BWHITE}|Currently There are 2 supported methods: {fg.FCYAN}Linear and Alternating/shifting.{RESET}\t\t    |
        |-------------------------------------------------------------------------------------------|
        {fg.BWHITE}|->Linear pages are ordered in form of: {fg.CYAN}File1Page1,...Fil1Pagen{RESET} then {fg.CYAN}File2Page1,...Fil2Pagen{RESET}|\n\t{fg.BWHITE}|File2 is joined at the end of the file1.\t\t\t\t\t\t    |
        |-------------------------------------------------------------------------------------------|
        {fg.BWHITE}|->Shifting method Picks: {fg.CYAN}File1Page1, File2Page1...File1pagen,File2Pagen{RESET}\t\t    |
        |--------------------------------------------------------------------------------------------"""

    ex = f"""\t_____________________________________________________
    \t|->{fg.BBLUE}filemac --pdfjoin file1.pdf file2.pdf --order AAB{RESET}|
    \t-----------------------------------------------------"""
    return options, helper, ex
