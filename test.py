import os
import shutil
import sys
import traceback
import pandas as pd
from crop import crop
import table_extractor


def main():
    input_folder = './input/'

    # -------------------------------------------------
    # BRING FILE FROM AUTOMATOR

    # if len(sys.argv) < 2:
    #     sys.exit(1)

    # file_path = sys.argv[1]
    # file_name = os.path.basename(file_path)

    # if not file_path.endswith('.pdf'):
    #     print("The provided file is not a pdf")
    #     sys.exit(1)

    # new_path = os.path.join(input_folder, 'data.pdf')
    # shutil.copy(file_path, new_path)

    # -------------------------------------------------

    # -------------------------------------------------
    # MANUALLY ADD FILE TO LOCAL INPUT FOLDER
    files = os.listdir(input_folder)
    file_name = 'test'

    try:
        for file in files:
            if file.endswith('.pdf'):
                original_path = os.path.join(input_folder, file)
                new_path = os.path.join(input_folder, "data.pdf")
                shutil.copy(original_path, new_path)
    except Exception as e:
        print(e)
    # -------------------------------------------------

    try:
        summary_pdf = crop('./input/data.pdf',
                           '1a- Total ordinary dividends (includes lines 1b, 5, 2e)',
                           './input/summary.pdf'
                           )
        dividends_pdf = crop("./input/data.pdf",
                          'Detail for Dividends and Distributions',
                          './input/dividends.pdf'
                          )
        interest_pdf = crop('./input/data.pdf',
                            'Detail for Interest Income',
                            './input/interest.pdf'
                            )
        
        if not summary_pdf:
            sys.exit(1)

        if not dividends_pdf:
            sys.exit(2)

        if interest_pdf:
            interest_table = table_extractor.interest('./input/interest.pdf')
            if interest_table.empty:
                raise ValueError(6)
            interest_table.to_csv(f'./output/interest.csv', float_format='%.2f')
            file_path = os.path.join(input_folder, "interest.pdf")
            if os.path.exists(file_path):
                os.remove(file_path)
        
        broker_transactions_df = table_extractor.broker('./input/summary.pdf')
        if broker_transactions_df.empty:
            raise ValueError(3)
        
        dividends_table = table_extractor.dividends('./input/dividends.pdf')
        
        if dividends_table.empty:
            raise ValueError(4)

        dividends_table.to_csv(f'./output/dividends.csv', float_format='%.2f')
        broker_transactions_df.to_csv(f'./output/broker_transactions.csv', float_format='%.2f')

        # UNCOMMENT TO EXPORT TO SINGLE .xls file:
        with pd.ExcelWriter(f'./output/{file_name}.xlsx', engine='xlsxwriter') as writer:
            dividends_table.to_excel(writer, sheet_name='Dividends', index=False)
            broker_transactions_df.to_excel(writer, sheet_name='Broker Transactions', index=False)
            if interest_pdf:
                interest_table.to_excel(writer, sheet_name='Interest', index=False)

    except Exception as e:
        traceback.print_exc()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("At line:", exc_tb.tb_lineno)
        if type(e) == 'ValueError':
            status = e
            sys.exit(e)
        else:
            sys.exit(100)
        

    files_to_clean = ["data.pdf", "dividends.pdf", "summary.pdf"]
    for file_name in files_to_clean:
        file_path = os.path.join(input_folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File not found: {file_path}")


if __name__ == '__main__':
    main()
