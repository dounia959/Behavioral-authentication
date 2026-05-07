"""
Flask backend for Continuous User Authentication system.
Provides API endpoints for data collection, training, and testing.
"""

import os
import json
from datetime import datetime
from pathlib import Path
import threading
import time

from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import numpy as np

from src.dataset import build_dataset
from src.models import train_models
from src.ensemble import predict_ensemble
from src.utils import ensure_dirs

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload

# Global state
app_state = {
    'collecting': False,
    'training': False,
    'testing': False,
    'models_trained': False,
    'last_result': None,
    'training_log': [],
    'error': None
}

ensure_dirs()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current application status"""
    return jsonify({
        'collecting': app_state['collecting'],
        'training': app_state['training'],
        'testing': app_state['testing'],
        'models_trained': app_state['models_trained'],
        'last_result': app_state['last_result'],
        'error': app_state['error']
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload training or test CSV file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        file_type = request.form.get('type', 'train')  # 'train' or 'test'

        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({'success': False, 'error': 'Only CSV files allowed'}), 400

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        if file_type == 'train':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'data_record.csv')
        else:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'test_session.csv')

        file.save(filepath)

        # Validate the CSV
        df = pd.read_csv(filepath)
        required_cols = {'timestamp', 'event_type', 'key', 'x', 'y'}
        missing = required_cols - set(df.columns)
        
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing columns: {", ".join(missing)}'
            }), 400

        return jsonify({
            'success': True,
            'message': f'File uploaded successfully ({len(df)} events)',
            'rows': len(df),
            'type': file_type
        })

    except Exception as e:
        app_state['error'] = str(e)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/train', methods=['POST'])
def train():
    """Train the models"""
    try:
        if app_state['training']:
            return jsonify({'success': False, 'error': 'Training already in progress'}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'data_record.csv')
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'No training data uploaded'}), 400

        app_state['training'] = True
        app_state['error'] = None
        app_state['training_log'] = []

        def train_worker():
            try:
                log_msg("Loading data from: " + file_path)
                X = build_dataset(file_path)
                
                if len(X) == 0:
                    raise Exception("No valid windows extracted. Check your data or window parameters.")

                log_msg(f"Dataset shape: {X.shape[0]} windows × {X.shape[1]} features")
                log_msg("Training models (SVM + Isolation Forest)...")
                
                train_models(X)
                app_state['models_trained'] = True
                
                log_msg("✓ Training complete!")
                app_state['error'] = None

            except Exception as e:
                app_state['error'] = str(e)
                log_msg(f"✗ Error: {str(e)}")
            finally:
                app_state['training'] = False

        thread = threading.Thread(target=train_worker, daemon=True)
        thread.start()

        return jsonify({'success': True, 'message': 'Training started'})

    except Exception as e:
        app_state['training'] = False
        app_state['error'] = str(e)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/test', methods=['POST'])
def test():
    """Run authentication test on test data"""
    try:
        if not app_state['models_trained']:
            return jsonify({'success': False, 'error': 'Models not trained yet'}), 400

        if app_state['testing']:
            return jsonify({'success': False, 'error': 'Test already in progress'}), 400

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test_session.csv')
        
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'No test data uploaded'}), 400

        app_state['testing'] = True
        app_state['error'] = None

        def test_worker():
            try:
                scaler = joblib.load("models/scaler.pkl")
                svm = joblib.load("models/svm.pkl")
                iso = joblib.load("models/iso.pkl")

                X_test = build_dataset(file_path)

                if len(X_test) == 0:
                    raise Exception("No valid windows in test data")

                final = predict_ensemble(svm, iso, scaler, X_test)

                total = len(final)
                legit = final.count(1)
                anomaly = final.count(-1)

                ratio = legit / total if total > 0 else 0
                threshold = 0.87

                is_legitimate = ratio > threshold
                confidence = round(ratio * 100, 2)

                app_state['last_result'] = {
                    'timestamp': datetime.now().isoformat(),
                    'total_windows': total,
                    'legitimate_windows': legit,
                    'anomaly_windows': anomaly,
                    'legitimacy_ratio': round(ratio, 4),
                    'confidence': confidence,
                    'is_legitimate': is_legitimate,
                    'verdict': 'LEGIT' if is_legitimate else 'ANOMALY',
                    'threshold': threshold
                }

                app_state['error'] = None

            except Exception as e:
                app_state['error'] = str(e)
            finally:
                app_state['testing'] = False

        thread = threading.Thread(target=test_worker, daemon=True)
        thread.start()

        return jsonify({'success': True, 'message': 'Test started'})

    except Exception as e:
        app_state['testing'] = False
        app_state['error'] = str(e)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/result', methods=['GET'])
def get_result():
    """Get the latest test result"""
    return jsonify(app_state['last_result'] or {})


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get training logs"""
    return jsonify({'logs': app_state['training_log']})


@app.route('/api/files', methods=['GET'])
def list_files():
    """List available data files"""
    try:
        files = {}
        data_dir = app.config['UPLOAD_FOLDER']

        if os.path.exists(data_dir):
            for filename in os.listdir(data_dir):
                if filename.endswith('.csv'):
                    filepath = os.path.join(data_dir, filename)
                    size = os.path.getsize(filepath)
                    df = pd.read_csv(filepath)
                    files[filename] = {
                        'size': size,
                        'rows': len(df),
                        'path': filepath
                    }

        return jsonify({'files': files})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset application state and delete models"""
    try:
        # Remove model files
        for model_file in ['models/scaler.pkl', 'models/svm.pkl', 'models/iso.pkl']:
            if os.path.exists(model_file):
                os.remove(model_file)

        app_state['models_trained'] = False
        app_state['last_result'] = None
        app_state['error'] = None
        app_state['training_log'] = []

        return jsonify({'success': True, 'message': 'System reset'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_msg(message):
    """Add message to training log"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    app_state['training_log'].append(log_entry)
    print(log_entry)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 50MB.'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Behavioral Authentication System - Web Interface")
    print("=" * 60)
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='localhost', port=5000)
