from flask import Flask, request, jsonify
import random
import time

from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Автоматические метрики HTTP-запросов
metrics = PrometheusMetrics(app, group_by='endpoint')

@app.route('/verify-user', methods=['POST'])
def verify_user():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    phone = data.get('phone')

    # Имитация задержки реального сервиса
    time.sleep(random.uniform(0.05, 0.6))

    # Очень простая "проверка"
    if email and '@' not in email:
        return jsonify({"error": "Invalid email format"}), 400

    if phone and not phone.startswith('+'):
        return jsonify({"error": "Phone must start with +"}), 400

    # Иногда падаем (имитация проблем у внешнего сервиса)
    if random.random() < 0.04:  # ~4%
        return jsonify({"error": "Internal service error"}), 500

    return jsonify({"status": "verified"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=False)