from sklearn.preprocessing import OrdinalEncoder
from pandas import read_csv, cut
import streamlit as st
from numpy import linspace

@st.cache_data
def obtener_df(path, full_dataset=False, subsize = 10_000):
    df = read_csv(path)
    if not full_dataset:
        df = df.sample(subsize).reset_index().drop("index",axis=1)
    df["loan_intent"] = df["loan_intent"].astype("category")
    df["person_home_ownership"] = df["person_home_ownership"].astype("category")
    df["loan_grade"] = df["loan_grade"].astype("category")
    df["cb_person_default_on_file"] = df["cb_person_default_on_file"].astype("category")
    labels = ['muy joven', 'joven', 'maso', 'viejo', 'muy viejo']

    # Crear la nuevas columnas categóricas
    bins = linspace(18,100,6).round()
    df["loan_status_cat"] = df['loan_status'].map({0: 'cumplido', 1: 'moroso'})
    df['edades'] = cut(df['person_age'], bins=bins, labels=labels, right=False)

    ord_encs = { col: OrdinalEncoder().fit(df[[col]]) for col in ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']}
    return df, ord_encs