import joblib
import pandas as pd

MODEL_PATH = "results/best_model.joblib"

FEATURES = [
    "ile_godzin_spisz_srednio_na_dob",
    "ile_kaw_napojow_energetycznych_250_ml_spozywasz_w_ciagu_dnia",
    "ile_ile_godzin_dziennie_poswiecasz_na_nauke",
    "ile_dni_w_tygodniu_cwiczysz",
    "jak_czesto_spozywasz_alkohol",
    "jak_czesto_palisz_papierosy",
    "ile_razy_w_miesiacu_uczestniczysz_w_aktywnosciach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle",
]

def ask_float(prompt: str) -> float:
    while True:
        s = input(prompt).strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            print("Wpisz liczbę (np. 7 albo 7.5).")

def ask_text(prompt: str) -> str:
    s = input(prompt).strip()
    return s

def main():
    pipe = joblib.load(MODEL_PATH)

    print("KALKULATOR: Predykcja wysokiego stresu (HIGH vs NOT_HIGH)\n")

    x = {}
    x["ile_godzin_spisz_srednio_na_dob"] = ask_float("Ile godzin śpisz średnio na dobę? ")
    x["ile_kaw_napojow_energetycznych_250_ml_spozywasz_w_ciagu_dnia"] = ask_float(
        "Ile kaw/energetyków 250 ml dziennie? "
    )
    x["ile_ile_godzin_dziennie_poswiecasz_na_nauke"] = ask_float("Ile godzin dziennie poświęcasz na naukę? ")
    x["ile_dni_w_tygodniu_cwiczysz"] = ask_float("Ile dni w tygodniu ćwiczysz? ")

    # Te dwie kolumny zwykle są kategoryczne (np. 'nigdy', 'czasem', 'często').
    # Wpisuj dokładnie tak, jak było w ankiecie w Excelu.
    x["jak_czesto_spozywasz_alkohol"] = ask_text("Jak często spożywasz alkohol? (np. nigdy/czasem/często) ")
    x["jak_czesto_palisz_papierosy"] = ask_text("Jak często palisz papierosy? (np. nigdy/czasem/często) ")

    x["ile_razy_w_miesiacu_uczestniczysz_w_aktywnosciach_odstresowujacych_npkino_zakupy_spacery_restauracja_kregle"] = ask_float(
        "Ile razy w miesiącu robisz aktywności odstresowujące? "
    )

    df = pd.DataFrame([x], columns=FEATURES)

    pred = pipe.predict(df)[0]
    print(f"\nWynik: {pred}")

    # jeśli model ma predict_proba (ExtraTrees ma), pokaż prawdopodobieństwo HIGH
    if hasattr(pipe, "predict_proba"):
        proba = pipe.predict_proba(df)[0]
        classes = list(pipe.classes_)
        if "HIGH" in classes:
            p_high = proba[classes.index("HIGH")]
            print(f"Prawdopodobieństwo HIGH: {p_high:.3f}")

if __name__ == "__main__":
    main()
