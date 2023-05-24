from pandas import read_csv, DataFrame, set_option

# Imposta il formato di visualizzazione dei numeri decimali
set_option('display.float_format', '{:,.2f}'.format)


def compara_casi(dataset, continente1, continente2):
    # Filtra i dati per il continente1 e il continente2
    dati_continente1 = dataset[dataset['continent'] == continente1]['new_cases']
    dati_continente2 = dataset[dataset['continent'] == continente2]['new_cases']

    statistiche_continente1 = dati_continente1.describe()
    statistiche_continente2 = dati_continente2.describe()

    # Calcola il numero totale di casi nel mondo
    casi_totali_mondo = dataset['new_cases'].sum()

    # Calcola la percentuale di casi rispetto al totale mondiale
    percentuale_continente1 = dati_continente1.sum() / casi_totali_mondo * 100
    percentuale_continente2 = dati_continente2.sum() / casi_totali_mondo * 100

    # Crea un DataFrame con le statistiche dei casi
    statstiche = DataFrame({
        continente1: {"minimo": statistiche_continente1['min'], "massimo": statistiche_continente1['max'], "media": statistiche_continente1['mean']},
        continente2: {"minimo": statistiche_continente2['min'], "massimo": statistiche_continente2['max'], "media": statistiche_continente2['mean']}
    })
    # Aggiungi la riga per la percentuale di casi rispetto al mondo
    statstiche.loc['Percentuale di casi totali rispetto al mondo'] = [percentuale_continente1, percentuale_continente2]
    return statstiche


def compara_vaccinazioni(dataset, continente1, continente2):
    # Filtra i dati per il continente1 e il continente2
    dati_continente1 = dataset[dataset['continent'] == continente1]['new_vaccinations']
    dati_continente2 = dataset[dataset['continent'] == continente2]['new_vaccinations']

    statistiche_continente1 = dati_continente1.describe()
    statistiche_continente2 = dati_continente2.describe()

    # Calcola il numero totale delle vaccinazioni nel mondo
    vaccini_totali_mondo = dataset['new_vaccinations'].sum()

    # Calcola la percentuale delle vaccinazioni rispetto al totale mondiale
    percentuale_continente1 = dati_continente1.sum() / vaccini_totali_mondo * 100
    percentuale_continente2 = dati_continente2.sum() / vaccini_totali_mondo * 100

    # Crea un DataFrame con le statistiche delle vaccinazioni
    statstiche = DataFrame({
        continente1: {"minimo": statistiche_continente1['min'], "massimo": statistiche_continente1['max'], "media": statistiche_continente1['mean']},
        continente2: {"minimo": statistiche_continente2['min'], "massimo": statistiche_continente2['max'], "media": statistiche_continente2['mean']}
    })
    # Aggiungi la riga per la percentuale delle vaccinazioni rispetto al mondo
    statstiche.loc['Percentuale di vaccinazioni totali rispetto al mondo'] = [percentuale_continente1, percentuale_continente2]
    return statstiche


# URL del dataset in formato CSV
dataset_url = "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
# Carica il dataset in un dataframe e specifica i tipi della colonna "test_units"
dtypes = {"tests_units": object}
dataframe = read_csv(dataset_url, dtype=dtypes)

# Stampa dimensione e intestazioni del dataset
print("Dimensione del dataset:", dataframe.shape)
print("Intestazioni:", dataframe.columns.values)

# Filtra solo le righe che hanno il valore del continente
continenti = dataframe.dropna(subset=['continent'])
# Raggruppa per continente e calcola la somma totale dei casi
casi_totali_continente = continenti.groupby('continent')['new_cases'].sum()
print("Casi totali per continente:")
print(casi_totali_continente)

# Calcola le statistiche tra Europa e America del Sud
comparazione_casi = compara_casi(dataframe, 'Europe', 'South America')
comparazione_vaccinazioni = compara_vaccinazioni(dataframe, 'Europe', 'South America')
# Aggiungi le comparazioni con l'oceania
comparazione_casi['Oceania'] = compara_casi(dataframe, 'Oceania', 'Europe').iloc[:, 0]
comparazione_vaccinazioni['Oceania'] = compara_vaccinazioni(dataframe, 'Oceania', 'Europe').iloc[:, 0]

# Stampa il riassunto delle informazioni raccolte
print()
print("Statistiche dei casi di COVID-19:")
print("Europa vs America del Sud vs Oceania:")
print(comparazione_casi.to_string(index_names=True))
print()

print("Statistiche sui vaccini per il COVID-19:")
print("Europa vs America del Sud vs Oceania:")
print(comparazione_vaccinazioni.to_string(index_names=True))
