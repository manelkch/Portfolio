import os
import numpy as np
import wfdb
import json
import pickle
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from preprocessing_methods import median_bandpass_filter

DATA_DIR = 'data'
MODEL_PATH = 'model/ae_model.keras'
SCALER_PATH = 'model/ae_scaler.pkl'
THRESHOLD_PATH = 'model/ae_threshold.json'
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
        raw_signal = record.p_signal[:, 0]

        filtered_signal = median_bandpass_filter(raw_signal)

        for i, pos in enumerate(annotation.sample):
            label = annotation.symbol[i]
            if label != 'N':
                continue
            start = pos - WINDOW_SIZE // 2
            end = pos + WINDOW_SIZE // 2
            if start < 0 or end >= len(filtered_signal):
                continue
            beat = filtered_signal[start:end]
            beats.append(beat)
    return np.array(beats)

def build_autoencoder(input_dim):
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(128, activation='relu')(input_layer)
    encoded = Dense(64, activation='relu')(encoded)
    decoded = Dense(128, activation='relu')(encoded)
    output_layer = Dense(input_dim, activation='linear')(decoded)
    autoencoder = Model(inputs=input_layer, outputs=output_layer)
    autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
    return autoencoder

def main():
    #print("Chargement des battements normaux...")
    beats = load_normal_beats()
    #print(f"{len(beats)} battements extraits")

    # Normalisation
    scaler = MinMaxScaler()
    beats_scaled = scaler.fit_transform(beats)

    # Split
    X_train, X_val = train_test_split(beats_scaled, test_size=0.1, random_state=42)

    #print("Construction du modèle autoencodeur...")
    autoencoder = build_autoencoder(WINDOW_SIZE)

    #print("Entraînement en cours...")
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    history = autoencoder.fit(
        X_train, X_train,
        validation_data=(X_val, X_val),
        epochs=50,
        batch_size=64,
        callbacks=[early_stop],
        verbose=1
    )


    #print("Calcul du seuil de reconstruction...")
    reconstructions = autoencoder.predict(X_train)
    reconstruction_errors = np.mean((X_train - reconstructions) ** 2, axis=1)
    threshold = float(np.percentile(reconstruction_errors, 95))  # 95e percentile

    #print(f"Seuil fixé à : {threshold:.6f}")

    os.makedirs('model', exist_ok=True)
    autoencoder.save(MODEL_PATH)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    with open(THRESHOLD_PATH, 'w') as f:
        json.dump({'threshold': threshold}, f)
    with open('model/ae_history.json', 'w') as f:
        json.dump(history.history, f)

    #print("Modèle, scaler et seuil sauvegardés.")

if __name__ == '__main__':
    main()
