import csv
import time
from datetime import datetime
import speedtest

# File untuk menyimpan hasil speedtest
csv_file = 'speedtest_log.csv'

# Buat header jika file belum ada
try:
    with open(csv_file, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'ping_ms', 'download_mbps', 'upload_mbps'])
except FileExistsError:
    pass  # File sudah ada
# Jalankan speedtest setiap 5 menit
while True:
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        ping = st.results.ping
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000      # Mbps
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Simpan ke CSV
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, round(ping, 2), round(download, 2), round(upload, 2)])

        print(f"[{timestamp}] Ping: {ping:.2f} ms | Download: {download:.2f} Mbps | Upload: {upload:.2f} Mbps")

    except Exception as e:
        print(f"Error saat speedtest: {e}")

    time.sleep(60)  # Tunggu 5 menit
