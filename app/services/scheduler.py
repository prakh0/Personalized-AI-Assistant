from apscheduler.schedulers.background import BackgroundScheduler
from app.services.stocks import get_market_summary
from app.communication.whatsapp import send_whatsapp_message

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.start()
print("Scheduler started")


def send_daily_market_report(user_id):
    print("Shedule triggered for user_id:", user_id)
    report = get_market_summary()
    send_whatsapp_message(user_id, report)


def schedule_daily_report(user_id, time="17:00"):
    hours, minutes = map(int, time.split(":"))
    print(f"Scheduling daily market report for user_id: {user_id}")
    scheduler.add_job(
        send_daily_market_report,
        "cron",
        hour=hours,
        minute=minutes,
        args=[user_id],
        id=f"market_{user_id}",
        replace_existing=True,
    )
