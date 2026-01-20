import streamlit as st

st.header("Czym jest stres?")
st.write("""
Stres to naturalna reakcja organizmu na wymagające sytuacje. Może mobilizować
do działania, ale w nadmiarze prowadzi do przemęczenia, zaburzeń snu i problemów zdrowotnych.
""")



st.set_page_config(page_title="Kalkulator stresu studenta")

st.title(" Kalkulator stresu studenta")

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
# STRONY
# ------------------

if page == "Kalkulator":
    st.title("Kalkulator stresu studenta 🧠🎓")
    st.write("Wypełnij pola poniżej, aby oszacować poziom stresu.")
    
    # ---------------------------------------
    # 🔽🔽🔽  TU WKLEJASZ SWÓJ KALKULATOR  🔽🔽🔽
    # ---------------------------------------

    # przykład loadera:
    # pipe = joblib.load("best_model.joblib")

    # tu wklejasz cały kod z pytaniami i predykcją
    # ...
    
    # ---------------------------------------
    # 🔼🔼🔼  TU WKLEJASZ SWÓJ KALKULATOR  🔼🔼🔼
    # ---------------------------------------


elif page == "Jak obniżyć stres?":
    st.title("📉 Jak obniżyć poziom stresu?")
    st.write("""
Stres jest naturalną reakcją organizmu, ale w nadmiarze może utrudniać naukę, sen i koncentrację.
Poniżej znajduje się kilka strategii potwierdzonych badaniami, które pomagają zmniejszać poziom stresu:
""")

    st.subheader("🛏 1. Popraw higienę snu")
    st.write("- stałe godziny snu\n- mniej ekranów przed snem\n- ograniczenie kofeiny wieczorem")

    st.subheader("🏃 2. Regularna aktywność")
    st.write("Już 20–30 minut ruchu dziennie poprawia nastrój i obniża napięcie.")

    st.subheader("🗂 3. Organizacja czasu")
    st.write("Planowanie tygodnia, metoda 2-minut, priorytetyzacja — to redukuje chaos i stres.")

    st.subheader("☕ 4. Uważna kofeina")
    st.write("Kofeina poprawia koncentrację, ale może zwiększać niepokój i pogarszać sen.")

    st.subheader("👥 5. Kontakt z innymi")
    st.write("Rozmowa z kimś bliskim, wspólne aktywności czy wsparcie emocjonalne działają amortyzująco.")

    st.subheader("🧘 6. Techniki relaksacyjne")
    st.write("Medytacja, ćwiczenia oddechowe, joga lub stretching obniżają pobudzenie układu nerwowego.")

    st.subheader("📝 7. Monitorowanie stresorów")
    st.write("Świadomość tego *co* i *kiedy* Cię stresuje zwiększa kontrolę nad reakcją organizmu.")


elif page == "O projekcie":
    st.title("🎓 O projekcie")

    st.write("""
Celem projektu jest stworzenie modelu predykcyjnego, który ocenia ryzyko **podwyższonego poziomu stresu**
u studentów na podstawie ich nawyków i stylu życia.

---

### 🧩 **Dane wejściowe**
Zebrane dane dotyczyły m.in.:
- ilości snu
- spożycia kawy i energetyków
- aktywności fizycznej
- czasu poświęcanego na naukę
- spożycia alkoholu
- palenia papierosów
- aktywności odstresowujących

---

### 🤖 **Model**
Zastosowano algorytm:
- **ExtraTreesClassifier**

oraz techniki:
- **RepeatedStratifiedKFold (5×5)**
- **RandomizedSearchCV** do strojenia
- oceny metryk: **F1-score**, **Balanced Accuracy**, **ROC-AUC**

---

### 🧠 **Narzędzia**
Projekt korzystał z:
- Python
- Pandas / NumPy
- Scikit-learn
- Streamlit
- joblib

---

### 🎯 **Zastosowania**
Aplikacja może być użyta jako:
- narzędzie samooceny dla studentów,
- element wsparcia psychologicznego,
- część badań naukowych,
- przykład aplikacji ML.

""")


      
