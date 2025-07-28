import os
import numpy as np
import wfdb
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest

DATA_DIR = 'data'
IF_MODEL_PATH = 'model/if_model.pkl'
IF_SCALER_PATH = 'model/if_scaler.pkl'
WINDOW_SIZE = 200

def load_normal_beats():
    beats = []
    for file in os.listdir(DATA_DIR):
        if not file.endswith('.dat'):
            continue
        record_name = file[:-4]
        record_path = os.path.join(DATA_DIR, record_name)
        record = wfdb.rdrecord(record_path)
        annotation = wfdb.rdann(record_path, 'atr')
        signal = record.p_signal[:, 0]
        for i, pos in enumerate(annotation.sample):
            label = annotation.symbol[i]
            if label != 'N':
                continue
            start = pos - WINDOW_SIZE // 2
            end = pos + WINDOW_SIZE // 2
            if start < 0 or end >= len(signal):
                continue
            beats.append(signal[start:end])
    return np.array(beats)

def main():
    #print("Chargement des battements normaux")
    beats = load_normal_beats()
    #print(f"{len(beats)} battements trouvés")

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(beats)

    #print("Entraînement de l’Isolation Forest")
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X_scaled)

    os.makedirs('model', exist_ok=True)
    with open(IF_MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(IF_SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    #print("Modèle Isolation Forest et scaler sauvegardés.")

if __name__ == '__main__':
    main()
