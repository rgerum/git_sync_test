import schedule
import time
import traceback
from git_sync import Git

git = Git()

def update_all():
    print(time.time(), git.current_hash)

def schedule_daily_update():
    print('Started scheduler for daily update...')
    schedule.every().minute.at(":03").do(update_all)

    while True:
        try:
            git.check_update()
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print('Stopped scheduler for daily update.')
            break
        except Exception as e:
            print(f'Error caught in main loop:')
            print(traceback.format_exc())
            print('Will sleep 1min.')
            time.sleep(60)

schedule_daily_update()
