import streamlit as st
import pandas as pd
import joblib

# ------------------
# SIDEBAR MENU
# ------------------

page = st.sidebar.radio(
    "Nawigacja",
    ["Kalkulator", "Jak obniżyć stres?", "O projekcie"]
)

# ------------------
# KONFIGURACJA MODELU
# ------------------

MODEL_PATH = "best_model.joblib"
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

# ------------------
# STRONY
# ------------------

if page == "Kalkulator":
    st.title("🧠 Kalkulator stresu studenta")
    st.write("Wypełnij pola poniżej, aby oszacować poziom stresu.")

    # ładowanie modelu
    try:
        pipe = joblib.load(MODEL_PATH)
    except:
        st.error("❌ Nie znaleziono modelu! Upewnij się, że plik best_model.joblib jest w folderze results/")
        st.stop()

    # opcje odpowiedzi
    sleep_opts = ["Mniej niż 5", "5-6", "7-8", "Więcej niż 8"]
    caffeine_opts = ["0", "1", "2", "3", "4 lub więcej"]
    study_opts = ["Mniej niż 1 godzinę", "1-2 godziny", "3-4 godziny", "5 lub więcej"]
    exercise_opts = ["0", "1-2 dni", "3-4 dni", "5-6 dni", "Codziennie"]
    alc_opts = ["Nigdy", "Sporadycznie", "Kilka razy w miesiącu", "Regularnie"]
    smoke_opts = ["Nigdy", "Sporadycznie", "Kilka razy w tygodniu", "Codziennie"]
    relax_opts = ["0 razy", "1-2 razy", "3-5 razy", "6+ razy"]

    # mapowania
    SLEEP_MAP = {"Mniej niż 5": 4.5, "5-6": 5.5, "7-8": 7.5, "Więcej niż 8": 8.5}
    CAFFEINE_MAP = {"0": 0, "1": 1, "2": 2, "3": 3, "4 lub więcej": 4}
    STUDY_MAP = {"Mniej niż 1 godzinę": 0.5, "1-2 godziny": 1.5, "3-4 godziny": 3.5, "5 lub więcej": 5.0}
    EXERCISE_MAP = {"0": 0, "1-2 dni": 1.5, "3-4 dni": 3.5, "5-6 dni": 5.5, "Codziennie": 7}
    ALC_MAP = {"Nigdy": 1, "Sporadycznie": 2, "Kilka razy w miesiącu": 3, "Regularnie": 4}
    SMOKE_MAP = {"Nigdy": 1, "Sporadycznie": 2, "Kilka razy w tygodniu": 3, "Codziennie": 4}
    RELAX_MAP = {"0 razy": 0.0, "1-2 razy": 1.5, "3-5 razy": 4.0, "6+ razy": 6.0}

    st.subheader("Wprowadź informacje:")

    x = {
        "ile_godzin_spisz_srednio_na_dob": SLEEP_MAP[st.selectbox("Ile godzin śpisz na dobę?", sleep_opts)],
        "ile_kaw_napojow_energetycznych_250_ml_spozywasz_w_ciagu_dnia": CAFFEINE_MAP[st.selectbox("Ile kaw/energetyków dziennie?", caffeine_opts)],
        "ile_ile_godzin_dziennie_poswiecasz_na_nauke": STUDY_MAP[st.selectbox("Ile godzin dziennie na naukę?", study_opts)],
        "ile_dni_w_tygodniu_cwiczysz": EXERCISE_MAP[st.selectbox("Ile dni ćwiczysz w tygodniu?", exercise_opts)],
        "jak_czesto_spozywasz_alkohol": ALC_MAP[st.selectbox("Jak często pijesz alkohol?", alc_opts)],
        "jak_czesto_palisz_papierosy": SMOKE_MAP[st.selectbox("Jak często palisz papierosy?", smoke_opts)],
        "ile_razy_w_miesiacu_uczestniczysz_w_aktywnosciach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle": RELAX_MAP[st.selectbox("Jak często robisz aktywności odstresowujące?", relax_opts)],
    }

    df = pd.DataFrame([x], columns=FEATURES)

    if st.button("Oblicz wynik"):
        pred = pipe.predict(df)[0]
        p_high = None

        if hasattr(pipe, "predict_proba"):
            proba = pipe.predict_proba(df)[0]
            classes = list(pipe.classes_)
            if "HIGH" in classes:
                p_high = float(proba[classes.index("HIGH")])
            if USE_THRESHOLD and p_high is not None:
                pred = "HIGH" if p_high >= THRESHOLD else "NOT_HIGH"

        st.subheader("📊 Wynik:")
        st.write(f"**Klasyfikacja:** {pred}")

        if p_high is not None:
            st.write(f"**Prawdopodobieństwo HIGH:** {p_high:.2f}")
            st.write(f"**Ocena ryzyka:** {risk_level(p_high)}")



elif page == "Jak obniżyć stres?":
    st.title("Jak obniżyć poziom stresu?")
    
    st.write("""
    Stres jest naturalną reakcją organizmu na wymagające sytuacje. Może mobilizować do działania,
    ale w nadmiarze utrudnia naukę, sen i koncentrację oraz prowadzi do przeciążenia.
    Poniżej znajduje się kilka strategii potwierdzonych badaniami, które pomagają zmniejszać poziom stresu.
    """)

    # 1. HIGIENA SNU
    st.subheader("1. Popraw higienę snu")
    st.write("""
    Sen ma ogromny wpływ na regulację emocji i funkcjonowanie układu nerwowego.
    Przy przewlekłym stresie mózg jest bardziej pobudzony, co utrudnia zasypianie i pogarsza jakość snu.

    **Co możesz zrobić:**
    - ustal stałe godziny snu i pobudki (nawet w weekendy),
    - ogranicz ekrany minimum godzinę przed snem,
    - zmniejsz kofeinę po godz. 15–16,
    - zadbaj o chłodne, ciche i ciemne środowisko snu.

    30–60 minut więcej snu może obniżyć poziom napięcia i poprawić koncentrację.
    """)

    # 2. AKTYWNOŚĆ FIZYCZNA
    st.subheader("2. Regularna aktywność fizyczna")
    st.write("""
    Ruch działa jak naturalny antydepresant. Badania pokazują, że **20–30 minut aktywności dziennie**:
    - obniża napięcie mięśniowe,
    - poprawia nastrój,
    - zmniejsza hormony stresu (kortyzol),
    - poprawia jakość snu.

    Nie musi to być siłownia — wystarczy spacer, rower, taniec lub joga.
    """)

    # 3. ORGANIZACJA CZASU
    st.subheader("3. Organizacja czasu")
    st.write("""
    Chaos i natłok obowiązków wzmacniają stres. Planowanie pomaga odzyskać poczucie kontroli.

    **Pomagają m.in.:**
    - planowanie tygodniowe,
    - metoda 2 minut (jeśli coś trwa <2 min — zrób od razu),
    - dzielenie dużych zadań na mniejsze,
    - priorytetyzacja (np. macierz Eisenhowera).

    Już sama struktura i porządek zmniejszają obciążenie psychiczne.
    """)

    # 4. UWAŻNA KOFEINA
    st.subheader("4. Uważna kofeina")
    st.write("""
    Kofeina poprawia koncentrację, ale u wielu osób może zwiększać niepokój, pobudzenie i utrudniać sen.

    **Warto obserwować:**
    - ile kaw/energetyków pijesz,
    - o której godzinie,
    - jak wpływają na Twoje samopoczucie.

    Czasem 1 kawa mniej dziennie robi zauważalną różnicę.
    """)

    # 5. KONTAKT SPOŁECZNY
    st.subheader("5. Kontakt z innymi")
    st.write("""
    Wsparcie społeczne jest jednym z najskuteczniejszych „buforów stresu”.

    Rozmowa, spacer, wspólne wyjście lub sama obecność kogoś zaufanego:
    - obniża napięcie,
    - pomaga spojrzeć na problem z dystansu,
    - daje poczucie bezpieczeństwa.

    Nawet krótki telefon potrafi zdziałać dużo.
    """)

    # 6. TECHNIKI RELAKSACYJNE
    st.subheader("6. Techniki relaksacyjne")
    st.write("""
    Techniki relaksacyjne aktywują układ przywspółczulny, który obniża napięcie i uspokaja ciało.

    Najbardziej przebadane metody:
    - ćwiczenia oddechowe (np. 4–4–6, box-breathing),
    - medytacja mindfulness,
    - joga i stretching,
    - progresywna relaksacja mięśni.

    Już 10 minut dziennie przynosi widoczne efekty.
    """)

    # 7. MONITOROWANIE STRESORÓW
    st.subheader("7. Monitorowanie stresorów")
    st.write("""
    Monitorowanie stresorów polega na identyfikowaniu sytuacji i reakcji, które wywołują napięcie.
    To zwiększa samoświadomość i poczucie kontroli.

    **Co obserwować:**
    - **kiedy** pojawia się stres,
    - **co** go wywołało (sytuacja, miejsce, osoba),
    - **jak** reaguje ciało (np. napięcie, kołatanie serca),
    - **jak** reagujesz emocjonalnie,
    - **co** pomaga, a co pogarsza sytuację.

    Po kilku dniach widać powtarzające się wzorce, np.:
    - „sen <6h = gorszy dzień”,
    - „najbardziej stresują mnie zadania bez określonego deadline’u”,
    - „kontakt z kimś mnie uspokaja”.

    To podejście jest stosowane w psychologii klinicznej i znacząco poprawia regulację emocji.
    """)

elif page == "O projekcie":
    st.title("O projekcie")

    st.write("""
    Celem projektu jest stworzenie modelu predykcyjnego, który ocenia ryzyko **podwyższonego poziomu stresu**
    u studentów na podstawie ich nawyków i stylu życia.

  
### **Dane wejściowe**
Dane dotyczyły m.in.:
- ilości snu
- spożycia kawy i energetyków
- aktywności fizycznej
- czasu poświęcanego na naukę
- spożycia alkoholu
- palenia papierosów
- aktywności odstresowujących

---
### **Zastosowania**
Aplikacja może być użyta jako:
- narzędzie samooceny dla studentów,
- element wsparcia psychologicznego,
- część badań naukowych,
- przykład aplikacji ML.
    """)


      
