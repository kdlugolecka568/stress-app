import streamlit as st

st.set_page_config(page_title="Kalkulator stresu studenta")

st.title(" Kalkulator stresu studenta")

import streamlit as st
import pandas as pd
import joblib

st.title("Kalkulator stresu 🧠")

pipe = joblib.load("best_model.joblib")

sleep = st.selectbox("Ile godzin śpisz średnio na dobę?",
                     ["Mniej niż 5", "5-6", "7-8", "Więcej niż 8"])

# ... tutaj wklejasz resztę pytań i mapowań ...

if st.button("Oblicz"):
    df = pd.DataFrame([{ "ile_godzin_spisz_srednio_na_dob": 7.5 }])  # przykładowo
    pred = pipe.predict(df)[0]
    st.write(f"Wynik: {pred}")
