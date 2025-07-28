import streamlit as st

def page_home_ecg():
    import streamlit as st
    from streamlit_option_menu import option_menu
    import numpy as np
    import wfdb

    import matplotlib.pyplot as plt
    import re

    # Define sections and their content
    sections = [
        "Objective",
        "Data Description",
        "Data Visualization",  
    ]

    # Sidebar: clickable list of sections
    with st.sidebar:
        st.title("Navigation")
        selected_section = option_menu(
            menu_title=None,
            options=sections,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "nav-link-selected": {"background-color": "#dde7e4", "color": "black",}
            }
        )
    
    

    if selected_section == "Objective":

        st.title("🫀 CardioSensAI - Automated arrhythmia detection")

        # Card 1 – The Challenge
        st.markdown("""
        <div style="background-color:#f0f4fa;padding:20px;border-radius:12px;margin-bottom:20px">
            <h3 style="color:#003366;"> The Challenge: Cardiovascular Disease and Arrhythmias</h3>
            <p>
            Cardiovascular diseases (<b>CVDs</b>) are the <b>leading cause of death worldwide</b>, causing over <b>30% of all deaths</b> according to the WHO.
            </p>
            <ul>
                <li><b>130+ million</b> people will suffer from CVDs by <b>2035</b></li>
                <li><b>Arrhythmias</b>, disrupting the heart rhythm, are a dangerous subset</li>
                <li>In the <b>US alone</b>, <b>6–12 million</b> people could be affected by <b>2050</b></li>
            </ul>
            <p>
            <b>Early detection</b> is crucial to prevent serious outcomes and reduce mortality.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card 2 – Limitations of manual ECG
        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:20px;border-radius:12px;margin-bottom:20px">
            <h3 style="color:#1f77b4;"> Limitations of Traditional ECG Interpretation</h3>
            <p>The <b>electrocardiogram (ECG)</b> is the most widely used tool for diagnosing arrhythmias, but:</p>
            <ul>
                <li>It requires <b>expertise</b> and training</li>
                <li>It is <b>time-consuming</b></li>
                <li>It suffers from <b>inter-reader variability</b></li>
            </ul>
            <p>This highlights the need for <b>automated and scalable solutions</b>.</p>
        </div>
        """, unsafe_allow_html=True)

        # Card 3 – Our Solution
        st.markdown("""
        <div style="background-color:#e8f3f8;padding:20px;border-radius:12px;margin-bottom:20px">
            <h3 style="color:#004c6d;"> Our AI-Powered Solution</h3>
            <p><b>CardioSenseAI</b> is an intelligent system that automates arrhythmia detection from ECG signals using machine learning.</p>
            <h4>What You Can Do With This App:</h4>
            <ul>
                <li>Load and inspect real ECG recordings</li>
                <li>Detect heartbeat anomalies automatically</li>
                <li>Compare the results of two models: <b>Autoencoder</b> and <b>Isolation Forest</b></li>
                <li>View model performance and architecture</li>
                <li>Understand how <b>AI transforms cardiac diagnostics</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Card 4 – Data source
        st.markdown("""
        <div style="background-color:#fff9e6;padding:20px;border-left:5px solid #f4a300;border-radius:12px;margin-bottom:20px">
            <h3 style="color:#b36b00;"> Data Source: MIT-BIH Arrhythmia Database</h3>
            <ul>
                <li>From MIT and Beth Israel Hospital</li>
                <li>Includes expert-annotated ECG recordings</li>
                <li>Widely used in arrhythmia detection research</li>
                <li>Used in CNN-based studies with up to <b>99.02% accuracy</b>  
                ([Ullah et al., 2020](https://doi.org/...))</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown("---")
        st.caption("Developed by Manel EL KOUCH, 2025 – EFREI Paris • Powered by Streamlit")


    if selected_section == "Data Description":
        st.title("Data Description")

        # Card – Dataset Introduction
        st.markdown("""
        <div style="background-color:#f0f4fa;padding:30px 40px;border-radius:12px;margin-bottom:25px">
            <h2 style="color:#003366;margin-top:0;"> MIT-BIH Arrhythmia Database</h2>
            <p style="font-size:16px;">
                The <strong>MIT-BIH Arrhythmia Database</strong> is a clinically annotated dataset that serves as a <strong>gold standard</strong> for developing and evaluating arrhythmia detection algorithms based on ECG signals.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card – Dataset Overview
        st.markdown("""
        <div style="background-color:#ffffff;border-left:6px solid #1f77b4;padding:30px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#1f77b4;"> Dataset Overview</h3>
            <ul style="font-size:16px;">
                <li><strong>Number of Records:</strong> 48 ECG recordings</li>
                <li><strong>Duration per Record:</strong> Approximately 30 minutes</li>
                <li><strong>Sampling Frequency:</strong> 360 Hz</li>
                <li><strong>Subjects:</strong> 47 individuals (aged 23 to 89)</li>
                <li><strong>Leads Used:</strong> Lead MLII + one modified chest lead V5</li>
                <li><strong>Annotations:</strong> Manual beat-by-beat labeling by cardiologists</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Card – Beat Categories
        st.markdown("""
        <div style="background-color:#eaf4ff;padding:30px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#004c6d;">🫀 Beat Categories</h3>
            <p style="font-size:16px;">Each heartbeat is labeled with a symbol representing its type:</p>
            <ul style="font-size:16px;">
                <li><code>N</code> —> Normal beat</li>
                <li><code>L</code> & <code> R</code> —> Left/Right bundle branch block</li>
                <li><code>A</code> —> Atrial premature beat</li>
                <li><code>V</code> —> Ventricular premature beat</li>
                <li>Other symbols exist but are ignored in this application</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Card – File Structure
        st.markdown("""
        <div style="background-color:#fff9e6;border-left:6px solid #f4a300;padding:30px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#b36b00;"> Files in Each ECG Record</h3>
            <p style="font-size:16px;">
                Each ECG record consists of <strong>3 files</strong> sharing the same base name:
            </p>
            <table style="width:100%;font-size:16px;border-collapse: collapse;margin-bottom:10px">
                <tr style="background-color:#f9f9f9;">
                    <th style="text-align:left;padding:8px;">File Extension</th>
                    <th style="text-align:left;padding:8px;">Description</th>
                </tr>
                <tr>
                    <td style="padding:8px;"><code>.dat</code></td>
                    <td style="padding:8px;">Raw ECG signal (binary format), typically 2-lead</td>
                </tr>
                <tr>
                    <td style="padding:8px;"><code>.hea</code></td>
                    <td style="padding:8px;">Header file (text) with metadata: sampling rate, channels, patient ID</td>
                </tr>
                <tr>
                    <td style="padding:8px;"><code>.atr</code></td>
                    <td style="padding:8px;">Annotation file: timestamped symbols and beat types</td>
                </tr>
            </table>
            <p style="font-size:16px;">
                <strong>Example:</strong> For patient record <code>100</code> There are :
                <br>→ <code>100.dat</code> + <code>100.hea</code> + <code>100.atr</code>
            </p>
            <p style="font-size:16px;">
                These files are processed using the <a href="https://github.com/MIT-LCP/wfdb-python" target="_blank">wfdb Python library</a>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card – Licensing & Dataset Access
        st.markdown("""
        <div style="background-color:#f0f0f0;padding:30px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#333;">📜 Licensing & Access</h3>
            <p style="font-size:16px;">
                The dataset is available via <strong>PhysioNet</strong> and is free to use under the 
                <strong>Open Data Commons Public Domain Dedication and License (PDDL)</strong>.
            </p>
            <p style="font-size:16px;">
                🔗 <a href="https://physionet.org/content/mitdb/1.0.0/" target="_blank">Access the MIT-BIH Database</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Card – Why this dataset?
        st.markdown("""
        <div style="background-color:#f7fbfc;padding:30px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#1b4965;"> Why This Dataset?</h3>
            <ul style="font-size:16px;">
                <li>High-quality annotations by cardiologists</li>
                <li>Clean and consistent ECG signals</li>
                <li>Trusted by the medical AI research community</li>
                <li>Supports both <strong>supervised</strong> and <strong>unsupervised</strong> learning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)



    if selected_section == "Data Visualization":

        st.title(" Data Visualization")

        ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
            121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
            220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

        channels = {'MLII': 0, 'V5': 1}

        # Sidebar controls
        with st.sidebar:
            st.header(" Patient Selection")
            patient = st.selectbox("Select Patient ID", ids)
            channel = st.selectbox("Select Channel", channels.keys())

        # Title card
        st.markdown(f"""
        <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#003366;margin-top:0;"> ECG Visualization – Patient {patient}, Channel {channel}</h3>
            <p style="font-size:16px;">Below is the ECG signal from the MIT-BIH record <strong>{patient}</strong>. Two plots are shown:</p>
            <ul style="font-size:16px;">
                <li>Full signal (first 10 seconds) across both leads</li>
                <li>Focused view on the selected channel: <strong>{channel}</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Load data
        record = wfdb.rdrecord(f'ecg/data/{patient}')
        annotation = wfdb.rdann(f"ecg/data/{patient}", 'atr')
        signal = record.p_signal
        fs = record.fs
        start = 0
        end = int(10 * fs)

        # Visualizations
        st.markdown("""
        <div style="background-color:#ffffff;padding:25px 40px;border-left:5px solid #1f77b4;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#1f77b4;"> First 10 Seconds – Both Channels (MLII & V5)</h4>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(signal[0:end])

        st.markdown(f"""
        <div style="background-color:#ffffff;padding:25px 40px;border-left:5px solid #ff7f0e;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#d65c00;"> First 10 Seconds – Channel {channel}</h4>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(signal[0:end, channels[channel]])

        # Patient metadata
        metadata_signal = {
            "Patient ID": patient,
            "Sampling Frequency (Hz)": record.fs,
            "Duration (s)": round(len(record.p_signal) / record.fs, 2),
            "Signal Channels": record.sig_name,
            "Number of Annotations": len(annotation.sample),
            "Recording Date": record.base_date.strftime('%Y-%m-%d') if record.base_date else "Unknown",
            "Recording Time": record.base_time.strftime('%H:%M:%S') if record.base_time else "Unknown"
        }

        st.markdown("""
        <div style="background-color:#e0f8ec;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#208060;"> Signal Metadata</h4>
        </div>
        """, unsafe_allow_html=True)
        for key, value in metadata_signal.items():
            st.markdown(f"**{key}:** {value}")

        # Extract extra metadata from header
        hea_path = f"ecg/data/{patient}.hea"
        with open(hea_path, 'r') as file:
            hea_lines = file.readlines()

        metadata = {
            "Age": None,
            "Sex": None,
            "Patient Code": None,
            "Patient Number": None,
            "Treatment Type": None,
            "Medications": [],
            "Comments": []
        }

        hash_lines = [line.strip("#").strip() for line in hea_lines if line.startswith("#")]

        if len(hash_lines) >= 1:
            parts = hash_lines[0].split()
            if len(parts) >= 5:
                metadata["Age"] = int(parts[0])
                metadata["Sex"] = parts[1]
                metadata["Patient Code"] = parts[2]
                metadata["Patient Number"] = parts[3]
                metadata["Treatment Type"] = parts[4]

        if len(hash_lines) >= 2:
            medications = [med.strip() for med in hash_lines[1].split(",")]
            metadata["Medications"] = medications

        if len(hash_lines) >= 3:
            metadata["Comments"] = hash_lines[2:]

        # Display additional metadata
        st.markdown("""
        <div style="background-color:#f9f9f9;padding:25px 40px;border-left:5px solid #888;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#444;"> Patient Header Information</h4>
        </div>
        """, unsafe_allow_html=True)
        for key, value in metadata.items():
            if isinstance(value, list):
                st.markdown(f"**{key}:**")
                for item in value:
                    st.markdown(f"- {item}")
            else:
                st.markdown(f"**{key}:** {value if value is not None else 'Not available'}")


def page_preprocessing():
    import streamlit as st
    import wfdb
    from streamlit_option_menu import option_menu
    import numpy as np
    import pywt
    import matplotlib.pyplot as plt
    import os
    
    from ecg.preprocessing_methods import median_filter1D, bandpass_filter, median_bandpass_filter, plot_ecg_with_rpeaks, extract_beats, min_max_normalize
    from scipy.ndimage import gaussian_filter1d
    import neurokit2 as nk
    import seaborn as sns
    import pandas as pd
    from collections import Counter

    #st.set_page_config(layout="wide")

    # Define sections and their content
    sections = [ 
        "Denoising",
        "Normalization",
        "R-Peak Detection",
        "Data Compression",
        "Exploratory Data Analysis"
    ]

    # Sidebar: clickable list of sections
    with st.sidebar:
        selected_section = option_menu(
            menu_title=None,
            options=sections,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "nav-link-selected": {"background-color": "#dde7e4", "color": "black",}
            }
        )

    if selected_section == "Denoising":
        st.session_state["chosen_filter"] = 'Median Filter'
        st.title("Data Denoising")

        # Patient & Channel Selection
        ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
            121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
            220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

        channels = {'MLII': 0, 'V5': 1}

        with st.sidebar:
            st.header("Filter Settings")
            patient = st.selectbox("Select Patient ID", ids)
            channel = st.selectbox("Select Channel", channels.keys())
            methods = [
                "Median Filter",
                "Bandpass Filter",
                "Median + Bandpass Filter",
                "Gaussian Filter"
            ]
            method = st.selectbox("Denoising Method", methods)

        # Intro card
        st.markdown(f"""
        <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#003366;margin-top:0;">ECG Signal for Patient {patient}, Channel {channel}</h3>
            <p style="font-size:16px;">Below is the original ECG signal extracted from the MIT-BIH database. A 10-second window is used for visualization.</p>
        </div>
        """, unsafe_allow_html=True)

        # Load and display raw ECG signal
        record = wfdb.rdrecord(f'ecg/data/{patient}')
        signal = record.p_signal
        fs = record.fs
        end = int(10 * fs)

        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#1f77b4;">Original ECG Signal (10 seconds)</h4>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(signal[:end, channels[channel]])

        # Denoising Method Section
        st.markdown(f"""
        <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#004c6d;">Denoising Method Selected: {method}</h4>
            <p style="font-size:16px;">The chart below shows the denoised ECG signal using the selected method. You may try different filters and confirm your choice.</p>
        </div>
        """, unsafe_allow_html=True)

        # Apply selected filter
        denoised = None
        if method == "Median Filter":
            denoised = median_filter1D(signal[:end, channels[channel]], 3)
        elif method == "Bandpass Filter":
            denoised = bandpass_filter(signal[:end, channels[channel]])
        elif method == "Median + Bandpass Filter":
            denoised = median_bandpass_filter(signal[:end, channels[channel]])
        elif method == "Gaussian Filter":
            denoised = gaussian_filter1d(signal[:end, channels[channel]], sigma=2)

        # Display filtered signal
        if denoised is not None:
            st.markdown("""
            <div style="background-color:#ffffff;border-left:5px solid #d62728;padding:25px 40px;border-radius:12px;margin-bottom:25px">
                <h4 style="color:#a32020;">Filtered ECG Signal</h4>
            </div>
            """, unsafe_allow_html=True)
            st.line_chart(denoised)

            if st.button("Confirm This Denoising Method"):
                st.session_state["chosen_filter"] = method
                st.success(f"{method} has been selected as your denoising method.")


    if selected_section == "Normalization":
        st.title("Signal Normalization")

        # Sélection patient / canal
        ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
            121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
            220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

        channels = {'MLII': 0, 'V5': 1}

        with st.sidebar:
            st.header("Signal Selection")
            patient = st.selectbox("Select Patient ID", ids)
            channel = st.selectbox("Select Channel", channels.keys())

        # Info carte
        st.markdown(f"""
        <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#003366;margin-top:0;">ECG Signal of Patient {patient} - Channel {channel}</h3>
            <p style="font-size:16px;">
                The following visualization compares the filtered ECG signal (using your previously chosen method)
                with its normalized version using <strong>Min-Max scaling</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Chargement des données
        record = wfdb.rdrecord(f'ecg/data/{patient}')
        signal = record.p_signal
        fs = record.fs
        end = int(10 * fs)

        # Affichage de la méthode de filtrage choisie
        st.markdown(f"""
        <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#004c6d;">Filtering Method Used</h4>
            <p style="font-size:16px;">{st.session_state.get('chosen_filter', 'Median Filter')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Application du filtre (ici median + bandpass car fixe)
        clean_signal = median_bandpass_filter(signal[:end, channels[channel]])
        normalized_signal = min_max_normalize(clean_signal)

        # Carte 1 – Signal filtré
        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#1f77b4;">Filtered ECG Signal (10 seconds)</h4>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(clean_signal)

        # Carte 2 – Signal normalisé
        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #ffaa00;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#cc7a00;">Normalized ECG Signal (Min-Max Scaling)</h4>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(normalized_signal)


    if selected_section == "R-Peak Detection":
        st.title("R-Peak Detection")

        # Sélection patient / canal
        ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
            121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
            220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

        channels = {'MLII': 0, 'V5': 1}

        with st.sidebar:
            st.header("Signal Selection")
            patient = st.selectbox("Select Patient ID", ids)
            channel = st.selectbox("Select Channel", channels.keys())

        # Introduction
        st.markdown(f"""
        <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#003366;margin-top:0;">R-Peak Detection on Patient {patient} – Channel {channel}</h3>
            <p style="font-size:16px;">The signal is filtered using your previously chosen method and analyzed to locate the R-peaks corresponding to each heartbeat.</p>
        </div>
        """, unsafe_allow_html=True)

        # Chargement et filtrage du signal
        record = wfdb.rdrecord(f'ecg/data/{patient}')
        signal = record.p_signal
        fs = record.fs
        end = int(10 * fs)

        st.markdown(f"""
        <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#004c6d;">Filtering Method Used</h4>
            <p style="font-size:16px;">{st.session_state.get('chosen_filter', 'Median Filter')}</p>
        </div>
        """, unsafe_allow_html=True)

        clean_signal = median_bandpass_filter(signal[:end, channels[channel]])

        # Affichage du signal filtré
        st.markdown("""
        <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#1f77b4;">Filtered ECG Signal (10 seconds)</h4>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(clean_signal)

        # Détection des R-peaks avec NeuroKit
        ecg_signals, ecg_info = nk.ecg_process(clean_signal, sampling_rate=360)
        r_peaks = ecg_info["ECG_R_Peaks"]

        # Visualisation des R-peaks
        st.markdown("""
        <div style="background-color:#e0f8ec;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#208060;">Detected R-Peaks on ECG</h4>
            <p style="font-size:16px;">The following graph shows the ECG signal with detected R-peaks marked in red.</p>
        </div>
        """, unsafe_allow_html=True)
        plot_ecg_with_rpeaks(clean_signal, r_peaks, fs=360, duration=end)

        # Segmentation des battements
        st.markdown("""
        <div style="background-color:#fff9e6;padding:25px 40px;border-left:5px solid #f4a300;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#b36b00;">Beat Segmentation</h4>
            <p style="font-size:16px;">The signal has been segmented around each detected R-peak to extract individual beats.</p>
        </div>
        """, unsafe_allow_html=True)

        beats = extract_beats(clean_signal, r_peaks)
        st.markdown(f"**Number of beats extracted:** {len(beats)}")

        # Exploration des battements
        st.markdown("""
        <div style="background-color:#f7fbfc;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h4 style="color:#1b4965;">Beat Visualization (First 5 Beats)</h4>
            <p style="font-size:16px;">Each plot below represents an individual heartbeat extracted from the signal.</p>
        </div>
        """, unsafe_allow_html=True)

        fig, axs = plt.subplots(1, 5, figsize=(15, 2))

        # Enlever le fond blanc du canvas général
        fig.patch.set_alpha(0)

        for i in range(5):
            axs[i].plot(beats[i], color="steelblue")
            axs[i].set_title(f"Beat {i}", fontsize=10)
            axs[i].axis("off")
            axs[i].set_facecolor("none")  # Pas de fond pour chaque plot

        st.pyplot(fig)


    if selected_section == "Data Compression":
        st.title("Data Compression")

        ids = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
            121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
            220, 221, 222, 223, 228, 230, 231, 232, 233, 234]

        channels = {'MLII': 0, 'V5': 1}

        with st.sidebar:
            st.header("Signal Selection")
            patient = st.selectbox("Select Patient ID", ids)
            channel = st.selectbox("Select Channel", channels.keys())
            methods = ["Wavelet Level 1", "Wavelet Multilevel"]
            method = st.selectbox("Compression Method", methods)

        # Chargement du signal
        record = wfdb.rdrecord(f'ecg/data/{patient}')
        signal = record.p_signal
        fs = record.fs
        end = int(10 * fs)

        st.markdown(f"""
        <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h3 style="color:#003366;margin-top:0;">Original ECG Signal – Patient {patient}, Channel {channel}</h3>
            <p style="font-size:16px;">This is the raw signal (10 seconds) from the selected channel, before compression.</p>
        </div>
        """, unsafe_allow_html=True)
        st.line_chart(signal[0:end, channels[channel]])

        st.markdown(f"**Signal shape:** {signal.shape}")
        original_size = os.path.getsize(f"ecg/data/{patient}.dat")
        st.markdown(f"**Original .dat file size:** {original_size / 1024:.2f} KB")

        st.markdown(f"""
        <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:25px">
            <h4 style="color:#004c6d;">Selected Compression Method</h4>
            <p style="font-size:16px;">{method}</p>
        </div>
        """, unsafe_allow_html=True)

        if method == "Wavelet Level 1":
            st.markdown("""
            <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:25px">
                <h4 style="color:#1f77b4;">Wavelet Decomposition – Level 1 (db3)</h4>
            </div>
            """, unsafe_allow_html=True)

            cA, cD = pywt.dwt(signal[:end, channels[channel]], 'db3')

            limit = st.slider("Select number of coefficients to visualize", min_value=100, max_value=2000, value=500, step=50)

            st.line_chart(cA[:limit])
            st.line_chart(cD[:limit])

            st.markdown("""
            <div style="background-color:#f9f9f9;border-left:5px solid #999;padding:25px 40px;border-radius:12px;margin-bottom:20px">
                <h4 style="color:#444;">Reconstructed Signal (from A1+D1)</h4>
            </div>
            """, unsafe_allow_html=True)

            reconstructed_signal = pywt.idwt(cA, cD, 'db3')
            st.line_chart(reconstructed_signal[:limit])

            # Compression fichier
            output_dir = "ecg/data/compressed"
            os.makedirs(output_dir, exist_ok=True)

            compressed_channels = []
            for i in range(signal.shape[1]):
                cA, _ = pywt.dwt(signal[:, i], wavelet='db4')  # niveau 1
                compressed_channels.append(cA)

            min_len = min(len(c) for c in compressed_channels)
            compressed_signal = np.vstack([c[:min_len] for c in compressed_channels]).T

            wfdb.wrsamp(record_name=os.path.join(output_dir, f"{patient}_wavelet1_compressed"),
                        fs=fs,
                        units=record.units,
                        sig_name=record.sig_name,
                        p_signal=compressed_signal)

            compressed_size = os.path.getsize(os.path.join(output_dir, f"{patient}_wavelet1_compressed.dat"))
            st.markdown(f"**Compressed file size:** {compressed_size / 1024:.2f} KB")
            st.markdown(f"**Compression ratio:** {compressed_size / original_size:.2%}")

        elif method == "Wavelet Multilevel":
            level = st.slider("Select decomposition level", min_value=1, max_value=5, value=3, step=1)

            st.markdown(f"""
            <div style="background-color:#ffffff;border-left:5px solid #ff7f0e;padding:25px 40px;border-radius:12px;margin-bottom:25px">
                <h4 style="color:#d65c00;">Wavelet Multilevel Decomposition – Level {level}</h4>
            </div>
            """, unsafe_allow_html=True)

            coeffs = pywt.wavedec(signal[:end, channels[channel]], 'db4', level=level)

            for i, coeff in enumerate(coeffs):
                st.line_chart(coeff[:end])
                if i == 0:
                    st.markdown(f"**Approximation A{level}**")
                else:
                    st.markdown(f"**Detail D{level - i + 1}**")

            st.markdown("""
            <div style="background-color:#f9f9f9;border-left:5px solid #999;padding:25px 40px;border-radius:12px;margin-bottom:20px">
                <h4 style="color:#444;">Reconstructed Signal (from all levels)</h4>
            </div>
            """, unsafe_allow_html=True)

            reconstructed_signal = pywt.waverec(coeffs, 'db4')[:end]
            st.line_chart(reconstructed_signal)


    if selected_section == "Exploratory Data Analysis":
        st.title("Exploratory Data Analysis")

        DATA_DIR = 'ecg/data'
        WINDOW_SIZE = 200

        @st.cache_resource
        def load_beat_statistics():
            all_labels = []
            patient_label_map = {}

            for filename in os.listdir(DATA_DIR):
                if filename.endswith('.dat'):
                    record_name = filename[:-4]
                    record_path = os.path.join(DATA_DIR, record_name)

                    try:
                        record = wfdb.rdrecord(record_path)
                        annotation = wfdb.rdann(record_path, 'atr')
                        ecg_signal = record.p_signal[:, 0]
                    except:
                        continue

                    labels = []
                    for i, sample in enumerate(annotation.sample):
                        label = annotation.symbol[i]
                        if label not in ['N', 'L', 'R', 'A', 'V']:
                            continue
                        start = sample - WINDOW_SIZE // 2
                        end = sample + WINDOW_SIZE // 2
                        if start >= 0 and end < len(ecg_signal):
                            labels.append(label)
                            all_labels.append(label)

                    patient_label_map[record_name] = labels

            return all_labels, patient_label_map


        def show_beat_distribution():
            st.markdown("""
            <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:20px">
                <h3 style="color:#003366;">Beat Distribution Overview</h3>
                <p style="font-size:16px;">This section provides a global view of the types of beats annotated in the dataset.</p>
            </div>
            """, unsafe_allow_html=True)

            all_labels, patient_label_map = load_beat_statistics()
            label_counts = Counter(all_labels)
            df_label_counts = pd.DataFrame(label_counts.items(), columns=['Label', 'Count']).sort_values(by='Count', ascending=False)

            # Total Beats per Class
            st.markdown("""
            <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
                <h4 style="color:#1f77b4;">Total Beats per Class</h4>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_label_counts)

            fig, ax = plt.subplots()
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")
            sns.barplot(data=df_label_counts, x='Label', y='Count', palette='Set2', ax=ax)
            ax.set_title("Total Beats per Label")
            st.pyplot(fig)

            # Normal vs Abnormal
            total_normal = label_counts.get('N', 0)
            total_abnormal = sum(label_counts[l] for l in ['L', 'R', 'A', 'V'])
            df_bin = pd.DataFrame({'Class': ['Normal', 'Abnormal'], 'Count': [total_normal, total_abnormal]})

            st.markdown("""
            <div style="background-color:#eaf4ff;padding:25px 40px;border-radius:12px;margin-bottom:20px">
                <h4 style="color:#004c6d;">Normal vs Abnormal Beats</h4>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Normal Beats", total_normal)
            with col2:
                st.metric("Abnormal Beats", total_abnormal)

            fig2, ax2 = plt.subplots()
            fig2.patch.set_alpha(0)
            ax2.set_facecolor("none")
            sns.barplot(data=df_bin, x='Class', y='Count', palette='coolwarm', ax=ax2)
            ax2.set_title("Binary Class Distribution")
            st.pyplot(fig2)

            # Per-patient Beat Count
            patient_data = []
            for patient, labels in patient_label_map.items():
                row = {
                    'Patient': patient,
                    'Total Beats': len(labels),
                    'Normal (N)': labels.count('N'),
                    'LBBB (L)': labels.count('L'),
                    'RBBB (R)': labels.count('R'),
                    'Atrial (A)': labels.count('A'),
                    'Ventricular (V)': labels.count('V'),
                }
                patient_data.append(row)
            
            df_patient = pd.DataFrame(patient_data).sort_values(by='Total Beats', ascending=False)

            st.markdown("""
            <div style="background-color:#fff9e6;border-left:5px solid #f4a300;padding:25px 40px;border-radius:12px;margin-bottom:20px">
                <h4 style="color:#b36b00;">Beat Distribution per Patient</h4>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_patient)

            fig3, ax3 = plt.subplots(figsize=(12, 5))
            fig3.patch.set_alpha(0)
            ax3.set_facecolor("none")
            df_patient.set_index("Patient")[["Normal (N)", "LBBB (L)", "RBBB (R)", "Atrial (A)", "Ventricular (V)"]].plot(
                kind="bar", stacked=True, ax=ax3)
            ax3.set_ylabel("Beats")
            ax3.set_title("Beats per Patient")
            st.pyplot(fig3)

        show_beat_distribution()


def page_frequency_analysis():
    import streamlit as st
    import os
    import numpy as np
    import wfdb
    import matplotlib.pyplot as plt

    #st.set_page_config(layout="wide")

    WINDOW_SIZE = 200
    DATA_DIR = "ecg/data"
    CHANNELS = {'MLII': 0, 'V5': 1}  # Adaptable selon les leads disponibles

    def compute_fft(signal, fs=360):
        N = len(signal)
        freqs = np.fft.fftfreq(N, d=1/fs)
        fft_values = np.fft.fft(signal)
        magnitude = np.abs(fft_values)
        return freqs[:N // 2], magnitude[:N // 2]

    def get_beats_by_label(record_path, target_label, channel_index):
        record = wfdb.rdrecord(record_path)
        annotation = wfdb.rdann(record_path, 'atr')
        signal = record.p_signal[:, channel_index]

        beats = []
        for i, sample in enumerate(annotation.sample):
            label = annotation.symbol[i]
            if label != target_label:
                continue
            start = sample - WINDOW_SIZE // 2
            end = sample + WINDOW_SIZE // 2
            if start >= 0 and end < len(signal):
                beat = signal[start:end]
                beats.append(beat)
        return beats

    def plot_comparison(normal_beat, abnormal_beat):
        f1, mag1 = compute_fft(normal_beat)
        f2, mag2 = compute_fft(abnormal_beat)

        fig, axes = plt.subplots(2, 2, figsize=(12, 6))
        fig.patch.set_alpha(0)
        for ax in axes.flatten():
            ax.set_facecolor("none")

        axes[0, 0].plot(normal_beat, color="steelblue")
        axes[0, 0].set_title("Normal Beat (Time Domain)")

        axes[0, 1].plot(f1, mag1, color="teal")
        axes[0, 1].set_title("Normal Beat (Frequency Domain)")

        axes[1, 0].plot(abnormal_beat, color="indianred")
        axes[1, 0].set_title("Abnormal Beat (Time Domain)")

        axes[1, 1].plot(f2, mag2, color="darkred")
        axes[1, 1].set_title("Abnormal Beat (Frequency Domain)")

        for ax in axes.flatten():
            ax.grid(True)

        plt.tight_layout()
        st.pyplot(fig)

    def main():
        st.title("Beat Comparison: Time vs Frequency")

        st.markdown("""
        <div style="background-color:#f0f4fa;padding:25px 40px;border-radius:12px;margin-bottom:20px">
            <h3 style="color:#003366;margin-top:0;">Compare ECG Beats in Time and Frequency Domains</h3>
            <p style="font-size:16px;">
                This tool allows you to explore the difference between a <strong>normal</strong> and an <strong>abnormal</strong> heartbeat
                from the same patient and specific ECG lead.
            </p>
        </div>
        """, unsafe_allow_html=True)

        patients = sorted([f[:-4] for f in os.listdir(DATA_DIR) if f.endswith('.dat')])

        with st.sidebar:
            st.header("Signal Selection")
            selected_patient = st.selectbox("Select Patient", patients)
            selected_channel = st.selectbox("Select Channel", CHANNELS.keys())

        if selected_patient:
            record_path = os.path.join(DATA_DIR, selected_patient)
            channel_index = CHANNELS[selected_channel]

            normal_beats = get_beats_by_label(record_path, 'N', channel_index)
            abnormal_beats = []
            for label in ['L', 'R', 'A', 'V']:
                abnormal_beats += get_beats_by_label(record_path, label, channel_index)

            if not normal_beats or not abnormal_beats:
                st.warning("This patient does not have both normal and abnormal beats for this channel.")
                return

            col1, col2 = st.columns(2)
            with col1:
                idx_n = st.slider("Select Normal Beat", 0, len(normal_beats)-1, 0)
            with col2:
                idx_a = st.slider("Select Abnormal Beat", 0, len(abnormal_beats)-1, 0)

            st.markdown(f"""
            <div style="background-color:#ffffff;border-left:5px solid #1f77b4;padding:25px 40px;border-radius:12px;margin-bottom:20px">
                <h4 style="color:#1f77b4;">Comparison for Patient <code>{selected_patient}</code> - Channel <code>{selected_channel}</code></h4>
            </div>
            """, unsafe_allow_html=True)

            plot_comparison(normal_beats[idx_n], abnormal_beats[idx_a])

    main()


def page_models():
    from ecg.detection_methods import article_method, autoencoder, isolation_forest
    import streamlit as st
    from streamlit_option_menu import option_menu

    #st.set_page_config(layout="wide")

    # Define sections and their content
    sections = [ 
        "CNN Method",
        "Autoencoder Method",
        "Isolation Forest Method"
    
    ]

    # Sidebar: clickable list of sections
    with st.sidebar:
        selected_section = option_menu(
            menu_title=None,
            options=sections,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "nav-link-selected": {"background-color": "#dde7e4", "color": "black",}
            }
        )


    if selected_section == "CNN Method":
        st.title("ECG Arrhythmia Detection")
        st.markdown("Based on the **shallow CNN model** from Rasti et al. (2024)")

        article_method()

    if selected_section == "Autoencoder Method":
        
        autoencoder()


    if selected_section == "Isolation Forest Method":
        
        isolation_forest()






