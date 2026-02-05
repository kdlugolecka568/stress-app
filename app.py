import os
import hashlib
import streamlit as st
import pandas as pd
import joblib
from utils import risk_level

# -------------------------------------------------
# USTAWIENIA STRONY (MUSI BYĆ ZANIM COKOLWIEK st.*)
# -------------------------------------------------
st.set_page_config(page_title="Kalkulator stresu", layout="centered")

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

@st.cache_resource(show_spinner=False)
def _load_pipe(path: str):
    return joblib.load(path)

def ask_option(question: str, options: list[str]) -> tuple[int, str]:
    # legenda była tu wcześniej wyświetlana; teraz nie pokazujemy jej w UI
    legend = " ".join([f"[{i+1}={opt}]" for i, opt in enumerate(options)])

    key = "opt_" + hashlib.md5(question.encode("utf-8")).hexdigest()
    k = st.radio(
        question,
        options=list(range(1, len(options) + 1)),
        format_func=lambda i: f"{i}. {options[i - 1]}",
        key=key,
    )
    return int(k), options[int(k) - 1]


def main():
    st.title("KALKULATOR: Predykcja wysokiego stresu (WYSOKI vs NIE_WYSOKI)")

    try:
        pipe = _load_pipe(MODEL_PATH)
        st.success(f"Model wczytany z: {MODEL_PATH}")
    except Exception as e:
        st.error(f"Nie udało się wczytać modelu z: {MODEL_PATH}")
        st.code(str(e))
        st.info("Upewnij się, że plik istnieje obok app.py (w katalogu projektu) lub zmień MODEL_PATH.")
        st.stop()

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
        ("ile_razy_w_miesiacu_uczestniczysz_w_aktywnościach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle".replace("ą", "a").replace("ł", "l"), "", [], {}),
    ]
    questions[-1] = (
        "ile_razy_w_miesiacu_uczestniczysz_w_aktywnosciach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle",
        "7/7 Ile razy w miesiącu uczestniczysz w aktywnościach odstresowujących (np. kino, zakupy, spacery, restauracja, kręgle)?",
        relax_opts,
        RELAX_MAP,
    )

    with st.form("stress_form"):
        x = {}
        summary = []

        for col, q, opts, mapper in questions:
            k, label = ask_option(q, opts)
            x[col] = mapper[k]
            summary.append((q.split(" ", 1)[1], label))

        submitted = st.form_submit_button("Oblicz wynik")

    if not submitted:
        st.info("Uzupełnij odpowiedzi i kliknij **Oblicz wynik**.")
        return

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

    LABEL_MAP = {
        "HIGH": "WYSOKI",
        "NIE_WYSOKI": "NIE_WYSOKI",
        "NOT_HIGH": "NIE_WYSOKI",
    }
    pred_pl = LABEL_MAP.get(str(pred), str(pred))

    st.subheader("Wynik")
    st.write(f"**Wynik:** {pred_pl}")

    if p_high is not None:
        st.write(f"**Prawdopodobieństwo WYSOKIEGO_STRESU:** {p_high:.3f}")
        if USE_THRESHOLD:
            st.write(f"**Założony próg WYSOKIEGO_STRESU:** {THRESHOLD:.2f}")
        st.write(f"**Ocena ryzyka WYSOKIEGO_STRESU:** {risk_level(p_high)}")

    st.info(
        "To narzędzie ma charakter informacyjny i pokazuje **predykcję modelu**, a nie diagnozę. "
        "Jeśli stres utrzymuje się długo, wpływa na sen/naukę/codzienne funkcjonowanie lub masz pogorszone samopoczucie — "
        "warto skonsultować się ze specjalistą (psycholog/psychoterapeuta/lekarz). "
        "W sytuacji zagrożenia zdrowia lub życia dzwoń pod **112**."
    )

    with st.expander("Legenda wyjaśniająca poziomy ryzyka"):
        st.write(" - niskie: Prawdopodobieństwo stresu poniżej 20% (bardzo małe ryzyko).")
        st.write(" - umiarkowane: Prawdopodobieństwo stresu między 20% a 40% (średnie ryzyko).")
        st.write(" - podwyższone: Prawdopodobieństwo stresu między 40% a 60% (wysokie ryzyko).")
        st.write(" - wysokie: Prawdopodobieństwo stresu powyżej 60% (bardzo wysokie ryzyko).")

# ------------------
# ROUTING STRON
# ------------------
if page == "Kalkulator":
    main()

elif page == "Jak obniżyć stres?":
    st.title("Jak obniżyć poziom stresu?")

    st.write("""
    Stres jest naturalną reakcją organizmu na wymagające sytuacje. Może mobilizować do działania,
    ale w nadmiarze utrudnia naukę, sen i koncentrację oraz prowadzi do przeciążenia.
    Poniżej kilka strategii, które często realnie pomagają.
    """)

    st.subheader("1. Popraw higienę snu")
    st.write("""
    - stałe godziny snu i pobudki,
    - ogranicz ekrany minimum godzinę przed snem,
    - zmniejsz kofeinę po godz. 15–16,
    - zadbaj o chłodne, ciche i ciemne środowisko snu.
    """)

    st.subheader("2. Regularna aktywność fizyczna")
    st.write("""
    **20–30 minut ruchu dziennie** może obniżać napięcie i poprawiać sen.
    Wystarczy spacer, rower, taniec lub joga — nie musi to być siłownia.
    """)

    st.subheader("3. Organizacja czasu")
    st.write("""
    - plan tygodnia,
    - dzielenie dużych zadań na mniejsze,
    - priorytetyzacja (co jest „na już”, a co może poczekać).
    """)

    st.subheader("4. Uważna kofeina")
    st.write("""
    Kofeina u części osób nasila niepokój i pogarsza sen. Obserwuj ilość oraz godzinę picia.
    Czasem 1 kawa mniej robi zauważalną różnicę.
    """)

    st.subheader("5. Kontakt z innymi")
    st.write("""
    Wsparcie społeczne działa jak bufor stresu — rozmowa lub wspólna aktywność realnie obniża napięcie.
    """)

    st.subheader("6. Techniki relaksacyjne")
    st.write("""
    - ćwiczenia oddechowe,
    - mindfulness,
    - stretching / joga.
    Już 10 minut dziennie pomaga.
    """)

    st.subheader("7. Monitorowanie stresorów")
    st.write("""
    Zapisuj: kiedy pojawia się stres, co go wywołało i co pomogło. Po kilku dniach zwykle widać wzorce.
    """)

    st.subheader("Kiedy warto szukać pomocy specjalisty?")
    st.write("""
    Warto rozważyć konsultację, jeśli:
    - stres utrzymuje się przez wiele tygodni i nie mija mimo odpoczynku,
    - masz problemy ze snem większość nocy,
    - pojawiają się napady lęku/paniki albo stałe napięcie,
    - spada koncentracja i funkcjonowanie na studiach/pracy,
    - pojawiają się myśli samobójcze lub autoagresywne (wtedy pilnie).
    """)

elif page == "O projekcie":
    st.title("O projekcie")

    st.write("""
    Celem projektu jest stworzenie modelu predykcyjnego, który ocenia ryzyko **podwyższonego poziomu stresu**
    u studentów na podstawie ich nawyków i stylu życia.

    ### Dane wejściowe
    - ilość snu
    - spożycie kawy i energetyków
    - aktywność fizyczna
    - czas poświęcany na naukę
    - alkohol
    - papierosy
    - aktywności odstresowujące

    ### Zastosowania
    - narzędzie samooceny
    - element wsparcia
    - część badań
    - przykład aplikacji ML
    """)

    st.warning(
        "Uwaga: wynik jest wyłącznie **predykcją statystyczną** na podstawie odpowiedzi użytkownika. "
        "Nie zastępuje konsultacji ze specjalistą ani diagnozy."
    )
