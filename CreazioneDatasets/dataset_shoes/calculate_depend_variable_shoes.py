"""
 #   Column                Non-Null Count  Dtype
---  ------                --------------  -----
 0   time                  5026 non-null   object x
 1   Meteo                 5026 non-null   object v
 2   TemperaturaPercepita  5026 non-null   float64 v
 3   StagionePrevisione    5026 non-null   object v
 4   Mese                  5026 non-null   object v
 5   Tipo                  5026 non-null   object
 6   Scivoloso             5026 non-null   bool v
 7   Impermeabile          5026 non-null   bool v
 8   Colore                5026 non-null   object v
 9   Stagione              5026 non-null   object v


    Stivaletto alla caviglia    1525
    Ballerine                    858
    Sneakers                     770
    Scarpa da ginnastica         701
    Scarpa classica              569
    Scarpe con tacchi            308
    Scarpe aperte                277
    Anfibi                        91
    Stivali                       21

 """
import pandas as pd
import utils

ranges = [
    {  # temperatura > 30°
        'inverno': 0,
        'autunno': 1,
        'primavera': 2,
        'estate': 5,
        'primavera_estate': 4,
        'autunno_inverno': 1,
        'all': 3
    },
    {  # 25° <= temperatura < 30°
        'inverno': 0,
        'autunno': 1,
        'primavera': 3,
        'estate': 5,
        'primavera_estate': 4,
        'autunno_inverno': 1,
        'all': 3
    },
    {  # 20° <= temperatura < 25°
        'inverno': 1,
        'autunno': 2,
        'primavera': 5,
        'estate': 4,
        'primavera_estate': 4,
        'autunno_inverno': 1,
        'all': 3
    },
    {  # 15° <= temperatura < 20°
        'inverno': 4,
        'autunno': 5,
        'primavera': 4,
        'estate': 3,
        'primavera_estate': 3,
        'autunno_inverno': 4,
        'all': 3
    },
    {  # 10 <= temperatura < 15°
        'inverno': 5,
        'autunno': 5,
        'primavera': 3,
        'estate': 1,
        'primavera_estate': 2,
        'autunno_inverno': 4,
        'all': 3
    },
    {  # 5 <= temperatura < 10°
        'inverno': 5,
        'autunno': 4,
        'primavera': 1,
        'estate': 0,
        'primavera_estate': 0,
        'autunno_inverno': 4,
        'all': 3
    },
    {  # temperatura < 5°
        'inverno': 5,
        'autunno': 3,
        'primavera': 1,
        'estate': 0,
        'primavera_estate': 0,
        'autunno_inverno': 3,
        'all': 3
    }
]

stagionalita = [
    {  # stagione inverno
        'inverno': 6,
        'autunno': 4,
        'primavera': 2,
        'estate': 0,
        'primavera_estate': 1,
        'autunno_inverno': 5,
        'all': 3
    },
    {  # stagione primavera
        'primavera': 6,
        'estate': 4,
        'autunno': 2,
        'inverno': 0,
        'primavera_estate': 5,
        'autunno_inverno': 1,
        'all': 3
    },
    {  # stagione estate
        'estate': 6,
        'autunno': 2,
        'inverno': 0,
        'primavera': 4,
        'primavera_estate': 5,
        'autunno_inverno': 1,
        'all': 3
    },
    {  # stagione autunno
        'autunno': 6,
        'inverno': 4,
        'primavera': 2,
        'estate': 0,
        'primavera_estate': 1,
        'autunno_inverno': 5,
        'all': 3
    }
]

valutazione_tipo={
    'pioggia': {
        'Stivaletto alla caviglia': 10,
        'Scarpa da ginnastica': 6,
        'Scarpa classica': 7,
        'Scarpe con tacchi': 4,
        'Scarpe aperte': 0,
        'Anfibi': 10,
        'Stivali': 10
    },
    'soleggiato': {
        'Stivaletto alla caviglia': 3,
        'Scarpa da ginnastica': 8,
        'Scarpa classica': 7,
        'Scarpe con tacchi': 7,
        'Scarpe aperte': 9,
        'Anfibi': 3,
        'Stivali': 3
    },

    'nuvoloso': {
        'Stivaletto alla caviglia': 4,
        'Scarpa da ginnastica': 8,
        'Scarpa classica': 8,
        'Scarpe con tacchi': 5,
        'Scarpe aperte': 2,
        'Anfibi': 4,
        'Stivali': 4
    },

    'neve': {
        'Stivaletto alla caviglia': 8,
        'Scarpa da ginnastica': 5,
        'Scarpa classica': 6,
        'Scarpe con tacchi': 1,
        'Scarpe aperte': 0,
        'Anfibi': 9,
        'Stivali': 10
    }
}


def evaluate_tipo(meteo, tipo):
    return valutazione_tipo[meteo][tipo]


def evaluate_stagione(stagione_capo, stagione_prev):
    i = utils.calculate_ranges_stagione(stagione_prev)
    return stagionalita[i][stagione_capo]


def evaluate_temperature(stagione_capo, temperatura_percepita):
    i = utils.calculate_ranges_temperatura(temperatura_percepita)
    return ranges[i][stagione_capo]


def evaluate_pioggia(scivoloso, impermeabile):
    if scivoloso and impermeabile:
        return 5
    elif scivoloso :
        return 3
    elif impermeabile:
        return 4
    else:
        return 0


df = pd.read_csv('../newCsv_all_clothes/shoes_meteo_dataset.csv')

df.loc[:, 'Punteggio'] = 0

for x in df.index:
    p = 0
    p += evaluate_temperature(df.loc[x, "Stagione"], df.loc[x, "TemperaturaPercepita"])
    p += evaluate_stagione(df.loc[x, "Stagione"], df.loc[x, "StagionePrevisione"])
    p += utils.evaluate_colore(df.loc[x, "Meteo"], df.loc[x, "Colore"], df.loc[x, "TemperaturaPercepita"])
    p += evaluate_tipo(df.loc[x, "Meteo"], df.loc[x, "Tipo"])
    if df.loc[x, 'Meteo'] == 'pioggia' or df.loc[x, 'Meteo'] == 'neve':
        p += evaluate_pioggia(df.loc[x, 'Scivoloso'], df.loc[x, 'Impermeabile'])

    df.loc[x, 'Punteggio'] = p
print(df.info())

df.to_csv('../newCsv_all_clothes/shoes_meteo_dataset_labeled.csv', index=False)
#TODO Aggiungere commenti