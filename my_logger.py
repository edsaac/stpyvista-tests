from time import sleep
from datetime import datetime
from os import system

LOGFILE = "my_log.txt"
system(f"touch {LOGFILE}")

while True:
    system(f"""echo "{datetime.now()}" >> {LOGFILE}""")
    system(f"ps aux --sort=-%mem >> {LOGFILE}")
    system(f"""echo "----------------" >> {LOGFILE}""")

    sleep(10*60)