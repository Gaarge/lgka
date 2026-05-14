from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__, static_folder=".", static_url_path="")

TELEGRAM_BOT_TOKEN = "8732002591:AAHcccizcFdIPHgOd7J7I6rigcid0Y-frlk"
TELEGRAM_CHAT_ID = "5115609735"


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/request", methods=["POST"])
def handle_request():
    print("1")
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not phone:
        return jsonify({"ok": False, "message": "Укажите имя и телефон."}), 400

    text = (
        "Новая заявка с сайта ЛГКА\n\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Вопрос: {message or 'Не указан'}"
    )

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return jsonify({"ok": False, "message": "Telegram не настроен на сервере."}), 500

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        },
        timeout=10
    )

    if not response.ok:
        return jsonify({"ok": False, "message": "Не удалось отправить заявку."}), 500

    return jsonify({"ok": True, "message": "Спасибо! Мы свяжемся с вами в ближайшее время."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
