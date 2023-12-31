import os
import FUNCTIONS as myfunc
from datetime import datetime


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
    today = datetime.now().strftime('%d%m%y')
    cwd = os.getcwd()
    file_name = f'manaviki_{today}.xlsx'
    path_to_file = f'{cwd}/OUTPUT/{file_name}'
    html_file = f'{cwd}/HTML/body.html'

    list_of_dates_gresco = ['26102023', '30102023', '03112023', '20231106', '231109']
    new_gresco = list_of_dates_gresco[-1]
    old_gresco = list_of_dates_gresco[-2]

    list_of_dates_kalimera = ['26102023', '30102023', '03112023', '231107']
    new_kalimera = list_of_dates_kalimera[-1]
    # ΔΕΝ ΜΑΣ ΕΝΔΙΑΦΕΡΟΥΝ ΟΙ ΠΤΩΣΕΙΣ ΤΙΜΩΝ
    old_kalimera = list_of_dates_kalimera[-2]

    # NEW PRICES GRESKO | A. FIND FILE | B. CREATE DATAFRAME
    fa = f'{cwd}/FILES/GRESKO {new_gresco}.xlsx'
    gresco = myfunc.run_prosfores_gresko(fa)

    # NEW PRICES KALIMERA FROUTA | A. FIND FILE | B. CREATE DATAFRAME
    fb = f'{cwd}/FILES/FNV {new_kalimera}.pdf'
    kalimera_frouta = myfunc.run_prosfores_kalimera(fb)

    # OLD PRICES GRESKO | A.FIND FILE | B.CREATE DATAFRAME | C.COMPARE WITH NEW PRICES
    gresco_price_change = None
    fc = f'{cwd}/FILES/GRESKO {old_gresco}.xlsx'
    gresco_old = myfunc.run_prosfores_gresko(fc)
    gresco_price_change = myfunc.run_gresko(gresco, gresco_old)
    # print(gresco_price_change)

    # OLD PRICES KALIMERA FROUTA | A.FIND FILE | B.CREATE DATAFRAME | C.COMPARE WITH NEW PRICES
    kalimera_price_changed = None
    fd = f'{cwd}/FILES/FNV {old_kalimera}.pdf'
    kalimera_frouta_old = myfunc.run_prosfores_kalimera(fd)
    kalimera_price_changed = myfunc.run_kalimera(kalimera_frouta, kalimera_frouta_old)
    # print(kalimera_price_changed)

    # CREATE EXCEL FUNCTION
    myfunc.export(path_to_file, gresco, kalimera_frouta, gresco_price_change, kalimera_price_changed)

    # SEND E-MAIL FUNCTION
    # myfunc.run(path_to_file, file_name, html_file)

    os.system(f'open {path_to_file}')


if __name__ == "__main__":
    run()
