from flask import Flask, request, jsonify, send_from_directory
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__, static_folder=".", static_url_path="")

MAIL_HOST = os.environ.get("MAIL_HOST", "smtp.gmail.com")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
MAIL_USER = "vladram3707@gmail.com"
MAIL_PASSWORD = "opvb ckvs uytg ltbb"
MAIL_TO = os.environ.get("MAIL_TO", "vladram4707@gmail.com")


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/request", methods=["POST"])
def handle_request():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not phone:
        return jsonify({
            "ok": False,
            "message": "Укажите имя и телефон."
        }), 400

    if not MAIL_USER or not MAIL_PASSWORD:
        return jsonify({
            "ok": False,
            "message": "Email не настроен на сервере."
        }), 500

    email_body = f"""Новая заявка с сайта ЛГКА

Имя: {name}
Телефон: {phone}
Вопрос: {message or "Не указан"}
"""

    msg = EmailMessage()
    msg["Subject"] = "Новая заявка с сайта ЛГКА"
    msg["From"] = MAIL_USER
    msg["To"] = MAIL_TO
    msg.set_content(email_body)

    try:
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(MAIL_USER, MAIL_PASSWORD)
            smtp.send_message(msg)

    except Exception as error:
        print("Email sending error:", error)
        return jsonify({
            "ok": False,
            "message": "Не удалось отправить заявку."
        }), 500

    return jsonify({
        "ok": True,
        "message": "Спасибо! Мы свяжемся с вами в ближайшее время."
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
