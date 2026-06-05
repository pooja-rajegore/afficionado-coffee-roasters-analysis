import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data():

    file_path = (
        Path(__file__).parent
        / "Data"
        / "Cleaned_Afficionado_Coffee_Data.xlsx"
    )

    df = pd.read_excel(file_path)

    return df
