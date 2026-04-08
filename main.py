import pandas as pd
import streamlit as st
from datetime import datetime

ARTIST_SHEET = "Artists"
RELEASE_SHEET = "Releases"

# BUG: Ghost id label


def create_new_artist(id_counter, name, email):
    id = id_counter + 1
    # NOTE: This is only true for now
    contract_id = id
    royalties_date = datetime.today().strftime("%m-%d")
    return {"ID": id, "Name": name, "Email": email, "Contract ID": contract_id, "Royalties Date": royalties_date, "Streams": "0", "Revenue TD": "0"}


def main():
    # Fetch data
    file = "1975 Records.xlsx"
    xls = pd.ExcelFile(file)
    sheets_dict = {
        sheet: pd.read_excel(xls, sheet)
        for sheet in xls.sheet_names
    }

    sheets = xls.sheet_names

    st.title("1975 Records Dashboard")

    # Display tabs
    tabs = st.tabs(sheets)
    for i, sheet in enumerate(sheets):
        with tabs[i]:
            df = pd.read_excel(file, sheet_name = sheet)
            st.dataframe(df)

    
    with st.form("add_artist"):
        name = st.text_input("Artist name")
        submitted = st.form_submit_button("Add")

        if submitted:
            # Reload correct sheet
            df = pd.read_excel(file, sheet_name = ARTIST_SHEET)

            new_row = pd.DataFrame([create_new_artist(df.shape[0], name, "example@email.com")])
            df = pd.concat([df, new_row], ignore_index = True)
            
            xls = pd.ExcelFile(file)
            sheets_dict = {
                sheet: pd.read_excel(xls, sheet)
                for sheet in xls.sheet_names
            }
            sheets_dict["Artists"] = df

            with pd.ExcelWriter(file, engine = "openpyxl") as writer:
                for sheet_name, data in sheets_dict.items():
                    data.to_excel(writer, sheet_name = sheet_name, index = False)
            st.success("Added!")


    print()

if __name__ == "__main__":
    main()
