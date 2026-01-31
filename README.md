Projekt polega na stworzeniu modelu uczenia maszynowego, który prognozuje ryzyko wystąpienia wysokiego poziomu stresu na podstawie odpowiedzi udzielonych w ankiecie dotyczącej stylu życia.
Aplikacja została zaimplementowana w formie interaktywnej aplikacji Streamlit, umożliwiającej użytkownikowi szybkie uzyskanie predykcji.

Cel projektu: analiza danych ankietowych dotyczących stylu życia, zbudowanie modelu klasyfikacyjnego (WYSOKI / NIE_WYSOKI stres), optymalizacja modelu pod kątem wykrywania wysokiego stresu, stworzenie aplikacji umożliwiającej łatwe korzystanie z modelu.

Dane zebrane za pomocą ankiety Google Forms (ok. 100 osób), odpowiedzi zapisane w pliku Excel, pytania dotyczyły m.in.: snu, aktywności fizycznej, spożycia kawy i alkoholu, palenia papierosów, aktywności odstresowujących, subiektywnej oceny poziomu stresu.

Aby stworzyć model przetestowano: regresję logistyczną oraz Extra Trees Classifier.
Ostatecznie wybrano Extra Trees Classifier, który uzyskał lepsze wyniki dla klasy „WYSOKI”. Model trenowano z użyciem: podziału danych 65% / 35% (train / test), walidacji krzyżowej, strojenia hiperparametrów (RandomizedSearchCV).

Model nie stanowi diagnozy medycznej – jego celem jest wyłącznie informacyjna ocena ryzyka.

Link do aplikacji: https://stress-app.streamlit.app/
