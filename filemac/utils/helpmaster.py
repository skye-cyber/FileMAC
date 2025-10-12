from .utils.colors import fg, rs


RESET = rs


def pdf_combine_help():
    options = f"""
        _________________________
        {fg.BWHITE_FG}|Linear: {fg.YELLOW_FG}AA/BB/AAB/BBA{RESET}  |
        {fg.BWHITE_FG}|Shifted: {fg.YELLOW_FG}AB/BA/ABA/BAB{RESET} |
        _________________________"""

    helper = f"""\n\t---------------------------------------------------------------------------------------------
        {fg.BWHITE_FG}|Currently There are 2 supported methods: {fg.FCYAN_FG}Linear and Alternating/shifting.{RESET}\t\t    |
        |-------------------------------------------------------------------------------------------|
        {fg.BWHITE_FG}|->Linear pages are ordered in form of: {fg.CYAN_FG}File1Page1,...Fil1Pagen{RESET} then {fg.CYAN_FG}File2Page1,...Fil2Pagen{RESET}|\n\t{fg.BWHITE_FG}|File2 is joined at the end of the file1.\t\t\t\t\t\t    |
        |-------------------------------------------------------------------------------------------|
        {fg.BWHITE_FG}|->Shifting method Picks: {fg.CYAN_FG}File1Page1, File2Page1...File1pagen,File2Pagen{RESET}\t\t    |
        |--------------------------------------------------------------------------------------------"""

    ex = f"""\t_____________________________________________________
    \t|->{fg.BBLUE_FG}filemac --pdfjoin file1.pdf file2.pdf --order AAB{RESET}|
    \t-----------------------------------------------------"""
    return options, helper, ex
