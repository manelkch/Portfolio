import pandas as pd



def drop_col(df):
    df = df.drop(['SIRET', 'Numero_inspection', 'Agrement', 'ods_type_activite'], axis=1)
    return df


def supp_nan(df):
    for col in df.columns:
        df.dropna(subset=[col], inplace=True)
    return df

def change_types(df):
    df['Date_inspection'] = pd.to_datetime(df['Date_inspection'], utc=True).dt.tz_localize(None).dt.date

    for col in df.columns:
        if col == 'Code_postal' or col == 'reg_code' or col == 'APP_Code_synthese_eval_sanit':
            df[col] = df[col].astype(int)
        else:
            if col != 'Date_inspection' and col != 'geores':
                df[col] = df[col].astype(str)
    return df


def data_preprocessing(df):
    df = drop_col(df) 
    df = supp_nan(df)
    df = change_types(df)

    return df

