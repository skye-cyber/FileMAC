import csv
import sys
import pandas as pd


def xls2csv(xls_file):
    try:
        _out_ = "out.csv"
        '''Read the XLS file using pandas'''

        # df = pd.read_excel(xls_file)

        '''Iterate over the rows of the dataframe and add them to the
        Word document'''
        print(f"Converting {xls_file}..")
        csv.list_dialects()
        # time.sleep(2)
        csv_reader = csv.reader(xls_file, dialect='excel')
        for row in csv_reader:
            # csv_writer = csv.writer(csv_reader [, dialect='excel'])
            csv.writer(_out_, row, dialect="excel")

            # print(f"Row {current_row}/{total_rows} \{percentage:.1f}%", end="\r")

    except FileNotFoundError as e:
        print(e)

    except KeyboardInterrupt:
        print("\nQuit!")
        sys.exit(1)

    '''except Exception as e:
        print(e)
        pass'''


xls2csv(xls_file="/home/skye/Documents/file_example_XLSX_1000.csv")
