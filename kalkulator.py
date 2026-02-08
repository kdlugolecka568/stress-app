MODEL_PATH = "/content/best_model.joblib"

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

def ask_option(question: str, options: list[str]) -> tuple[int, str]:
    legend = " ".join([f"[{i+1}={opt}]" for i, opt in enumerate(options)])
    base_prompt = f"{question} {legend}: "
    prompt = base_prompt
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            k = int(s)
            if 1 <= k <= len(options):
                return k, options[k - 1]
        prompt = f"BŁĄD!: WPISZ NUMER Z PODANYCH. Pytanie: {base_prompt}"

def risk_level(p_high: float) -> str:
    if p_high < 0.20:
        return "niskie"
    if p_high < 0.40:
        return "umiarkowane"
    if p_high < 0.60:
        return "podwyższone"
    return "wysokie"

def main():
    pipe = joblib.load(MODEL_PATH)
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
        summary.append((q.split(" ", 1)[1], label))  # bez "1/7 "

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

    print("\nTwoje odpowiedzi:")
    for q, label in summary:
        print(f"- {q}: {label}")

    print(f"\nWynik: {pred}")
    if p_high is not None:
        print(f"Prawdopodobieństwo WYSOKIEGO_STRESU: {p_high:.3f}")
        if USE_THRESHOLD:
            print(f"Próg WYSOKIEGO_STRESU: {THRESHOLD:.2f}")
        print(f"Ocena ryzyka WYSOKIEGO_STRESU: {risk_level(p_high)}")

if __name__ == "__main__":
    main()


# Legenda wyjaśniająca poziomy ryzyka
print("\nLegenda wyjaśniająca poziomy ryzyka:")
print(" - niskie: Prawdopodobieństwo stresu poniżej 20% (bardzo małe ryzyko).")
print(" - umiarkowane: Prawdopodobieństwo stresu między 20% a 40% (średnie ryzyko).")
print(" - podwyższone: Prawdopodobieństwo stresu między 40% a 60% (wysokie ryzyko).")
print(" - wysokie: Prawdopodobieństwo stresu powyżej 60% (bardzo wysokie ryzyko).")

#"""
#    Funkcja główna, która uruchamia kalkulator do predykcji wysokiego stresu (HIGH vs NOT_HIGH).
#    Zawiera pytania dotyczące różnych aspektów życia, takich jak sen, kawa, nauka, ćwiczenia, alkohol, papierosy i relaks.
#    Na podstawie odpowiedzi użytkownika oblicza prawdopodobieństwo wystąpienia wysokiego stresu oraz ocenia ryzyko.
#
#    Funkcja wykonuje następujące kroki:
#    1. Ładuje wytrenowany model za pomocą joblib (plik: "results/best_model.joblib").
#    2. Zadaje użytkownikowi pytania dotyczące stylu życia.
#    3. Mapuje odpowiedzi użytkownika na liczby, które są używane do predykcji.
#    4. Na podstawie odpowiedzi oblicza wynik klasyfikacji: "HIGH" lub "NOT_HIGH".
#   5. Oblicza prawdopodobieństwo wysokiego stresu (jeśli dostępne) i ocenia ryzyko.
#
#    Args:
#        Brak.
#
#    Returns:
#        None.

#Próg 0.40 dla klasyfikacji "WYSOKI" został wybrany na podstawie analizy wyników metryk modelu oraz rozkładu prawdopodobieństwa. Został on ustalony tak, aby zapewnić równowagę między precyzją a czułością w klasyfikacji.

#Uzasadnienie wyboru progu 0.40:


#  Model klasyfikacyjny oblicza prawdopodobieństwo przynależności danego przypadku do klasy "WYSOKI". Zgodnie z rozkładem, jeśli wartość P(WYSOKI) jest wyższa niż 40%, oznacza to, że model jest wystarczająco pewny, by przypisać przypadek do tej klasy.
#    Wartość ta została wybrana, aby  zminimalizować liczbę błędów fałszywie pozytywnych.


#   Na podstawie metryk F1-score i balanced accuracy z wyników modelu, próg 0.40 pozwala uzyskać dobrą jakość predykcji dla klasy "WYSOKI". Wyższy próg (np. 0.50) mógłby zmniejszyć liczbę klasyfikacji fałszywie pozytywnych, ale również prowadzić do większej liczby fałszywych negatywów, co mogłoby skutkować w missed cases w kontekście identyfikacji osób z wysokim stresem.
#   Z kolei próg 0.30 mógłby zbyt mocno zredukować precyzję, skutkując nadmiernym przypisaniem przypadków do klasy "WYSOKI", co może obniżyć jakość klasyfikacji.


#   Dzięki temu progowi model uzyskuje dobrą zdolność identyfikowania osób z wysokim stresem, zachowując odpowiednią precyzję (tj. minimalizując liczbę fałszywych pozytywnych klasyfikacji) oraz wysoką czułość (tzw. recall), co przekłada się na rzetelność i trafność predykcji.



#"""    
