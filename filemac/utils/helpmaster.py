from .utils.colors import foreground, background

fcl = foreground()
bcl = background()
RESET = fcl.RESET


def pdf_combine_help():
    options = f"""
        _________________________
        {fcl.BWHITE_FG}|Linear: {fcl.YELLOW_FG}AA/BB/AAB/BBA{RESET}  |
        {fcl.BWHITE_FG}|Shifted: {fcl.YELLOW_FG}AB/BA/ABA/BAB{RESET} |
        _________________________"""

    helper = f"""\n\t---------------------------------------------------------------------------------------------
        {fcl.BWHITE_FG}|Currently There are 2 supported methods: {fcl.FCYAN_FG}Linear and Alternating/shifting.{RESET}\t\t    |
        |-------------------------------------------------------------------------------------------|
        {fcl.BWHITE_FG}|->Linear pages are ordered in form of: {fcl.CYAN_FG}File1Page1,...Fil1Pagen{RESET} then {fcl.CYAN_FG}File2Page1,...Fil2Pagen{RESET}|\n\t{fcl.BWHITE_FG}|File2 is joined at the end of the file1.\t\t\t\t\t\t    |
        |-------------------------------------------------------------------------------------------|
        {fcl.BWHITE_FG}|->Shifting method Picks: {fcl.CYAN_FG}File1Page1, File2Page1...File1pagen,File2Pagen{RESET}\t\t    |
        |--------------------------------------------------------------------------------------------"""

    ex = f"""\t_____________________________________________________
    \t|->{fcl.BBLUE_FG}filemac --pdfjoin file1.pdf file2.pdf --order AAB{RESET}|
    \t-----------------------------------------------------"""
    return options, helper, ex
