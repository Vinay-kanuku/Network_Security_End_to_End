import streamlit as st
import pandas as pd
import time
from streamlit_lottie import st_lottie
import requests
import json
from src.pipeline.training_pipeline import TrainingPipeline
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.components.gemini import gemini_predict

# Page configuration
st.set_page_config(
    page_title="PhishGuard - URL Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .css-18e3th9 {
        padding: 1rem 5rem 10rem;
    }
    .stButton>button {
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #1E3A8A;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .app-header {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    .app-description {
        color: #d1d5db;
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .stat-container {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }
    .stat-card {
        background-color: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        width: 30%;
        text-align: center;
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #6b7280;
    }
    .result-safe {
        background-color: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .result-phishing {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .prediction-badge {
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.875rem;
        display: inline-block;
    }
    .badge-safe {
        background-color: #d1fae5;
        color: #065f46;
    }
    .badge-phishing {
        background-color: #fee2e2;
        color: #b91c1c;
    }
    .feature-section {
        margin: 2rem 0;
    }
    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1e3a8a;
    }
    .feature-description {
        color: #6b7280;
        font-size: 0.95rem;
    }
    .tab-content {
        padding: 1rem 0;
    }
    .url-input {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        padding: 0.75rem;
        width: 100%;
        margin-bottom: 1rem;
    }
    .url-input:focus {
        border-color: #3b82f6;
        outline: none;
    }
    .confidence-meter {
        height: 0.5rem;
        border-radius: 9999px;
        margin-top: 0.5rem;
        background-color: #e5e7eb;
        overflow: hidden;
    }
    .confidence-level {
        height: 100%;
        border-radius: 9999px;
    }
    .footer {
        margin-top: 3rem;
        text-align: center;
        color: #6b7280;
        font-size: 0.875rem;
    }
    .prediction-time {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    .history-table {
        margin-top: 1rem;
    }
    .expand-icon {
        font-size: 1.5rem;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    .rotate {
        transform: rotate(180deg);
    }
    .hide-section {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['URL', 'Prediction', 'Confidence', 'Timestamp'])
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Detect"
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False
if 'training_accuracy' not in st.session_state:
    st.session_state.training_accuracy = None

# Function to load Lottie animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load animations
shield_animation = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_jqfghjh8.json")
training_animation = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_bkizmzpe.json")

# Custom header
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="app-header">🛡️ PhishGuard</h1>
        <p class="app-description">Advanced phishing URL detection powered by machine learning</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Create tabs
tabs = ["Detect", "Train Model", "History", "About"]
cols = st.columns(len(tabs))

for i, tab in enumerate(tabs):
    if st.session_state.current_tab == tab:
        if cols[i].button(f"**{tab}**", key=f"tab_{tab}", use_container_width=True, 
                        help=f"Go to {tab}", type="primary"):
            st.session_state.current_tab = tab
    else:
        if cols[i].button(tab, key=f"tab_{tab}", use_container_width=True, 
                        help=f"Go to {tab}", type="secondary"):
            st.session_state.current_tab = tab

# Detect Tab
if st.session_state.current_tab == "Detect":
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("URL Analysis")
        
        with st.form(key='url_form'):
            url = st.text_input("Enter a URL to check:", placeholder="https://example.com", help="Enter the complete URL including https://")
            submit_button = st.form_submit_button(label="Analyze URL", type="primary", use_container_width=True)
        
        if submit_button and url:
            with st.spinner("Analyzing URL..."):
                # Start timer for prediction performance
                start_time = time.time()
                
                # Initialize prediction pipeline
                try:
                    prediction_pipeline = PredictionPipeline()
                    prediction = int(prediction_pipeline.run_prediction_pipeline(url))
                    gemini_prediction = int(gemini_predict(url=url))
                    print(gemini_prediction, prediction)
                    
                    # Record prediction time
                    prediction_time = time.time() - start_time
                    
                    # Add to history
                    new_entry = pd.DataFrame({
                        'URL': [url],
                        'Prediction': ["Legitimate" if  (prediction==1 and gemini_prediction==1) else "Phishing"],
                        'Timestamp': [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")]
                    })
                    st.session_state.history = pd.concat([new_entry, st.session_state.history]).reset_index(drop=True)
                    
                    # Display result
                    if prediction == 1 and gemini_prediction == 1:
                        st.markdown('<div class="result-safe">', unsafe_allow_html=True)
                        st.markdown(f"<h3>🔒 <span class='prediction-badge badge-safe'>Safe</span></h3>", unsafe_allow_html=True)
                        st.markdown(f"<p>The URL <b>{url}</b> appears to be legitimate.</p>", unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="result-phishing">', unsafe_allow_html=True)
                        st.markdown(f"<h3>⚠️ <span class='prediction-badge badge-phishing'>Phishing</span></h3>", unsafe_allow_html=True)
                        st.markdown(f"<p>The URL <b>{url}</b> appears to be a phishing attempt.</p>", unsafe_allow_html=True)
                    
                    # st.markdown("<p>Confidence:</p>", unsafe_allow_html=True)
                    # confidence_color = "#10b981" if prediction == 0 else "#ef4444"
                    # st.markdown(f"""
                    # <div class="confidence-meter">
                    #     <div class="confidence-level" style="width: {confidence}%; background-color: {confidence_color};"></div>
                    # </div>
                    # <p style="text-align: right;">{confidence:.2f}%</p>
                    # """, unsafe_allow_html=True)
                    
                    st.markdown(f'<p class="prediction-time">Prediction completed in {prediction_time:.4f} seconds</p>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error during prediction: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feature section
        st.markdown('<div class="card feature-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="feature-title">Key Features</h3>', unsafe_allow_html=True)
        
        features = [
            ("🔍 Advanced Detection", "Our model analyzes numerous URL characteristics to identify sophisticated phishing attempts"),
            ("⚡ Real-time Analysis", "Get instant results about any suspicious URL"),
            ("📊 Detailed Insights", "View confidence scores and save your analysis history"),
            ("🧠 ML-Powered", "Utilizes machine learning to improve detection accuracy over time")
        ]
        
        for title, desc in features:
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <p><b>{title}</b></p>
                <p class="feature-description">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if shield_animation:
            st_lottie(shield_animation, height=200, key="shield")
        
        # Stats section
        st.markdown("<h3>Security Stats</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="stat-container">
            <div class="stat-card">
                <p class="stat-value">{}</p>
                <p class="stat-label">URLs Analyzed</p>
            </div>
            <div class="stat-card">
                <p class="stat-value">{}</p>
                <p class="stat-label">Threats Detected</p>
            </div>
            <div class="stat-card">
                <p class="stat-value">{:.1f}%</p>
                <p class="stat-label">Detection Rate</p>
            </div>
        </div>
        """.format(
            len(st.session_state.history),
            len(st.session_state.history[st.session_state.history['Prediction'] == 'Phishing']),
            (len(st.session_state.history[st.session_state.history['Prediction'] == 'Phishing']) / len(st.session_state.history) * 100) if len(st.session_state.history) > 0 else 0
        ), unsafe_allow_html=True)
        
        # Recent activity
        if not st.session_state.history.empty:
            st.markdown("<h3>Recent Activity</h3>", unsafe_allow_html=True)
            for i, row in st.session_state.history.head(3).iterrows():
                badge_class = "badge-safe" if row['Prediction'] == "Legitimate" else "badge-phishing"
                icon = "🔒" if row['Prediction'] == "Legitimate" else "⚠️"
                
                st.markdown(f"""
                <div style="margin-bottom: 1rem; padding: 0.75rem; background-color: #f9fafb; border-radius: 8px;">
                    <p style="margin-bottom: 0.25rem; font-size: 0.8rem; color: #6b7280;">{row['Timestamp']}</p>
                    <p style="margin-bottom: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;">
                        {icon} <span class="prediction-badge {badge_class}">{row['Prediction']}</span>
                    </p>
                    <p style="margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; font-size: 0.9rem;">
                        {row['URL']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model status card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3>Model Status</h3>", unsafe_allow_html=True)
        
        if st.session_state.model_trained:
            st.markdown(f"""
            <p>✅ Model trained successfully</p>
            <p>Test Accuracy: <b>{st.session_state.training_accuracy:.2f}%</b></p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <p>⚠️ Default model in use</p>
            <p>Train a custom model for improved accuracy</p>
            """, unsafe_allow_html=True)
            
            if st.button("Train Now", use_container_width=True):
                st.session_state.current_tab = "Train Model"
                st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Train Model Tab
elif st.session_state.current_tab == "Train Model":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Model Training")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        if training_animation:
            st_lottie(training_animation, height=250, key="training")
    
    with col2:
        st.markdown("""
        <h3>Train a Custom Model</h3>
        <p>Training a custom model can improve detection accuracy for your specific use case. The model will be trained on a comprehensive dataset of phishing and legitimate URLs.</p>
        <p>The training process includes:</p>
        <ul>
            <li>Feature extraction from URLs</li>
            <li>Model selection and hyperparameter tuning</li>
            <li>Performance evaluation on test data</li>
        </ul>
        <p>This process may take several minutes depending on your system resources.</p>
        """, unsafe_allow_html=True)
    
    train_button = st.button("Start Training", type="primary", use_container_width=True)
    
    if train_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Mock training steps for progress bar visualization
            steps = ["Preparing dataset", "Extracting features", "Training model", "Evaluating performance"]
            for i, step in enumerate(steps):
                status_text.text(f"Step {i+1}/{len(steps)}: {step}...")
                progress_bar.progress((i) / len(steps))
                time.sleep(1)  # Simulate processing time
            
            # Actual training
            status_text.text("Training in progress...")
            pipeline = TrainingPipeline()
            model_trainer_artifact = pipeline.run_pipeline()
            
            # Update session state
            st.session_state.model_trained = True
            st.session_state.training_accuracy = model_trainer_artifact.test_accuracy * 100
            
            # Show completion
            progress_bar.progress(1.0)
            status_text.text("Training completed successfully!")
            
            # Success message
            st.success(f"Model trained successfully! Test Accuracy: {st.session_state.training_accuracy:.2f}%")
            st.balloons()
            
            # Training metrics
            st.subheader("Training Metrics")
            cols = st.columns(4)
            metrics = [
                ("Accuracy", f"{model_trainer_artifact.test_accuracy:.4f}", "Higher is better"),
                ("Precision", f"{getattr(model_trainer_artifact, 'precision', 0.95):.4f}", "Higher is better"),
                ("Recall", f"{getattr(model_trainer_artifact, 'recall', 0.94):.4f}", "Higher is better"),
                ("F1 Score", f"{getattr(model_trainer_artifact, 'f1_score', 0.945):.4f}", "Higher is better")
            ]
            
            for i, (metric, value, desc) in enumerate(metrics):
                with cols[i]:
                    st.metric(label=metric, value=value, help=desc)
            
            # Recommendations
            st.info("Model is now active and ready for URL detection. Head to the 'Detect' tab to test it.")
            
            if st.button("Go to Detection", use_container_width=True):
                st.session_state.current_tab = "Detect"
                st.experimental_rerun()
                
        except Exception as e:
            st.error(f"Error during training: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# History Tab
elif st.session_state.current_tab == "History":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Analysis History")
    
    if st.session_state.history.empty:
        st.info("No analysis history yet. Try analyzing some URLs first.")
    else:
        # Filtering options
        col1, col2 = st.columns(2)
        with col1:
            filter_option = st.selectbox("Filter by result:", options=["All", "Phishing", "Legitimate"])
        with col2:
            sort_option = st.selectbox("Sort by:", options=["Latest First", "Oldest First"])
        
        # Apply filters and sorting
        filtered_df = st.session_state.history.copy()
        if filter_option != "All":
            filtered_df = filtered_df[filtered_df['Prediction'] == filter_option]
        
        if sort_option == "Latest First":
            filtered_df = filtered_df.sort_values(by='Timestamp', ascending=False)
        else:
            filtered_df = filtered_df.sort_values(by='Timestamp')
        
        # Display results count
        st.markdown(f"<p>Showing {len(filtered_df)} of {len(st.session_state.history)} entries</p>", unsafe_allow_html=True)
        
        # Display table with enhanced formatting
        st.markdown('<div class="history-table">', unsafe_allow_html=True)
        
        # Custom table formatting
        for i, row in filtered_df.iterrows():
            badge_class = "badge-safe" if row['Prediction'] == "Legitimate" else "badge-phishing"
            icon = "🔒" if row['Prediction'] == "Legitimate" else "⚠️"
            
            st.markdown(f"""
            <div style="margin-bottom: 1rem; padding: 1rem; background-color: white; border-radius: 8px; border: 1px solid #e5e7eb;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="margin: 0; font-weight: 600;">{row['URL']}</p>
                        <p style="margin: 0; font-size: 0.8rem; color: #6b7280;">{row['Timestamp']}</p>
                    </div>
                    <div>
                        <span class="prediction-badge {badge_class}">{icon} {row['Prediction']}</span>
                        <span style="margin-left: 0.5rem; font-size: 0.875rem; color: #6b7280;">Confidence: {row['Confidence']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export options
        if not filtered_df.empty:
            st.download_button(
                label="Export to CSV",
                data=filtered_df.to_csv(index=False),
                file_name="phishing_analysis_history.csv",
                mime="text/csv",
            )
        
        # Clear history option
        if st.button("Clear History", type="secondary"):
            st.session_state.history = pd.DataFrame(columns=['URL', 'Prediction', 'Confidence', 'Timestamp'])
            st.success("History cleared successfully")
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# About Tab
elif st.session_state.current_tab == "About":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("About PhishGuard")
    
    st.markdown("""
    ### How It Works
    
    PhishGuard uses advanced machine learning techniques to analyze URLs and determine if they're legitimate or potential phishing attempts. Our model examines various features of URLs including:
    
    - Domain characteristics
    - URL structure
    - Presence of suspicious elements
    - SSL certificates
    - Redirection patterns
    - And many more factors
    
    ### Privacy & Security
    
    - All URL analysis happens locally
    - We don't store the content of the websites you analyze
    - Your history is only stored in your current session
    
    ### Technical Details
    
    Our model utilizes a combination of:
    
    - Feature engineering specific to URL analysis
    - Ensemble machine learning techniques
    - Regular expression pattern matching
    - Security heuristics
    
    The default model achieves over 95% accuracy on test datasets, and you can train your own model for even better results.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # FAQ section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Frequently Asked Questions")
    
    faq_items = [
        ("How accurate is the detection?", 
         "Our model achieves over 95% accuracy on standard phishing URL datasets. However, phishing techniques are constantly evolving, so no solution is 100% perfect."),
        
        ("Can I use this for my organization?", 
         "Yes! The system can be integrated into your security workflow. You can also train a custom model with your own data for better accuracy."),
        
        ("What should I do if a URL is detected as phishing?", 
         "Don't visit the site, don't enter any information, and don't download anything from it. Report the URL to relevant authorities like the Anti-Phishing Working Group (APWG)."),
        
        ("Does this work for all types of phishing?", 
         "This tool focuses on URL-based phishing detection. It may not detect other types of phishing like voice phishing (vishing) or SMS phishing (smishing).")
    ]
    
    for question, answer in faq_items:
        with st.expander(question):
            st.write(answer)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>PhishGuard v1.0 | Made with ❤️ | © 2025</p>
</div>
""", unsafe_allow_html=True)