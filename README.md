## Opis projektu
Projekt polega na stworzeniu modelu uczenia maszynowego prognozującego ryzyko wystąpienia wysokiego poziomu stresu na podstawie odpowiedzi z ankiety dotyczącej stylu życia. Model został udostępniony w formie interaktywnej aplikacji Streamlit, umożliwiającej użytkownikowi szybkie uzyskanie predykcji.
Uwaga: model nie stanowi diagnozy medycznej - wynik ma charakter wyłącznie informacyjny.


## Dane
Dane pochodzą z ankiety Google Forms (ok. 100 odpowiedzi) i są zapisane w pliku Excel (wersjonowanym przez DVC). Pytania dotyczyły m.in. snu, aktywności fizycznej, spożycia kawy i alkoholu, palenia papierosów oraz aktywności odstresowujących.

Zmienna docelowa ma postać binarną:
- HIGH (WYSOKI stres)
- NOT_HIGH (NIE_WYSOKI stres)


## Podejście ML i strategia uczenia
Przetestowano dwa modele:
- Logistic Regression
- Extra Trees Classifier (model finalny)

Model finalny: **Extra Trees Classifier** - wybrany ze względu na lepszy wynik dla klasy HIGH (klasa priorytetowa).

### Preprocessing
W projekcie zastosowano pipeline obejmujący:
- imputację braków w danych numerycznych (mediana),
- imputację braków w danych kategorycznych (najczęstsza wartość),
- kodowanie One-Hot Encoding dla zmiennych kategorycznych.

### Walidacja i strojenie hiperparametrów
Uczenie realizowane jest w pliku `train.py` z użyciem:
- podziału danych: 65% / 35% (train / test),
- strojenia hiperparametrów: **RandomizedSearchCV** (`n_iter=40`),
- walidacji krzyżowej: **RepeatedStratifiedKFold** (`n_splits=5`, `n_repeats=5`),
- metryki optymalizacyjnej ukierunkowanej na klasę HIGH: **F1(HIGH)**  
  (w kodzie: `scoring={"f1_high": ...}` oraz `refit="f1_high"`).


## Wyniki (HOLDOUT - zbiór testowy)

### Logistic Regression
LogisticRegression - HOLDOUT
- BA: 0.8177
- F1(HIGH): 0.7273
-      CM:
           [[ 4  2]
            [ 1 31]]


                 precision    recall  f1-score   support

          HIGH       0.80      0.67      0.73         6
      NOT_HIGH       0.94      0.97      0.95        32
  
      accuracy                           0.92        38



ExtraTreesClassifier - HOLDOUT
- BA: 0.8333
- F1(HIGH): 0.8000
-     CM:
           [[ 4  2]
            [ 0 32]]

                 precision    recall  f1-score   support
          HIGH       1.00      0.67      0.80         6
      NOT_HIGH       0.94      1.00      0.97        32

      accuracy                           0.95        38

## Aplikacja (Streamlit)
Plik `app.py` ładuje wytrenowany model z:
- `MODEL_PATH = "best_model.joblib"`

Aplikacja zwraca:
- predykcję klasy (WYSOKI / NIE_WYSOKI),
- prawdopodobieństwo klasy HIGH (jeśli dostępne `predict_proba`),
- poziom ryzyka na podstawie p(HIGH) oraz progów ryzyka.

W aplikacji ustawiono próg decyzyjny:
- `THRESHOLD = 0.40` (jeżeli `p(HIGH) >= 0.40` → wynik HIGH).


## Wersjonowanie danych i modelu (DVC)
W projekcie wykorzystano DVC do wersjonowania danych i modelu. W repozytorium znajdują się pliki `.dvc` śledzące artefakty:
- `prawidowy_excel.xlsx.dvc`
- `best_model.joblib.dvc`

## Struktura repozytorium (kluczowe pliki)
- `train.py` - trening + strojenie + zapis modelu
- `kalkulator.py` - wersja konsolowa (CLI) kalkulatora: uruchamiana z terminala, zadaje pytania przez `input()`, wykonuje predykcję na podstawie wczytanego modelu
- `app.py` - aplikacja Streamlit (interfejs + predykcja)
- `utils.py` - funkcje pomocnicze
- `tests/` - testy jednostkowe
- `requirements.txt` - zależności


Link do aplikacji: https://stress-app.streamlit.app/
