import traceback
import sys
import pymupdf
import pandas as pd

def convert_to_float(x):
    if x.strip():  # Check if x is not an empty string after stripping
        return float(x.strip().replace(",", ""))
    else:
        return None

def clean_and_convert(df):
    table_start = df[df['notes'] ==
                     'Notes'].index.to_list()[0]
    df.drop(df.index[0:table_start], inplace=True)
    df = df.reset_index(drop=True)

    rows_to_drop_Secu = df[df['amount'] == 'Amount'].index
    df.drop(rows_to_drop_Secu, inplace=True)
    df = df.reset_index(drop=True)

    # convert amounts to float values
    df['amount'] = df['amount'].apply(lambda x: convert_to_float(x))

    # Drop rows with NaN in the 'amount' column
    df = df[df['amount'].notna()]

    # Drop empty rows
    df = df[df['amount'] != '']

    # Drop totals
    df = df[~df['transaction'].str.contains('Total', na=False)]

    df['symbol'] = df['symbol'].replace('', pd.NA).ffill()
    # Trim the 'symbol' column
    df['symbol'] = df['symbol'].apply(lambda x: x[x.rfind(' ') + 1:])

    return df


def extract_initial(page):
    tabs = page.find_tables(
        strategy="text",
        vertical_strategy="text",
        horizontal_strategy="text",
        min_words_vertical=8,
        min_words_horizontal=0
    )

    tabs_len = len(tabs.tables)

    if tabs_len > 0:
        df = tabs[0].to_pandas()

        df.columns = ['symbol', 'date', 'amount', 'transaction', 'notes']

        # clean rows:
        table_start = df[df['notes'] == 'Notes'].index.to_list()[0]
        df.drop(df.index[0:table_start], inplace=True)
        df = df.reset_index(drop=True)

        clean_df = clean_and_convert(df)

        return clean_df

def extract_continued(page):
    tabs = page.find_tables(
        strategy="text",
        vertical_strategy="text",
        horizontal_strategy="simple",
        min_words_vertical=4,
        min_words_horizontal=0
    )

    tabs_len = len(tabs.tables)

    if tabs_len > 0:
        df = tabs[0].to_pandas()

        df.columns = ['foo', 'bar', 'symbol', 'date', 'amount', 'transaction', 'beta', 'kappa', 'notes']

        df.drop(columns=['foo', 'bar', 'beta', 'kappa'], inplace=True)

        # clean rows:
        table_start = df[df['notes'] == 'Notes'].index.to_list()[0]
        df.drop(df.index[0:table_start], inplace=True)
        df = df.reset_index(drop=True)

        clean_df = clean_and_convert(df)

        return clean_df

def dividends(file_path):
    try:
        doc = pymupdf.open(file_path)
        dfs = []

        for i, page in enumerate(doc):
            if i == 0:
                df = extract_initial(page)
            else: 
                df = extract_continued(page)
            if df is not None:
                dfs.append(df)

        total_df = pd.concat(dfs, ignore_index=True)
        table = total_df.pivot_table(index='symbol', columns='transaction', values='amount', aggfunc='sum', fill_value=0).reset_index()
        return table
    except Exception as e:
        traceback.print_exc()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('error:', e)
        print("At line:", exc_tb.tb_lineno)
        return pd.DataFrame()

def broker(file_path): 
    try: 
        doc = pymupdf.open(file_path)
        page = doc[0]
        tabs = page.find_tables(
            strategy="text",
            vertical_strategy="text",
            horizontal_strategy="text",
            min_words_vertical=9,
            min_words_horizontal=0
        )

        tabs_len = len(tabs.tables)

        if tabs_len > 0:
            df = tabs[0].to_pandas()

            df.columns = ["term", "type", 'foo', 'bar', 'alpha', 'beta', 'gamma', 'amount']

            table_start = df[df['term'] == 'Term'].index.to_list()[0]
            df.drop(df.index[0:table_start], inplace=True)
            df = df.reset_index(drop=True)

            df.drop(columns=['term', 'foo', 'bar', 'alpha', 'beta', 'gamma'], inplace=True)

            df_filtered = df[df['type'].str.contains('Total', case=False) | df['type'].str.contains('Grand total', case=False)]

            return df_filtered
    except Exception as e:
        return pd.DataFrame()


