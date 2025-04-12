import pandas as pd
from sqlalchemy import create_engine
import argparse

fname = "data/Data-startupticker.xlsx"  # Path to your Excel file
sheet_table = {
    "Companies": "companies",
    "Company description": "company_descriptions",
    "Deals": "deals",
    "Deal description": "deal_descriptions"
}
db_name = "svcrdb"
DATABASE_HOST_IP = "localhost"

local_db_endpoint = f"mysql+mysqlconnector://root:password@{DATABASE_HOST_IP}/{db_name}"

def main(
    local: bool = True
):

    engine = create_engine(local_db_endpoint)

    # Load the Excel file
    for sheet, table in sheet_table.items():
        df = pd.read_excel(fname, sheet_name=sheet)
        df.to_sql(name=table, con=engine, if_exists='replace', index=False)


# # Write to MySQL table (replace if exists)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate the database.")
    parser.add_argument("--local", action="store_true", help="Run local population")
    args = parser.parse_args()

    main(local=args.local)
