import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def wczytaj_dane(sciezka_csv):

    # Wczytuje dane z pliku CSV

    return pd.read_csv(sciezka_csv)

def klasyfikacja_wektorow(dane):

    # Funkcjado do przeprowadzenia klasyfikacji wektorów cech przy użyciu SVM i wyświetlenia wyników


    X = dane.drop('kategoria', axis=1)
    y = dane['kategoria']

    # zbiór treningowy i testowy (80% trening, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    klasyfikator = SVC(kernel='linear')


    klasyfikator.fit(X_train, y_train)


    y_pred = klasyfikator.predict(X_test)


    dokladnosc = accuracy_score(y_test, y_pred)
    print(f'Dokładność klasyfikatora SVM: {dokladnosc:.2f}')


    print('\nRaport klasyfikacji:')
    print(classification_report(y_test, y_pred))


    macierz_pomylek = confusion_matrix(y_test, y_pred)


    plt.figure(figsize=(8, 6))
    sns.heatmap(macierz_pomylek, annot=True, fmt='d', cmap='Blues', xticklabels=klasyfikator.classes_, yticklabels=klasyfikator.classes_)
    plt.xlabel('Etykiety przewidywane')
    plt.ylabel('Etykiety rzeczywiste')
    plt.title('Macierz pomyłek dla klasyfikatora SVM')
    plt.show()

if __name__ == "__main__":
    sciezka_csv = "cechy.csv"


    dane = wczytaj_dane(sciezka_csv)

    klasyfikacja_wektorow(dane)