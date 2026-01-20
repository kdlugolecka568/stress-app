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
    st.title("Kalkulator stresu studenta")
    st.write("Wypełnij pola poniżej, aby oszacować poziom stresu.")
    
    # ---------------------------------------
    #  KALKULATOR 
    # ---------------------------------------
    pass   # ← usuń, gdy wkleisz kalkulator

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

    ---
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


      
