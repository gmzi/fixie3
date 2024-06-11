import traceback
import sys
import pymupdf
import pandas as pd
import re

def convert_to_float(x):
    if x.strip():
        return round(float(x.strip().replace(",", "")), 2)
    else:
        return None
    
def format_numeric_columns(df):
    for col in df.select_dtypes(include=['number']).columns:
        df[col] = df[col].map('${:,.2f}'.format)
    return df

def extract_text_to_dataframe(page, transaction_types):
    transaction_types_pattern = '|'.join(map(re.escape, transaction_types))

    text_raw = page.get_text("text")

    substring = "Security description"
    index = text_raw.find(substring)
    text = text_raw[index:]

    lines = text.split('\n')
    data = []
    current_symbol = None
    current_ticker = '-'
    current_date = None
    current_amount = None
    current_transaction = None

    for line in lines:
        if "Total " in line:
            continue
        elif re.match(r'^[A-Z]{2,}', line):
            if "(cont'd)" in line:
                line = line.replace("(cont'd)", "").strip()
            current_symbol = line
        elif re.match(r'.*([A-Z]{2,})$', line):
            # ticker = re.sub(r'[^A-Za-z\s]', '', line).strip()
            # current_ticker = ticker
            match = re.search(r'\b([A-Z]{1,20})\b(?=\s*\d{2}/\d{2}/\d{2}|\s*$)', line)
            if match:
                current_ticker = match.group(1)
            else: 
                current_ticker = '-'
        elif re.match(r'\d{2}/\d{2}/\d{2}', line):
            current_date = line
        elif re.match(r'-?\d+,\d{3}\.\d+|-?\d+\.\d+', line):
            current_amount = line
        elif re.match(transaction_types_pattern, line):
            current_transaction = line
            if current_symbol and current_date and current_amount and current_transaction:
                data.append([current_symbol, current_ticker, current_date, current_amount, current_transaction])
                current_date = None
                current_amount = None
                current_transaction = None

    columns = ["symbol", "ticker", "date", "amount", "transaction"]

    df = pd.DataFrame(data, columns=columns)

    df['amount'] = df['amount'].apply(lambda x: convert_to_float(x))

    return df

def dividends(file_path):
    transaction_types = ['Nonqualified dividend', 'Qualified dividend', 'Short-term capital gain', 'Long-term capital gain', 'Section 199A dividend', 'Foreign tax withheld', 'Tax-exempt dividend']
    try:
        doc = pymupdf.open(file_path)
        dfs = []

        for page in doc:
            df = extract_text_to_dataframe(page, transaction_types)
            if df is not None and not df.empty:
                dfs.append(df)

        if len(dfs) == 0:
            return pd.DataFrame()
        
        master_df = pd.concat(dfs, ignore_index=True)

        ticker_df = master_df[['symbol', 'ticker']].drop_duplicates()

        table = master_df.pivot_table(index=['symbol'], columns='transaction', values='amount', aggfunc='sum', fill_value=0).reset_index()

        table = pd.merge(table, ticker_df,  on='symbol', how='left')


        sums = table.sum(axis=0)
        sums['symbol'] = 'Totals'
        sums_df = pd.DataFrame([sums.values], columns=table.columns)

        new_table = pd.concat([sums_df, table], ignore_index=True)

        new_table = format_numeric_columns(new_table)

        # Remove contents of 'ticker' column where 'symbol' is 'Totals'
        new_table.loc[new_table['symbol'] == 'Totals', 'ticker'] = ''

        # Dynamically reorder columns
        columns = list(new_table.columns)
        columns.remove('symbol')
        columns.remove('ticker')
        new_order = ['symbol', 'ticker'] + columns
        new_table = new_table[new_order]

        return new_table
    
    except Exception as e:
        traceback.print_exc()
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('error:', e)
        print("At line:", exc_tb.tb_lineno)
        return pd.DataFrame()

def interest(file_path):
    transaction_types = ['Interest']
    try:
        doc = pymupdf.open(file_path)
        dfs = []

        for page in doc:
            df = extract_text_to_dataframe(page, transaction_types)
            if df is not None and not df.empty:
                dfs.append(df)

        master_df = pd.concat(dfs, ignore_index=True)

        table = master_df.pivot_table(index='symbol', columns='transaction', values='amount', aggfunc='sum', fill_value=0).reset_index()

        sums = table.sum(axis=0)
        sums['symbol'] = 'Totals'

        sums_df = pd.DataFrame([sums.values], columns=table.columns)

        new_table = pd.concat([sums_df, table], ignore_index=True)

        for col in new_table.columns[1:]:
            new_table[col] = new_table[col].astype(float).map('${:,.2f}'.format)

        return new_table
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

            # Convert values in "amount" column to currency format using .loc
            df_filtered.loc[:, 'amount'] = df_filtered['amount'].apply(lambda x: "${:,.2f}".format(float(x.replace(",", ""))))

            return df_filtered
    except Exception as e:
        return pd.DataFrame()


