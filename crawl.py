from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputMessagesFilterVideo
from telethon.tl import types
import os
import sys
import time

# Inisialisasi client Telegram
client = TelegramClient('session_name', None, None)

def download_videos():
    # Menampilkan tulisan "Loading..." dengan animasi titik-titik
    sys.stdout.write("Connecting to Telegram server ")
    sys.stdout.flush()
    while not client.is_connected():
        for _ in range(3):
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write("\b\b\b   \b\b\b")
        sys.stdout.flush()

    # Menghubungkan ke server Telegram
    client.connect()
    print("\nConnected to Telegram server")

    # Meminta input dari pengguna
    api_id = input('Masukkan API ID: ')
    api_hash = input('Masukkan API Hash: ')
    phone_number = input('Masukkan nomor telepon: ')
    group_username = input('Masukkan username grup: ')
    download_path = input('Masukkan path untuk menyimpan video (kosongkan untuk path default): ') or 'videos/'
    limit = int(input('Masukkan jumlah pesan yang ingin diambil: '))

    # Inisialisasi client Telegram
    client = TelegramClient('session_name', api_id, api_hash)

    # Menghubungkan ke server Telegram
    client.connect()

    # Mendapatkan nomor telepon dari pengguna
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input('Masukkan kode yang dikirim ke Telegram: '))

    # Mengambil semua pesan yang mengandung video dari grup
    entity = client.get_entity(group_username)
    messages = client(GetHistoryRequest(
        peer=entity,
        limit=limit,  # Mengambil jumlah pesan sesuai limit
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0,
        offset_peer=entity
    ))

    # Membuat direktori jika belum ada
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Mengambil video dari setiap pesan
    for message in messages.messages:
        if message.media and isinstance(message.media, types.MessageMediaVideo):
            video = message.media.video
            video_path = client.download_media(video, download_path)
            print(f"Video {video.id} diunduh ke: {video_path}")

# Menjalankan fungsi download_videos
if __name__ == '__main__':
    download_videos()
    
