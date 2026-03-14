import streamlit as st
import pandas as pd
import tempfile

from rpy2.robjects import r
from rpy2.robjects import pandas2ri
import rpy2.robjects as ro

pandas2ri.activate()

st.title("GTSummary Table Generator")

file = st.file_uploader("Upload Excel File", type=["xlsx","csv"])

if file:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    # select variables
    variables = st.multiselect("Select Variables", df.columns)

    datatype = {}

    if variables:

        st.subheader("Select Data Type")

        for v in variables:

            datatype[v] = st.selectbox(
                f"{v} type",
                ["continuous","categorical"],
                key=v
            )

    if st.button("Generate Table"):

        rdf = pandas2ri.py2rpy(df)

        ro.globalenv["data_py"] = rdf
        ro.globalenv["var_list"] = ro.StrVector(variables)

        types = [datatype[v] for v in variables]
        ro.globalenv["type_list"] = ro.StrVector(types)

        temp_doc = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")

        ro.globalenv["outfile"] = temp_doc.name

        r('''
        library(gtsummary)
        library(flextable)
        library(dplyr)
        library(officer)

        data <- data_py

        vars <- var_list
        types <- type_list

        data2 <- data %>% select(all_of(vars))

        type_formula <- list()

        for(i in seq_along(vars)){
            if(types[i] == "continuous"){
                type_formula[[vars[i]]] <- "continuous"
            } else {
                type_formula[[vars[i]]] <- "categorical"
            }
        }

        tbl <- data2 %>%
        tbl_summary(type = type_formula)

        ft <- as_flex_table(tbl)

        ft <- fontsize(ft, size = 11)
        ft <- font(ft, fontname = "Calibri")

        save_as_docx(ft, path = outfile)
        ''')

        st.success("Table Created")

        with open(temp_doc.name, "rb") as f:
            st.download_button(
                "Download Table (Word)",
                f,
                file_name="gtsummary_table.docx"
            )