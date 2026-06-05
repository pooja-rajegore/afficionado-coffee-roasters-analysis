import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data():

    file_path = Path(__file__).resolve().parent / "Data" / "Cleaned_Afficionado_Coffee_Data.xlsx"

    st.write("File path:", file_path)
    st.write("Exists:", file_path.exists())

    if not file_path.exists():
        st.error(f"Missing file: {file_path}")
        st.stop()

    return pd.read_excel(file_path)
