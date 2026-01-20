import streamlit as st

st.set_page_config(page_title="Kalkulator stresu studenta")

st.title(" Kalkulator stresu studenta")

import streamlit as st
import pandas as pd
import joblib

MODEL_PATH = "kalkulator stresu"
USE_THRESHOLD = True
THRESHOLD = 0.40

FEATURES = [
    "ile_godzin_spisz_srednio_na_dob",
    "ile_kaw_napojow_energetycznych_250_ml_spozywasz_w_ciagu_dnia",
    "ile_ile_godzin_dziennie_poswiecasz_na_nauke",
    "ile_dni_w_tygodniu_cwiczysz",
    "jak_czesto_spozywasz_alkohol",
    "jak_czesto_palisz_papierosy",
    "ile_razy_w_miesiacu_uczestniczysz_w_aktywnosciach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle",
]

def risk_level(p_high: float) -> str:
    if p_high < 0.20:
        return "niskie"
    if p_high < 0.40:
        return "umiarkowane"
    if p_high < 0.60:
        return "podwyższone"
    return "wysokie"

st.title("Kalkulator ryzyka wysokiego stresu")

pipe = joblib.load(MODEL_PATH)

sleep = st.selectbox("Ile godzin śpisz średnio na dobę?",
                     ["Mniej niż 5", "5-6", "7-8", "Więcej niż 8"])
caffeine = st.selectbox("Ile kaw/energetyków pijesz dziennie?",
                        ["0", "1", "2", "3", "4 lub więcej"])
study = st.selectbox("Ile godzin dziennie się uczysz?",
                     ["Mniej niż 1", "1-2", "3-4", "5 lub więcej"])
ex = st.selectbox("Ile dni w tygodniu ćwiczysz?",
                  ["0", "1-2", "3-4", "5-6", "Codziennie"])
alc = st.selectbox("Jak często pijesz alkohol?",
                   ["Nigdy", "Sporadycznie", "Kilka razy w miesiącu", "Regularnie"])
smoke = st.selectbox("Jak często palisz papierosy?",
                     ["Nigdy", "Sporadycznie", "Kilka razy w tygodniu", "Codziennie"])
relax = st.selectbox("Ile razy w miesiącu robisz aktywności odstresowujące?",
                     ["0", "1-2", "3-5", "6+"])

SLEEP_MAP = {"Mniej niż 5":4.5, "5-6":5.5, "7-8":7.5, "Więcej niż 8":8.5}
CAFFEINE_MAP = {"0":0, "1":1, "2":2, "3":3, "4 lub więcej":4}
STUDY_MAP = {"Mniej niż 1":0.5, "1-2":1.5, "3-4":3.5, "5 lub więcej":5}
EX_MAP = {"0":0, "1-2":1.5, "3-4":3.5, "5-6":5.5, "Codziennie":7}
ALC_MAP = {"Nigdy":1, "Sporadycznie":2, "Kilka razy w miesiącu":3, "Regularnie":4}
SMOKE_MAP = {"Nigdy":1, "Sporadycznie":2, "Kilka razy w tygodniu":3, "Codziennie":4}
RELAX_MAP = {"0":0.0, "1-2":1.5, "3-5":4.0, "6+":6.0}

if st.button("Oblicz"):
    x = pd.DataFrame([{
        FEATURES[0]: SLEEP_MAP[sleep],
        FEATURES[1]: CAFFEINE_MAP[caffeine],
        FEATURES[2]: STUDY_MAP[study],
        FEATURES[3]: EX_MAP[ex],
        FEATURES[4]: ALC_MAP[alc],
        FEATURES[5]: SMOKE_MAP[smoke],
        FEATURES[6]: RELAX_MAP[relax],
    }])

    pred = pipe.predict(x)[0]
    p_high = None

    if hasattr(pipe, "predict_proba"):
        proba = pipe.predict_proba(x)[0]
        classes = list(pipe.classes_)
        if "HIGH" in classes:
            p_high = float(proba[classes.index("HIGH")])
        if USE_THRESHOLD and p_high is not None:
            pred = "HIGH" if p_high >= THRESHOLD else "NOT_HIGH"

    st.subheader(f"Wynik: {pred}")

    if p_high is not None:
        st.write(f"Prawdopodobieństwo HIGH = {p_high:.3f}")
        st.write(f"Poziom ryzyka: **{risk_level(p_high)}**")


