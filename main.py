import os
import FUNCTIONS as myfunc


def run():
    """
    Main function to process price data and send out emails.

    This function processes price data from Excel and PDF files, compares new prices with old prices
    for two products, 'GRESKO' and 'KALIMERA FROUTA', then creates a new Excel file with the results
    and sends out an email with the Excel file attached.

    Parameters:
    None

    Returns:
    None

    Side Effects:
    - Reads from Excel and PDF files.
    - Creates and writes to an Excel file.
    - Sends an email with an attachment.
    """

    cwd = os.getcwd()
    file_name = 'manaviki.xlsx'
    path_to_file = f'{cwd}/OUTPUT/{file_name}'
    html_file = f'{cwd}/HTML/body.html'

    list_of_dates =['26102023', '30102023']
    new = list_of_dates[-1]
    old = list_of_dates[-2]

    # NEW PRICES GRESKO | A. FIND FILE | B. CREATE DATAFRAME
    fa = f'{cwd}/FILES/GRESKO {new}.xlsx'
    gresco = myfunc.run_prosfores_gresko(fa)

    # NEW PRICES KALIMERA FROUTA | A. FIND FILE | B. CREATE DATAFRAME
    fb = f'{cwd}/FILES/FNV {new}.pdf'
    kalimera_frouta = myfunc.run_prosfores_kalimera(fb)

    # OLD PRICES GRESKO | A.FIND FILE | B.CREATE DATAFRAME | C.COMPARE WITH NEW PRICES
    fc = f'{cwd}/FILES/GRESKO {old}.xlsx'
    gresco_old = myfunc.run_prosfores_gresko(fc)
    gresco_price_change = myfunc.run_gresko(gresco, gresco_old)

    # OLD PRICES KALIMERA FROUTA | A.FIND FILE | B.CREATE DATAFRAME | C.COMPARE WITH NEW PRICES
    fd = f'{cwd}/FILES/FNV {old}.pdf'
    kalimera_frouta_old = myfunc.run_prosfores_kalimera(fd)
    kalimera_price_changed = myfunc.run_kalimera(kalimera_frouta, kalimera_frouta_old)

    # CREATE EXCEL FUNCTION
    myfunc.export(f'{cwd}/OUTPUT/manaviki.xlsx', gresco, kalimera_frouta, gresco_price_change, kalimera_price_changed)

    # SEND E-MAIL FUNCTION
    myfunc.run(path_to_file, file_name, html_file)


if __name__ == "__main__":
    run()
