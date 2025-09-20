from prometheus_client import Counter, Histogram, generate_latest
from flask import Response

# Prometheus metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['endpoint'])

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

# Update existing endpoints to track metrics
@app.route('/')
def index():
    with REQUEST_LATENCY.labels('/').time():
        REQUEST_COUNT.labels('/').inc()
        return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    with REQUEST_LATENCY.labels('/predict').time():
        REQUEST_COUNT.labels('/predict').inc()
        try:
            if model is None:
                return jsonify({'error': 'Model not loaded'}), 500
            data = request.get_json()
            image_data = data.get('image')
            if not image_data:
                return jsonify({'error': 'No image data provided'}), 400
            processed_image = preprocess_image(image_data)
            if processed_image is None:
                return jsonify({'error': 'Failed to process image'}), 400
            predictions = model.predict(processed_image)
            predicted_class = np.argmax(predictions[0])
            confidence = float(np.max(predictions[0]))
            class_probabilities = {str(i): float(predictions[0][i]) for i in range(10)}
            return jsonify({
                'predicted_number': int(predicted_class),
                'confidence': confidence,
                'all_probabilities': class_probabilities
            })
        except Exception as e:
            print(f"Error in prediction: {e}")
            return jsonify({'error': 'Prediction failed'}), 500

@app.route('/health')
def health():
    with REQUEST_LATENCY.labels('/health').time():
        REQUEST_COUNT.labels('/health').inc()
        return jsonify({'status': 'healthy', 'model_loaded': model is not None})