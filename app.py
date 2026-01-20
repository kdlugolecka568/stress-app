import streamlit as st

st.header("Czym jest stres?")
st.write("""
Stres to naturalna reakcja organizmu na wymagające sytuacje. Może mobilizować
do działania, ale w nadmiarze prowadzi do przemęczenia, zaburzeń snu i problemów zdrowotnych.
""")



st.set_page_config(page_title="Kalkulator stresu studenta")

st.title(" Kalkulator stresu studenta")

with st.expander("📉 Jak obniżyć poziom stresu?"):
    st.write("""
        **1. Popraw higienę snu** — stałe godziny, mniej ekranów przed snem, mniej kofeiny popołudniami.
        **2. Aktywność fizyczna** — 20-30 min dziennie obniża napięcie i poprawia nastrój.
        **3. Organizacja czasu** — priorytetyzacja, plan tygodniowy, metoda 2 minut.
        **4. Uważna kofeina** — ograniczenie może zmniejszyć niepokój i poprawić sen.
        **5. Kontakt społeczny** — wspólne aktywności amortyzują stres.
        **6. Techniki relaksacyjne** — medytacja, oddech, stretching.
        **7. Monitorowanie stresorów** — identyfikacja i obserwacja reakcji.
    """)

with st.expander("🎓 O projekcie"):
    st.write("""
        Celem projektu jest stworzenie modelu oceniającego ryzyko wysokiego stresu u studentów
        na podstawie stylu życia i nawyków.
        
        **Dane wejściowe**: sen, kofeina, aktywność fizyczna, nauka, alkohol, palenie, hobby.
        
        **Metody**:
        - Python (Pandas, NumPy)
        - Scikit-learn (ExtraTreesClassifier, CV 5×5, RandomizedSearchCV)
        - Streamlit (aplikacja web)
        - joblib (zapis/ładowanie modelu)

        **Zastosowania**: samoocena, badania, edukacja, narzędzia well-being.
    """)

