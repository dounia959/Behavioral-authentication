/**
 * Behavioral Authentication System - Frontend JavaScript
 * Handles UI interactions and API calls
 */

// ============================================================================
// STATE MANAGEMENT
// ============================================================================

const state = {
    trainFileUploaded: false,
    testFileUploaded: false,
    modelsTrained: false,
    isTraining: false,
    isTesting: false,
    statusCheckInterval: null
};

// ============================================================================
// DOM ELEMENTS
// ============================================================================

const elements = {
    // Training section
    trainUploadArea: document.getElementById('trainUploadArea'),
    trainFileInput: document.getElementById('trainFileInput'),
    trainFileStatus: document.getElementById('trainFileStatus'),
    trainFileName: document.getElementById('trainFileName'),
    clearTrainBtn: document.getElementById('clearTrainBtn'),
    trainBtn: document.getElementById('trainBtn'),
    trainingStatus: document.getElementById('trainingStatus'),
    trainingLogs: document.getElementById('trainingLogs'),
    logsContent: document.getElementById('logsContent'),
    trainingSuccess: document.getElementById('trainingSuccess'),
    trainingError: document.getElementById('trainingError'),
    errorMessage: document.getElementById('errorMessage'),

    // Test section
    testUploadArea: document.getElementById('testUploadArea'),
    testFileInput: document.getElementById('testFileInput'),
    testFileStatus: document.getElementById('testFileStatus'),
    testFileName: document.getElementById('testFileName'),
    clearTestBtn: document.getElementById('clearTestBtn'),
    testBtn: document.getElementById('testBtn'),

    // Result section
    noResult: document.getElementById('noResult'),
    resultContainer: document.getElementById('resultContainer'),
    verdictBox: document.getElementById('verdictBox'),
    verdictText: document.getElementById('verdictText'),
    confidenceLevel: document.getElementById('confidenceLevel'),
    confidenceText: document.getElementById('confidenceText'),
    totalWindows: document.getElementById('totalWindows'),
    legitWindows: document.getElementById('legitWindows'),
    anomalyWindows: document.getElementById('anomalyWindows'),
    threshold: document.getElementById('threshold'),
    resultTime: document.getElementById('resultTime'),

    // System controls
    resetBtn: document.getElementById('resetBtn'),
    systemStatus: document.getElementById('systemStatus'),
    statusText: document.getElementById('statusText')
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkInitialStatus();
    startStatusPolling();
});

function initializeEventListeners() {
    // Training file upload
    elements.trainUploadArea.addEventListener('click', () => elements.trainFileInput.click());
    elements.trainFileInput.addEventListener('change', handleTrainFileSelect);
    elements.trainUploadArea.addEventListener('dragover', handleDragOver);
    elements.trainUploadArea.addEventListener('dragleave', handleDragLeave);
    elements.trainUploadArea.addEventListener('drop', (e) => handleTrainFileDrop(e));
    elements.clearTrainBtn.addEventListener('click', clearTrainFile);
    elements.trainBtn.addEventListener('click', handleTrainClick);

    // Test file upload
    elements.testUploadArea.addEventListener('click', () => elements.testFileInput.click());
    elements.testFileInput.addEventListener('change', handleTestFileSelect);
    elements.testUploadArea.addEventListener('dragover', handleDragOver);
    elements.testUploadArea.addEventListener('dragleave', handleDragLeave);
    elements.testUploadArea.addEventListener('drop', (e) => handleTestFileDrop(e));
    elements.clearTestBtn.addEventListener('click', clearTestFile);
    elements.testBtn.addEventListener('click', handleTestClick);

    // System controls
    elements.resetBtn.addEventListener('click', handleReset);
}

// ============================================================================
// FILE UPLOAD HANDLERS
// ============================================================================

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
}

function handleTrainFileDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0], 'train');
    }
}

function handleTestFileDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0], 'test');
    }
}

function handleTrainFileSelect(e) {
    if (e.target.files.length > 0) {
        uploadFile(e.target.files[0], 'train');
    }
}

function handleTestFileSelect(e) {
    if (e.target.files.length > 0) {
        uploadFile(e.target.files[0], 'test');
    }
}

function uploadFile(file, type) {
    if (!file.name.endsWith('.csv')) {
        showError('Only CSV files are allowed');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    updateStatus('busy', 'Uploading...');

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (type === 'train') {
                state.trainFileUploaded = true;
                elements.trainFileName.textContent = `✓ ${file.name} (${data.rows} events)`;
                elements.trainFileStatus.classList.remove('hidden');
                elements.trainUploadArea.classList.add('hidden');
                elements.clearTrainBtn.style.display = 'inline-block';
                showNotification(`Training data uploaded: ${data.rows} events`);
            } else {
                state.testFileUploaded = true;
                elements.testFileName.textContent = `✓ ${file.name} (${data.rows} events)`;
                elements.testFileStatus.classList.remove('hidden');
                elements.testUploadArea.classList.add('hidden');
                elements.clearTestBtn.style.display = 'inline-block';
                showNotification(`Test data uploaded: ${data.rows} events`);
            }
            updateStatus('idle', 'Ready');
        } else {
            showError(data.error || 'Upload failed');
            updateStatus('error', 'Error');
        }
    })
    .catch(error => {
        showError('Upload error: ' + error.message);
        updateStatus('error', 'Error');
    });
}

function clearTrainFile() {
    state.trainFileUploaded = false;
    elements.trainFileInput.value = '';
    elements.trainFileStatus.classList.add('hidden');
    elements.trainUploadArea.classList.remove('hidden');
    elements.clearTrainBtn.style.display = 'none';
    elements.trainBtn.disabled = true;
}

function clearTestFile() {
    state.testFileUploaded = false;
    elements.testFileInput.value = '';
    elements.testFileStatus.classList.add('hidden');
    elements.testUploadArea.classList.remove('hidden');
    elements.clearTestBtn.style.display = 'none';
    elements.testBtn.disabled = true;
}

// ============================================================================
// TRAINING HANDLER
// ============================================================================

function handleTrainClick() {
    if (!state.trainFileUploaded) {
        showError('Please upload training data first');
        return;
    }

    if (state.isTraining) {
        showError('Training already in progress');
        return;
    }

    state.isTraining = true;
    elements.trainBtn.disabled = true;
    elements.trainingStatus.classList.remove('hidden');
    elements.trainingLogs.classList.remove('hidden');
    elements.trainingSuccess.classList.add('hidden');
    elements.trainingError.classList.add('hidden');
    elements.logsContent.innerHTML = '';

    updateStatus('busy', 'Training models...');

    fetch('/api/train', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                pollTrainingProgress();
            } else {
                showError(data.error);
                state.isTraining = false;
                elements.trainBtn.disabled = false;
                updateStatus('error', 'Training failed');
            }
        })
        .catch(error => {
            showError('Training request failed: ' + error.message);
            state.isTraining = false;
            elements.trainBtn.disabled = false;
            updateStatus('error', 'Error');
        });
}

function pollTrainingProgress() {
    const pollInterval = setInterval(() => {
        fetch('/api/logs')
            .then(response => response.json())
            .then(data => {
                updateTrainingLogs(data.logs);
            });

        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                if (!data.training) {
                    clearInterval(pollInterval);
                    state.isTraining = false;

                    if (data.error) {
                        elements.trainingStatus.classList.add('hidden');
                        elements.trainingError.classList.remove('hidden');
                        elements.errorMessage.textContent = data.error;
                        updateStatus('error', 'Training failed');
                    } else {
                        state.modelsTrained = true;
                        elements.trainingStatus.classList.add('hidden');
                        elements.trainingSuccess.classList.remove('hidden');
                        elements.trainingLogs.classList.add('hidden');
                        elements.trainBtn.disabled = false;

                        // Enable test button
                        elements.testBtn.disabled = false;

                        updateStatus('idle', 'Ready');
                        showNotification('✓ Models trained successfully!');
                    }
                }
            });
    }, 500);
}

function updateTrainingLogs(logs) {
    elements.logsContent.innerHTML = logs.map(log => `<div>${log}</div>`).join('');
    elements.logsContent.scrollTop = elements.logsContent.scrollHeight;
}

// ============================================================================
// TEST HANDLER
// ============================================================================

function handleTestClick() {
    if (!state.testFileUploaded) {
        showError('Please upload test data first');
        return;
    }

    if (!state.modelsTrained) {
        showError('Please train models first');
        return;
    }

    if (state.isTesting) {
        showError('Test already in progress');
        return;
    }

    state.isTesting = true;
    elements.testBtn.disabled = true;
    updateStatus('busy', 'Running authentication test...');

    fetch('/api/test', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                pollTestProgress();
            } else {
                showError(data.error);
                state.isTesting = false;
                elements.testBtn.disabled = false;
                updateStatus('error', 'Test failed');
            }
        })
        .catch(error => {
            showError('Test request failed: ' + error.message);
            state.isTesting = false;
            elements.testBtn.disabled = false;
            updateStatus('error', 'Error');
        });
}

function pollTestProgress() {
    const pollInterval = setInterval(() => {
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                if (!data.testing) {
                    clearInterval(pollInterval);
                    state.isTesting = false;
                    elements.testBtn.disabled = false;

                    if (data.error) {
                        showError(data.error);
                        updateStatus('error', 'Test failed');
                    } else if (data.last_result) {
                        displayResult(data.last_result);
                        updateStatus('idle', 'Ready');
                    }
                }
            });
    }, 500);
}

// ============================================================================
// RESULT DISPLAY
// ============================================================================

function displayResult(result) {
    elements.noResult.classList.add('hidden');
    elements.resultContainer.classList.remove('hidden');

    // Verdict
    const isLegit = result.is_legitimate;
    elements.verdictText.textContent = result.verdict;
    elements.verdictText.className = `verdict-text ${isLegit ? 'legit' : 'anomaly'}`;

    // Confidence bar
    const confidence = result.confidence || 0;
    elements.confidenceLevel.style.width = confidence + '%';
    elements.confidenceLevel.textContent = confidence + '%';

    // Confidence text
    if (isLegit) {
        elements.confidenceText.textContent = `✓ Legitimate with ${confidence}% confidence (threshold: ${(result.threshold * 100).toFixed(0)}%)`;
        elements.confidenceText.style.color = 'var(--success-color)';
    } else {
        elements.confidenceText.textContent = `✗ Anomaly detected with ${(100 - confidence).toFixed(0)}% anomaly score (threshold: ${(result.threshold * 100).toFixed(0)}%)`;
        elements.confidenceText.style.color = 'var(--danger-color)';
    }

    // Statistics
    elements.totalWindows.textContent = result.total_windows;
    elements.legitWindows.textContent = result.legitimate_windows;
    elements.anomalyWindows.textContent = result.anomaly_windows;
    elements.threshold.textContent = `${(result.threshold * 100).toFixed(0)}%`;

    // Timestamp
    const date = new Date(result.timestamp);
    elements.resultTime.textContent = date.toLocaleString();

    showNotification(`✓ Test completed: ${result.verdict}`);
}

// ============================================================================
// SYSTEM CONTROLS
// ============================================================================

function handleReset() {
    if (!confirm('Are you sure you want to reset the system? This will delete all trained models.')) {
        return;
    }

    updateStatus('busy', 'Resetting...');

    fetch('/api/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reset state
                state.modelsTrained = false;
                state.trainFileUploaded = false;
                state.testFileUploaded = false;

                // Reset UI
                elements.trainFileStatus.classList.add('hidden');
                elements.trainUploadArea.classList.remove('hidden');
                elements.clearTrainBtn.style.display = 'none';
                elements.trainFileInput.value = '';

                elements.testFileStatus.classList.add('hidden');
                elements.testUploadArea.classList.remove('hidden');
                elements.clearTestBtn.style.display = 'none';
                elements.testFileInput.value = '';

                elements.trainingSuccess.classList.add('hidden');
                elements.trainingError.classList.add('hidden');
                elements.trainingStatus.classList.add('hidden');
                elements.trainingLogs.classList.add('hidden');

                elements.noResult.classList.remove('hidden');
                elements.resultContainer.classList.add('hidden');

                // Enable/disable buttons
                elements.trainBtn.disabled = !state.trainFileUploaded;
                elements.testBtn.disabled = true;

                updateStatus('idle', 'Ready');
                showNotification('✓ System reset successfully');
            } else {
                showError(data.error);
                updateStatus('error', 'Reset failed');
            }
        })
        .catch(error => {
            showError('Reset failed: ' + error.message);
            updateStatus('error', 'Error');
        });
}

// ============================================================================
// STATUS MANAGEMENT
// ============================================================================

function updateStatus(status, text) {
    elements.systemStatus.className = `indicator-dot ${status}`;
    elements.statusText.textContent = text;
}

function checkInitialStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            state.modelsTrained = data.models_trained;
            elements.testBtn.disabled = !state.modelsTrained;
            if (data.last_result) {
                displayResult(data.last_result);
            }
            updateStatus('idle', 'Ready');
        })
        .catch(error => console.error('Failed to check initial status:', error));
}

function startStatusPolling() {
    state.statusCheckInterval = setInterval(() => {
        if (!state.isTraining && !state.isTesting) {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    state.modelsTrained = data.models_trained;
                    if (data.error) {
                        updateStatus('error', 'Error');
                    }
                })
                .catch(error => console.error('Status check failed:', error));
        }
    }, 5000);
}

// ============================================================================
// NOTIFICATIONS
// ============================================================================

function showNotification(message) {
    // Create a simple notification (can be replaced with toast library)
    console.log('Notification:', message);
    // You could implement a toast notification here
}

function showError(message) {
    console.error('Error:', message);
    // Toast or alert
    alert('Error: ' + message);
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function formatDate(timestamp) {
    return new Date(timestamp).toLocaleString();
}
