import time
import schedule
from datetime import datetime
from app.backend_DDD.core.commands import auth_commands as auth_cmds
from app.backend_DDD.core.database.database_api_queries import DatabaseManager



database = DatabaseManager()


def hourly_task():
    """Task to run at the start of every hour."""
    auth_cmds.update_pdc_menu(
        db_man=database
    )
    print(f"Hourly pdc scheduler executed at {datetime.now()}")

# Schedule the task
schedule.every().hour.at(":00").do(hourly_task)

def run_schedule():
    while True:
        print(f'Checking task at {datetime.now()}')
        schedule.run_pending()
        time.sleep(10)

if __name__ == '__main__':
    run_schedule()
