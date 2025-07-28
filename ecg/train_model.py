import os
import numpy as np
import wfdb
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dense, Dropout, Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical
import json

HISTORY_PATH = 'model/training_history.json'
METRICS_PATH = 'model/final_metrics.json'


DATA_DIR = 'data'
MODEL_PATH = 'model/shallow_cnn.pkl'
WINDOW_SIZE = 200  # number of samples per beat

def load_ecg_data():
    signals, labels = [], []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.dat'):
            record_name = filename[:-4]
            record_path = os.path.join(DATA_DIR, record_name)

            record = wfdb.rdrecord(record_path)
            annotation = wfdb.rdann(record_path, 'atr')

            ecg_signal = record.p_signal[:, 0]  # Use channel 0

            for i, sample in enumerate(annotation.sample):
                label = annotation.symbol[i]
                if label not in ['N', 'L', 'R', 'A', 'V']:  # N=normal; others abnormal
                    continue

                start = sample - WINDOW_SIZE // 2
                end = sample + WINDOW_SIZE // 2

                if start >= 0 and end < len(ecg_signal):
                    beat = ecg_signal[start:end]
                    signals.append(beat)
                    labels.append(0 if label == 'N' else 1)

    X = np.array(signals)
    y = np.array(labels)
    X = X[..., np.newaxis]  # reshape for Conv1D

    return X, y

def build_model(input_shape):
    model = Sequential([
        Conv1D(32, kernel_size=5, activation='relu', input_shape=input_shape),
        MaxPooling1D(pool_size=2),
        Dropout(0.2),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(loss='binary_crossentropy', optimizer=SGD(learning_rate=0.01), metrics=['accuracy'])
    return model

def main():
    #print("Loading ECG data...")
    X, y = load_ecg_data()
    #print(f"Loaded {len(X)} samples")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

    #print("Building model...")
    model = build_model(X.shape[1:])

    #print("Training model...")
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=64)

    #print("Evaluating model...")
    loss, acc = model.evaluate(X_test, y_test)
    #print(f"Test accuracy: {acc:.4f}")

    #print(f"Saving model to {MODEL_PATH}...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    # Save training history
    with open(HISTORY_PATH, 'w') as f:
        json.dump(history.history, f)

    # Save final test metrics
    metrics = {'loss': loss, 'accuracy': acc}
    with open(METRICS_PATH, 'w') as f:
        json.dump(metrics, f)


if __name__ == '__main__':
    main()
