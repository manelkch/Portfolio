
def article_method():
    import streamlit as st
    import os
    import numpy as np
    import wfdb
    import json
    import matplotlib.pyplot as plt
    from tensorflow.keras.models import load_model  

    BASE_DIR = os.path.dirname(__file__)   # where detection_methods.py lives
    MODEL_DIR = os.path.join(BASE_DIR, "model")
    DATA_DIR = os.path.join(BASE_DIR, "data")

    MODEL_PATH = os.path.join(MODEL_DIR, "shallow_cnn.h5")
    HISTORY_PATH = os.path.join(MODEL_DIR, "training_history.json")
    METRICS_PATH = os.path.join(MODEL_DIR, "final_metrics.json")
    
    WINDOW_SIZE = 200
    CHANNELS = {'MLII': 0, 'V5': 1}

    @st.cache_resource
    def load_trained_model():
        model = load_model(MODEL_PATH)
        return model

    @st.cache_resource
    def load_training_history():
        with open(HISTORY_PATH, 'r') as f:
            history = json.load(f)
        return history

    @st.cache_resource
    def load_final_metrics():
        with open(METRICS_PATH, 'r') as f:
            return json.load(f)

    def extract_beats(record_path, channel_index):
        record = wfdb.rdrecord(record_path)
        annotation = wfdb.rdann(record_path, 'atr')
        ecg_signal = record.p_signal[:, channel_index]
        beats, positions = [], []

        for i, sample in enumerate(annotation.sample):
            label = annotation.symbol[i]
            if label not in ['N', 'L', 'R', 'A', 'V']:
                continue
            start = sample - WINDOW_SIZE // 2
            end = sample + WINDOW_SIZE // 2
            if start >= 0 and end < len(ecg_signal):
                beat = ecg_signal[start:end]
                beats.append(beat)
                positions.append(sample)

        beats = np.array(beats)[..., np.newaxis]
        return beats, positions, ecg_signal, annotation.symbol

    def show_training_info():
        with st.container():
            st.subheader("Training Information")

            metrics = load_final_metrics()
            st.markdown(f"**Final Test Accuracy:** `{metrics['accuracy']:.4f}`")
            st.markdown(f"**Final Test Loss:** `{metrics['loss']:.4f}`")

            history = load_training_history()
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(history['loss'], label='Training Loss')
            ax.plot(history['val_loss'], label='Validation Loss')
            ax.set_title("Training & Validation Loss")
            ax.set_xlabel("Epoch")
            ax.set_ylabel("Loss")
            ax.legend()
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")
            st.pyplot(fig)

            st.markdown("### CNN Model Summary")
            st.markdown("""
            - **Input**: 1D ECG segment (200 samples)
            - **Layer 1**: `Conv1D(32 filters, kernel_size=5, ReLU)`
            - **Layer 2**: `MaxPooling1D(pool_size=2)`
            - **Layer 3**: `Dropout(0.2)`
            - **Layer 4**: `Flatten()`
            - **Layer 5**: `Dense(64, ReLU)`
            - **Output**: `Dense(1, Sigmoid)`
            """)

    def main():
        show_training_info()

        with st.sidebar:
            st.header("Signal Selection")
            patients = sorted([f[:-4] for f in os.listdir(DATA_DIR) if f.endswith('.dat')])
            selected_patient = st.selectbox("Select a patient record", patients)
            selected_channel = st.selectbox("Select Channel", CHANNELS.keys())

        if selected_patient:
            channel_index = CHANNELS[selected_channel]
            record_path = os.path.join(DATA_DIR, selected_patient)
            st.markdown(f"""
            <div style="background-color:#f7f7f9;padding:20px 30px;border-radius:12px;margin-bottom:20px">
                <strong>Patient:</strong> {selected_patient} &nbsp;&nbsp; | &nbsp;&nbsp; <strong>Channel:</strong> {selected_channel}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("#### Automated Detection")
            model = load_trained_model()

            beats, positions, full_signal, labels = extract_beats(record_path, channel_index)
            predictions = model.predict(beats).flatten()
            binary_preds = (predictions >= 0.5).astype(int)

            fig, ax = plt.subplots(figsize=(15, 4))
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")
            ax.plot(full_signal, label="ECG Signal", alpha=0.6)

            # Predictions overlay
            for pos, pred in zip(positions, binary_preds):
                color = 'red' if pred == 1 else 'green'
                ax.axvline(pos, color=color, linestyle='--', alpha=0.5)

            # Ground truth abnormal beats
            for pos, label in zip(positions, labels):
                if label in ['L', 'R', 'A', 'V']:
                    ax.axvline(pos, color='orange', linestyle=':', linewidth=1.5, alpha=0.6)

            ax.set_title("Detected Beats with Ground Truth Overlay")
            ax.set_xlabel("Sample")
            ax.set_ylabel("Amplitude")
            st.pyplot(fig)

            # Beat statistics
            true_anormal = sum(1 for l in labels if l in ['L', 'R', 'A', 'V'])
            st.success(f"""
            - Total beats analysed: **{len(binary_preds)}**
            - Anomalies detected by model: **{sum(binary_preds)}**
            - True abnormal beats (from annotation): **{true_anormal}**
            """)

    main()



def autoencoder():
    import streamlit as st
    import os
    import numpy as np
    import wfdb
    import pickle
    import json
    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_squared_error
    from tensorflow.keras.models import load_model
    from ecg.preprocessing_methods import median_bandpass_filter

    DATA_DIR = 'ecg/data'
    MODEL_PATH = 'ecg/model/ae_model.keras'
    SCALER_PATH = 'ecg/model/ae_scaler.pkl'
    THRESHOLD_PATH = 'ecg/model/ae_threshold.json'
    WINDOW_SIZE = 200
    CHANNELS = {'MLII': 0, 'V5': 1}

    @st.cache_resource
    def load_components():
        model = load_model(MODEL_PATH)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        with open(THRESHOLD_PATH, 'r') as f:
            threshold = json.load(f)['threshold']
        return model, scaler, threshold

    def extract_beats(record_path, channel_index):
        record = wfdb.rdrecord(record_path)
        annotation = wfdb.rdann(record_path, 'atr')
        raw_signal = record.p_signal[:, channel_index]
        ecg_signal = median_bandpass_filter(raw_signal)

        beats, positions, labels = [], [], []
        for i, sample in enumerate(annotation.sample):
            label = annotation.symbol[i]
            start = sample - WINDOW_SIZE // 2
            end = sample + WINDOW_SIZE // 2
            if start >= 0 and end < len(ecg_signal):
                beat = ecg_signal[start:end]
                beats.append(beat)
                positions.append(sample)
                labels.append(label)

        return np.array(beats), np.array(positions), ecg_signal, labels

    def show_model_summary():
        st.subheader("Autoencoder Model Summary")
        st.markdown("""
        - **Input**: `200` samples (1D ECG beat)
        - **Encoder**:
            - Dense(128) + ReLU
            - Dense(64)  + ReLU
        - **Decoder**:
            - Dense(128) + ReLU
            - Dense(200) + Linear
        - **Loss**: Mean Squared Error (MSE)
        - **Optimizer**: Adam (lr = 0.001)
        - **Anomaly threshold**: based on 95th percentile
        """)

    def plot_ecg_with_anomalies(signal, positions, anomalies, labels):
        fig, ax = plt.subplots(figsize=(15, 4))
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        ax.plot(signal, label='ECG', alpha=0.6)
        for pos, is_anomaly in zip(positions, anomalies):
            color = 'red' if is_anomaly else 'green'
            ax.axvline(pos, color=color, linestyle='--', alpha=0.4)
        for pos, label in zip(positions, labels):
            if label in ['L', 'R', 'A', 'V']:
                ax.axvline(pos, color='orange', linestyle=':', linewidth=1.5, alpha=0.6)
        ax.set_title("ECG with anomaly detection (red = model, orange = ground truth)")
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        st.pyplot(fig)

    def plot_reconstruction_error(errors, threshold):
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        ax.plot(errors, label="Reconstruction error")
        ax.axhline(threshold, color='red', linestyle='--', label=f'Threshold = {threshold:.5f}')
        ax.set_title("Reconstruction error per beat")
        ax.set_xlabel("Beat")
        ax.set_ylabel("MSE")
        ax.legend()
        st.pyplot(fig)

    def plot_reconstruction(beat, reconstructed, index, is_anomaly):
        fig, ax = plt.subplots()
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        ax.plot(beat, label='Original', alpha=0.7)
        ax.plot(reconstructed, label='Reconstructed', alpha=0.7)
        title = f"Beat {index} — {'Anomaly' if is_anomaly else 'Normal'}"
        ax.set_title(title)
        ax.legend()
        st.pyplot(fig)

    def main():
        st.title("Unsupervised Arrhythmia Detection using Autoencoder")

        show_model_summary()
        st.write(st.session_state.get('chosen_filter', ''))
        model, scaler, threshold = load_components()

        with st.sidebar:
            st.header("Signal Selection")
            patients = sorted([f[:-4] for f in os.listdir(DATA_DIR) if f.endswith('.dat')])
            selected = st.selectbox("Choose a patient record", patients)
            channel = st.selectbox("Select Channel", CHANNELS.keys())

        if selected:
            channel_index = CHANNELS[channel]
            record_path = os.path.join(DATA_DIR, selected)
            beats, positions, full_signal, labels = extract_beats(record_path, channel_index)

            beats_scaled = scaler.transform(beats)
            reconstructed = model.predict(beats_scaled)
            errors = np.mean((beats_scaled - reconstructed)**2, axis=1)
            anomalies = errors > threshold


            plot_ecg_with_anomalies(full_signal, positions, anomalies, labels)
            plot_reconstruction_error(errors, threshold)

            true_abnormal = sum(1 for l in labels if l in ['L', 'R', 'A', 'V'])

            st.success(f"""
            - Total beats analysed: **{len(beats)}**
            - Anomalies detected by model: **{np.sum(anomalies)}**
            - True abnormal beats (from annotation): **{true_abnormal}**
            """)

            st.subheader("Detailed analysis of a beat")
            idx = st.slider("Choose a beat index", 0, len(beats)-1, 0)
            plot_reconstruction(beats[idx], scaler.inverse_transform([reconstructed[idx]])[0], idx, anomalies[idx])

    main()



def isolation_forest():
    import streamlit as st
    import os
    import numpy as np
    import wfdb
    import pickle
    import matplotlib.pyplot as plt

    DATA_DIR = 'ecg/data'
    MODEL_PATH = 'ecg/model/if_model.pkl'
    SCALER_PATH = 'ecg/model/if_scaler.pkl'
    WINDOW_SIZE = 200
    CHANNELS = {'MLII': 0, 'V5': 1}

    @st.cache_resource
    def load_if_model():
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        return model, scaler

    def extract_beats(record_path, channel_index):
        record = wfdb.rdrecord(record_path)
        annotation = wfdb.rdann(record_path, 'atr')
        signal = record.p_signal[:, channel_index]
        beats, positions, labels = [], [], []
        for i, pos in enumerate(annotation.sample):
            label = annotation.symbol[i]
            start = pos - WINDOW_SIZE // 2
            end = pos + WINDOW_SIZE // 2
            if start >= 0 and end < len(signal):
                beat = signal[start:end]
                beats.append(beat)
                positions.append(pos)
                labels.append(label)
        return np.array(beats), np.array(positions), signal, labels

    def plot_ecg_with_anomalies(signal, positions, anomalies, labels):
        fig, ax = plt.subplots(figsize=(12, 3))
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        ax.plot(signal, label='ECG', alpha=0.6)
        for pos, is_anomaly in zip(positions, anomalies):
            color = 'red' if is_anomaly else 'green'
            ax.axvline(pos, color=color, linestyle='--', alpha=0.4)
        for pos, label in zip(positions, labels):
            if label in ['L', 'R', 'A', 'V']:
                ax.axvline(pos, color='orange', linestyle=':', linewidth=1.5, alpha=0.6)
        ax.set_title("ECG with anomaly detection (red = model, orange = ground truth)")
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        st.pyplot(fig)

    def show_model_summary():
        with st.container():
            st.subheader("Isolation Forest – Model Summary")
            st.markdown("""
            - **Method**: Unsupervised anomaly detection  
            - **Algorithm**: `IsolationForest` from `scikit-learn`  
            - **Contamination rate**: 5% (expected proportion of anomalies)  
            - **Input**: ECG beats (200 time points each)  
            - **Output**:  
                - Anomaly score ∈ [−1, 1]  
                - Binary prediction:  
                    - `1` = Normal  
                    - `-1` = Anomaly
            """)

    def plot_anomaly_scores(scores):
        fig, ax = plt.subplots(figsize=(6, 3))
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")
        ax.hist(scores, bins=50, alpha=0.7)
        ax.set_title("Anomaly Score Distribution")
        ax.set_xlabel("Score (lower = more anomalous)")
        ax.set_ylabel("Number of beats")
        st.pyplot(fig)

    def main():
        st.title("ECG Anomaly Detection using Isolation Forest")

        show_model_summary()
        model, scaler = load_if_model()

        with st.sidebar:
            st.header("Signal Selection")
            patients = sorted([f[:-4] for f in os.listdir(DATA_DIR) if f.endswith('.dat')])
            selected = st.selectbox("Choose a patient", patients)
            channel = st.selectbox("Select Channel", CHANNELS.keys())

        if selected:
            channel_index = CHANNELS[channel]
            path = os.path.join(DATA_DIR, selected)
            beats, positions, full_signal, labels = extract_beats(path, channel_index)
            X_scaled = scaler.transform(beats)

            st.info("Predicting anomalies using Isolation Forest...")
            scores = model.decision_function(X_scaled)
            preds = model.predict(X_scaled)
            is_anomaly = preds == -1

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div style="background-color:#f8f9fa;padding:15px 20px;border-radius:12px;margin-bottom:10px">
                    <strong>Total beats analysed:</strong> {0}<br>
                    <strong>Detected anomalies:</strong> {1}
                </div>
                """.format(len(beats), int(np.sum(is_anomaly))), unsafe_allow_html=True)
            with col2:
                true_abnormal = sum(1 for l in labels if l in ['L', 'R', 'A', 'V'])
                st.markdown("""
                <div style="background-color:#f8f9fa;padding:15px 20px;border-radius:12px;margin-bottom:10px">
                    <strong>Ground Truth Abnormal Beats:</strong> {0}
                </div>
                """.format(true_abnormal), unsafe_allow_html=True)

            #plot_anomaly_scores(scores)
            plot_ecg_with_anomalies(full_signal, positions, is_anomaly, labels)

            #st.subheader("Detailed Beat Analysis")
            #idx = st.slider("Select a beat index", 0, len(beats) - 1, 0)
            #fig, ax = plt.subplots(figsize=(6, 3))
            #fig.patch.set_alpha(0)
            #ax.set_facecolor("none")
            #ax.plot(beats[idx], label='Original beat')
            #ax.set_title(f"Beat {idx} — {'Anomaly' if is_anomaly[idx] else 'Normal'}")
            #ax.legend()
            #st.pyplot(fig)

    main()
