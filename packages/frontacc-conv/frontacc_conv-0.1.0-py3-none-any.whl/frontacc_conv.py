"""
Financial data conversion utilities module.
Supports converting between various financial data formats including:
- Excel GL transactions to QIF format
"""

import pandas as pd
import argparse
import csv
import os  # Add this import at the top of the file

class ConversionError(Exception):
    """Custom exception for conversion errors"""
    pass

class FrontaccConverter:
    """Class handling various financial data format conversions"""

    @staticmethod
    def csv2native(input_file: str, output_file: str, bank: str, account: str, currency: str) -> None:
        """
        Convert Airwallex Balance Activity Report to Frontaccounting BankImport native format
        
        Args:
            input_file: Path to source csv file
            output_file: Path to output csv file
            
        Raises:
            ConversionError: If conversion fails
            FileNotFoundError: If input file doesn't exist
        """
        
        try:

            df = pd.read_csv(input_file) 
            # Open the output CSV file for writing
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                # header for statemetn header
                # fields"0:bank[varchar(6)], 1:account[varchar(24)], 2:currency[varchar(4)], 3:startBalance[double], 4:endBalance[double], 5:smtDate[date], 6:number[int(11)], 7:seq[int(11)], 8:statementId[varchar(32)]"
                writer.writerow(["bank", "account", "currency", "startBalance", "endBalance", "smtDate", "number", "seq", "statementId"])
                # Extract the filename without path and extension
                input_filename = os.path.splitext(os.path.basename(input_file))[0]
                writer.writerow([bank, account, currency, 0.0, 0.0, "", 0, 0, input_filename])

                #header for transaction
                # 0:valueTimestamp[date],1:entryTimestamp[date],2:account[varchar(24)],3:accountName[varchar(60)],4:transactionCode[varchar(32)],5:transactionCodeDesc[varchar(32)],6:transactionDC[varchar(2)],7:transactionAmount[double],8:transactionTitle[varchar(256)],9:transactionChargeAmount[double],10:transactionChargeTitle[varchar(256)]
                writer.writerow(["valueTimestamp", "entryTimestamp", "account", "accountName", "transactionCode", "transactionCodeDesc", "transactionDC", "transactionAmount", "transactionTitle", "transactionChargeAmount", "transactionChargeTitle"])
                for _, row in df.iterrows():
                    date = row['Time'].split("T")[0]  # Extracting the date portion
                    amount = -row["Debit Net Amount"] if pd.notna(row["Debit Net Amount"]) else row["Credit Net Amount"]
                    writer.writerow(date, date, f"{account} {currency}" , "", "", "", "", amount, row["Description"], "", "")
        except Exception as e:
            raise ConversionError(f"Failed to convert Airwallex Balance Activity Report CSV to Frontaccounting BankImport native format: {str(e)}")

    
    @staticmethod
    def gl2qif(input_file: str, output_file: str, payee: str, account_type: str = "Bank",) -> None:
        """
        Convert Excel GL transactions to QIF format
        
        Args:
            input_file: Path to source Excel file
            output_file: Path to output QIF file
            payee: Payee for the transaction
            account_type: QIF account type (default: Cash)
            
        Raises:
            ConversionError: If conversion fails
            FileNotFoundError: If input file doesn't exist
        """
        try:
            # Read specific cells for period and opening balance
            xls = pd.ExcelFile(input_file)
            period = pd.read_excel(xls, usecols="B", skiprows=2, nrows=1).iloc[0, 0]

            opening_balance_debit  = pd.read_excel(xls, usecols="H", skiprows=5, nrows=1).iloc[0, 0]
            opening_balance_credit = pd.read_excel(xls, usecols="I", skiprows=5, nrows=1).iloc[0, 0]
            opening_balance = opening_balance_credit if pd.notna(opening_balance_credit) else - opening_balance_debit
            
            last_valid_index = 0
            # Read transactions starting from row 9
            df = pd.read_excel(
                xls, 
                skiprows=7, 
                usecols="A:J", 
                names=["Type", "Ref", "#", "Date", "Dimension", "Unused", "Person/Item", "Debit", "Credit", "Balance"],
                dtype={
                    "Type": str, 
                    "Ref": str, 
                    "#": str, 
                    "Date": "datetime64[ns]", 
                    "Dimension": str, 
                    "Unused": str, 
                    "Person/Item": str, 
                },
                converters={
                    "Debit": lambda x: float(str(x).replace(',', '').replace('.', '.', 1)) if pd.notnull(x) else 0.0,
                    "Credit": lambda x: float(str(x).replace(',', '').replace('.', '.', 1)) if pd.notnull(x) else 0.0,
                    "Balance": lambda x: float(str(x).replace(',', '').replace('.', '.', 1)) if pd.notnull(x) else 0.0
                }
            )
            # Start QIF file with account type header
            with open(output_file, 'w') as qif_file:
                qif_file.write(f"!Type:{account_type}\n")
                
                # Iterate over each row in the dataframe and format into QIF
                for _, row in df.iterrows():
                    if pd.isna(row['Date']):  # Stop processing if 'Date' is NaN
                        empty_line_index = _
                        break
                    trans_amount = row['Debit'] if pd.notna(row['Debit']) else - row['Credit']
                    qif_file.write(f"D{row['Date'].strftime('%m/%d/%Y')}\n")
                    qif_file.write(f"T{trans_amount}\n")
                    qif_file.write(f"N{row['Ref']}\n")
                    descr = row['Person/Item'].replace("\n", "")
                    qif_file.write(f"M{row['Type']}: {descr}\n")
                    qif_file.write(f"P{payee}\n")
                    qif_file.write("^\n")

                # Read closing balance similar to opening balance
                closing_balance_debit = pd.read_excel(xls, usecols="H", skiprows=6 + empty_line_index, nrows=1).iloc[0, 0]
                closing_balance_credit = pd.read_excel(xls, usecols="I", skiprows=6 + empty_line_index, nrows=1).iloc[0, 0]
                closing_balance = closing_balance_credit if pd.notna(closing_balance_credit) else - closing_balance_debit

            print(f"Successfully converted {input_file} to {output_file}")
            print(f"Period: {period}, Opening Balance: {opening_balance}, Closing Balance: {closing_balance}")
            
        except Exception as e:
            raise ConversionError(f"Failed to convert {input_file} to QIF: {str(e)}")

def main(): 
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Convert financial data formats.')
    parser.add_argument('conversion_type', type=str, choices=['gl2qif', 'csv2native'], help='Type of conversion to perform')
    parser.add_argument('input_file', type=str, help='Path to the input file')
    parser.add_argument('output_file', type=str, help='Path to the output file')
    parser.add_argument('qif_payee', type=str, nargs='?', default='Default Payee', help='Payee for QIF transactions (default: "Default Payee")')
    parser.add_argument('bank', type=str, nargs='?', default='Default Bank', help='Bank for Frontaccounting BankImport (default: "Default Bank")')
    parser.add_argument('account', type=str, nargs='?', default='Default Account', help='Account for Frontaccounting BankImport (default: "Default Account")')
    parser.add_argument('currency', type=str, nargs='?', default='USD', help='Currency for Frontaccounting BankImport (default: "USD")')
    
    args = parser.parse_args()
    
    if args.conversion_type == 'gl2qif':
        FrontaccConverter.gl2qif(args.input_file, args.output_file, args.qif_payee) 
    elif args.conversion_type == 'csv2native':
        FrontaccConverter.csv2native(args.input_file, args.output_file, args.bank, args.account, args.currency)  

if __name__ == "__main__":
    main()
