import streamlit as st
import pandas as pd
from tableone import TableOne

st.title("Clinical Table 1 Generator")

st.write("Upload dataset and generate descriptive statistics table")

file = st.file_uploader("Upload Excel or CSV", type=["xlsx","csv"])

if file is not None:

    # read dataset
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    # select variables
    columns = st.multiselect("Select variables for table", df.columns)

    if columns:

        categorical = st.multiselect(
            "Select categorical variables",
            columns
        )

        groupby = st.selectbox(
            "Group by variable (optional)",
            ["None"] + columns
        )

        if st.button("Generate Table"):

            if groupby == "None":
                table = TableOne(
                    df,
                    columns=columns,
                    categorical=categorical
                )
            else:
                table = TableOne(
                    df,
                    columns=columns,
                    categorical=categorical,
                    groupby=groupby,
                    pval=True
                )

            st.subheader("Table 1")
            st.write(table)

            # convert table to dataframe
            table_df = table.tableone.reset_index()

            csv = table_df.to_csv(index=False)

            st.download_button(
                "Download Table (CSV)",
                csv,
                "table1.csv",
                "text/csv"
            )
