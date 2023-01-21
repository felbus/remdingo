from flask import Blueprint, render_template, request, jsonify

from remdingo.services.message_processor import MessageProcessor
from remdingo.services.reminders_check import RemindersCheck
from remdingo.storage.reminders_repo import RemindersRepo


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    return render_template(
        "dashboard/index.html"
    )


@dashboard_bp.route("/faq")
def faq():
    return render_template(
        "dashboard/faq.html"
    )


@dashboard_bp.route("/about")
def about():
    return render_template(
        "dashboard/about.html"
    )


@dashboard_bp.route("/examples")
def examples():
    return render_template(
        "dashboard/examples.html"
    )


@dashboard_bp.route('/check_reminders')
def check_reminders():
    customer_id = request.args.get("customerId", default="")
    reminders = RemindersCheck.check_reminders(customer_id)

    return jsonify({
        "reminders": reminders
    })


@dashboard_bp.route('/ack_reminder')
def ack_reminder():
    customer_id = request.args.get("customerId", default="")
    ack = request.args.get('ack')
    offset = request.args.get('offset')
    message = RemindersCheck.process_reminder_ack(customer_id, ack, int(offset))

    return jsonify({
        "message": message
    })


@dashboard_bp.route('/process_reminder')
def process_reminder():
    customer_id = request.args.get("customerId", default="")

    if not customer_id or len(customer_id) == 0:
        return jsonify({
            "message": "please register or allow cookies for remdingo to work"
        })

    message = request.args.get('message')
    offset = request.args.get('offset')
    tz = request.args.get('tz')

    message_components = message.split(' ')

    if len(message_components) == 1 and message_components[0] == "list":
        reminders_df = RemindersRepo.get_all_reminders(customer_id)
        reminders = []
        if len(reminders_df) > 0:
            for idx, row in reminders_df.iterrows():
                reminders.append({
                    'reminder': row['reminder_text'],
                    'dt': row['reminder_date_user'],
                    'reminder_id': row['id'],
                })
        return jsonify({
            "reminders": reminders,
            "message": "list"
        })

    if len(message_components) == 1 and message_components[0] == "history":
        reminders_df = RemindersRepo.get_reminders_history(customer_id)
        reminders = []
        if len(reminders_df) > 0:
            for idx, row in reminders_df.iterrows():
                reminders.append({
                    'reminder': row['reminder_text'],
                    'dt': row['reminder_date_user'],
                    'reminder_id': row['id'],
                })
        return jsonify({
            "reminders": reminders,
            "message": "history"
        })

    mp = MessageProcessor()
    response_message = mp.process_and_store_message(customer_id, message, int(offset), tz=tz)

    return jsonify({
        "message": response_message
    })
