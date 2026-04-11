import pandas as pd
import streamlit as st
from datetime import datetime

ARTIST_SHEET = "Artists"
RELEASE_SHEET = "Releases"

# BUG: Ghost id label

def parse_currency(value):
    if isinstance(value, str):
        value = value.replace("£", "").replace(",", "")
    return float(value)


def create_new_artist(df, name, email):
    id = df["ID"].max() + 1
    # NOTE: This is only true for now
    contract_id = id
    royalties_date = datetime.today().strftime("%m-%d")
    return {"ID": id, "Name": name, "Email": email, "Contract ID": contract_id, "Royalties Date": royalties_date, "Streams": 0, "Revenue TD": 0}


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
            event = st.dataframe(
                df,
                use_container_width = True,
                hide_index = True,
                on_select = "rerun",
                selection_mode = "single-row"
            )

            if event.selection.rows:
                selected_index = event.selection.rows[0]
                selected_row = df.iloc[selected_index]

                st.session_state["edit_sheet"] = sheet
                st.session_state["edit_index"] = selected_index

            if st.session_state.get("edit_sheet") == ARTIST_SHEET and sheet == ARTIST_SHEET:
                idx = st.session_state["edit_index"]
                row = df.iloc[idx]

                st.divider()
                st.subheader(f"Editing: {row['Name']}")

                with st.form("edit_artist"):
                    name = st.text_input("Name", value = row["Name"])
                    email = st.text_input("Email", value = row["Email"])
                    streams = st.number_input("Streams", value = int(row["Streams"]))
                    revenue = st.number_input(
                        "Revenue TD",
                        value = parse_currency(row["Revenue TD"])
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        save = st.form_submit_button("Submit")
                    with col2:
                        cancel = st.form_submit_button("Cancel")

                    if cancel:
                        st.session_state.pop("edit_index", None)
                        st.session_state.pop("edit_sheet", None)
                        st.rerun()
                    if save:
                        df.loc[idx, "Name"] = name
                        df.loc[idx, "Email"] = email
                        df.loc[idx, "Streams"] = streams
                        df.loc[idx, "Revenue TD"] = revenue

                        sheets_dict[ARTIST_SHEET] = df

                        with pd.ExcelWriter(file, engine = "openpyxl") as writer:
                            for sheet_name, data in sheets_dict.items():
                                data.to_excel(writer, sheet_name = sheet_name, index = False)
                        del st.session_state["edit_index"]

                        st.success("Updated")
                        st.rerun()
    
    if "edit_index" not in st.session_state:
        with st.form("add_artist"):
            name = st.text_input("Artist name")
            submitted = st.form_submit_button("Add")

            if submitted:
                # Reload correct sheet
                df = pd.read_excel(file, sheet_name = ARTIST_SHEET)

                new_row = pd.DataFrame([create_new_artist(df, name, "example@email.com")])
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
