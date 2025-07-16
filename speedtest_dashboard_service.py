import subprocess
import threading
import time

def run_speedtest():
    while True:
        subprocess.run(["python", "auto_speedtest.py"])
        time.sleep(60)  # 5 menit

def run_dashboard():
    subprocess.run(["streamlit", "run", "dashboard_speedtest_full.py"])

# Jalankan speedtest di thread terpisah
speedtest_thread = threading.Thread(target=run_speedtest)
speedtest_thread.daemon = True
speedtest_thread.start()

# Jalankan dashboard
run_dashboard()
