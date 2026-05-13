import threading
import uvicorn

from app.communication.gmail import start_email_listener
from app.services.scheduler import schedule_daily_report

schedule_daily_report("918924913047")


def run_gmail():

    start_email_listener()


if __name__ == "__main__":

    gmail_thread = threading.Thread(
        target=run_gmail,
        daemon=True,
        name="GmailListenerThread",
    )

    gmail_thread.start()

    uvicorn.run(
        "app.communication.whatsapp:app",
        host="0.0.0.0",
        port=8000,
    )
