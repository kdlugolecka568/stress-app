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

import joblib
import pandas as pd
import streamlit as st

# Ścieżka do modelu
def main():
    pipe = joblib.load(best_model.joblib)
    print("KALKULATOR: Predykcja wysokiego stresu (WYSOKI vs NIE_WYSOKI)\n")

    sleep_opts = ["Mniej niż 5", "5-6", "7-8", "Więcej niż 8"]
    caffeine_opts = ["0", "1", "2", "3", "4 lub więcej"]
    study_opts = ["Mniej niż 1 godzinę", "1-2 godziny", "3-4 godziny", "5 lub więcej"]
    exercise_opts = ["0", "1-2 dni", "3-4 dni", "5-6 dni", "Codziennie"]
    alc_opts = ["Nigdy", "Sporadycznie (raz w miesiącu lub rzadziej)", "Kilka razy w miesiącu", "Regularnie (kilka razy w tygodniu)"]
    smoke_opts = ["Nigdy", "Sporadycznie (np. przy okazji imprezy)", "Kilka razy w tygodniu", "Codziennie"]
    relax_opts = ["W ogóle (0 razy w miesiącu)", "Rzadko (1-2 razy w miesiącu)", "Kilka razy w miesiącu (3-5 razy)", "Często (6 lub więcej razy w miesiącu)"]

    SLEEP_MAP = {1: 4.5, 2: 5.5, 3: 7.5, 4: 8.5}
    CAFFEINE_MAP = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    STUDY_MAP = {1: 0.5, 2: 1.5, 3: 3.5, 4: 5.0}
    EXERCISE_MAP = {1: 0, 2: 1.5, 3: 3.5, 4: 5.5, 5: 7}
    ALC_MAP = {1: 1, 2: 2, 3: 3, 4: 4}
    SMOKE_MAP = {1: 1, 2: 2, 3: 3, 4: 4}
    RELAX_MAP = {1: 0.0, 2: 1.5, 3: 4.0, 4: 6.0}

    questions = [
        ("ile_godzin_spisz_srednio_na_dob", "1/7 Ile godzin śpisz średnio na dobę?", sleep_opts, SLEEP_MAP),
        ("ile_kaw_napojow_energetycznych_250_ml_spozywasz_w_ciagu_dnia", "2/7 Ile kaw/ napojów energetycznych (250 ml) spożywasz w ciągu dnia?", caffeine_opts, CAFFEINE_MAP),
        ("ile_ile_godzin_dziennie_poswiecasz_na_nauke", "3/7 Ile godzin dziennie poświęcasz na naukę?", study_opts, STUDY_MAP),
        ("ile_dni_w_tygodniu_cwiczysz", "4/7 Ile dni w tygodniu ćwiczysz?", exercise_opts, EXERCISE_MAP),
        ("jak_czesto_spozywasz_alkohol", "5/7 Jak często spożywasz alkohol?", alc_opts, ALC_MAP),
        ("jak_czesto_palisz_papierosy", "6/7 Jak często palisz papierosy?", smoke_opts, SMOKE_MAP),
        ("ile_razy_w_miesiacu_uczestniczysz_w_aktywnościach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle".replace("ą", "a").replace("ł", "l"), "", [], {}),  # placeholder to keep code compact
    ]
    # poprawny ostatni rekord (bez kombinowania z polskimi znakami)
    questions[-1] = (
        "ile_razy_w_miesiacu_uczestniczysz_w_aktywnosciach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle",
        "7/7 Ile razy w miesiącu uczestniczysz w aktywnościach odstresowujących (np. kino, zakupy, spacery, restauracja, kręgle)?",
        relax_opts,
        RELAX_MAP,
    )

    x = {}
    summary = []

    for col, q, opts, mapper in questions:
        k, label = ask_option(q, opts)
        x[col] = mapper[k]
        if ' ' in q:
            st.write(f"- {q.split(' ', 1)[1]}: {label}")
        else:
            st.write(f"- {q}: {label}")

    df = pd.DataFrame([x], columns=FEATURES)

    pred = pipe.predict(df)[0]
    p_high = None

    if hasattr(pipe, "predict_proba"):
        proba = pipe.predict_proba(df)[0]
        classes = list(pipe.classes_)
        if "HIGH" in classes:
            p_high = float(proba[classes.index("HIGH")])
        if USE_THRESHOLD and p_high is not None:
            pred = "HIGH" if p_high >= THRESHOLD else "NIE_WYSOKI"

    st.write(f"\nWynik: {pred}")
    if p_high is not None:
        st.write(f"Prawdopodobieństwo WYSOKIEGO_STRESU: {p_high:.3f}")
        if USE_THRESHOLD:
            st.write(f"Próg WYSOKIEGO_STRESU: {THRESHOLD:.2f}")
        st.write(f"Ocena ryzyka WYSOKIEGO_STRESU: {risk_level(p_high)}")

if __name__ == "__main__":
    main()




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


      
