import streamlit as st

st.set_page_config(page_title="Kalkulator stresu studenta")

st.title("📊 Kalkulator stresu studenta")

st.write("Wypełnij krótką ankietę, a aplikacja oszacuje Twój poziom stresu (0–10).")

with st.form("stress_form"):
    # 1. KAWA
    kawa = st.selectbox(
        "Ile filiżanek kawy pijesz dziennie?",
        ["0", "1", "2", "3", "4 lub więcej"]
    )

    # 2. SEN
    sen = st.selectbox(
        "Ile godzin śpisz średnio na dobę?",
        ["mniej niż 5", "5–6", "7–8", "więcej niż 8"]
    )

    # 3. NAUKA
    nauka = st.selectbox(
        "Ile godzin dziennie poświęcasz na naukę?",
        ["mniej niż 1", "1–2", "3–4", "5 lub więcej"]
    )

    # 4. IMPREZY
    imprezy = st.selectbox(
        "Ile razy w tygodniu imprezujesz?",
        ["wcale", "1 raz", "2–3 razy", "4 lub więcej razy"]
    )

    # 5. ALKOHOL
    alkohol = st.selectbox(
        "Jak często spożywasz alkohol?",
        ["nigdy", "sporadycznie (raz w miesiącu lub rzadziej)",
         "kilka razy w miesiącu", "regularnie (kilka razy w tygodniu)"]
    )

    # 6. PAPIEROSY
    papierosy = st.selectbox(
        "Jak często palisz papierosy?",
        ["nigdy", "sporadycznie (np. tylko na imprezach)",
         "kilka razy w tygodniu", "codziennie"]
    )

    # 7. AKTYWNOŚCI ODSTRESOWUJĄCE
    relaks = st.selectbox(
        "Ile razy w miesiącu uczestniczysz w aktywnościach odstresowujących \
        (kino, zakupy, spacery, restauracja, kręgle itd.)?",
        ["0", "1–2", "3–5", "6 lub więcej"]
    )

    submitted = st.form_submit_button("Oblicz poziom stresu")

if submitted:
    # Przeliczenie odpowiedzi na punkty (im więcej punktów, tym większy stres)
    mapa_kawa = {
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4 lub więcej": 4
    }

    mapa_sen = {
        "mniej niż 5": 4,
        "5–6": 3,
        "7–8": 1,
        "więcej niż 8": 0
    }

    mapa_nauka = {
        "mniej niż 1": 2,
        "1–2": 1,
        "3–4": 2,
        "5 lub więcej": 3
    }

    mapa_imprezy = {
        "wcale": 2,
        "1 raz": 1,
        "2–3 razy": 2,
        "4 lub więcej razy": 3
    }

    mapa_alkohol = {
        "nigdy": 0,
        "sporadycznie (raz w miesiącu lub rzadziej)": 1,
        "kilka razy w miesiącu": 2,
        "regularnie (kilka razy w tygodniu)": 3
    }

    mapa_papierosy = {
        "nigdy": 0,
        "sporadycznie (np. tylko na imprezach)": 1,
        "kilka razy w tygodniu": 3,
        "codziennie": 4
    }

    mapa_relaks = {
        "0": 4,
        "1–2": 3,
        "3–5": 1,
        "6 lub więcej": 0
    }

    # surowy wynik (im większy, tym większy stres)
    raw_score = (
        mapa_kawa[kawa]
        + mapa_sen[sen]
        + mapa_nauka[nauka]
        + mapa_imprezy[imprezy]
        + mapa_alkohol[alkohol]
        + mapa_papierosy[papierosy]
        + mapa_relaks[relaks]
    )

    max_score = 4 + 4 + 3 + 3 + 3 + 4 + 4  # maksymalna liczba punktów
    stress_level = round(raw_score / max_score * 10, 1)  # skala 0–10

    st.subheader(f"Twój poziom stresu: **{stress_level} / 10**")

    if stress_level <= 3:
        st.success("Niski poziom stresu 🙂")
    elif stress_level <= 6:
        st.info("Średni poziom stresu 😐 Warto zadbać o odpoczynek.")
    else:
        st.error("Wysoki poziom stresu 😵 Spróbuj zwiększyć sen i aktywności odstresowujące.")

