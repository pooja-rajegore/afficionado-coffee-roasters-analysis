import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data():

    file_path = (
        Path(__file__).resolve().parent
        / "Data"
        / "Cleaned_Afficionado_Coffee_Data.csv"
    )

    df = pd.read_csv(file_path)

    return df
