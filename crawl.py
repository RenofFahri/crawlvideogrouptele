import pickle
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputMessagesFilterVideo
from telethon.tl import types
import os

# Memuat atau membuat objek data
if os.path.exists('data.pkl'):
    with open('data.pkl', 'rb') as f:
        data = pickle.load(f)
else:
    data = {
        'api_id': input('Masukkan API ID: '),
        'api_hash': input('Masukkan API Hash: '),
    }

    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)

# Inisialisasi client Telegram dengan data
client = TelegramClient('session_name', data['api_id'], data['api_hash'])

def download_videos():
    # Menghubungkan ke server Telegram
    client.connect()

    # Meminta input dari pengguna
    data['phone_number'] = input('Masukkan nomor telepon: ')
    data['group_username'] = input('Masukkan username grup: ')
    data['download_path'] = input('Masukkan path untuk menyimpan video (kosongkan untuk path default): ') or 'videos/'
    data['limit'] = int(input('Masukkan jumlah pesan yang ingin diambil: '))

    # Mendapatkan nomor telepon dari pengguna
    if not client.is_user_authorized():
        client.send_code_request(data['phone_number'])
        client.sign_in(data['phone_number'], input('Masukkan kode yang dikirim ke Telegram: '))

    # Mengambil semua pesan yang mengandung video dari grup
    entity = client.get_entity(data['group_username'])
    messages = client(GetHistoryRequest(
        peer=entity,
        limit=data['limit'],  # Mengambil jumlah pesan sesuai limit
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0,
        offset_peer=entity
    ))

    # Membuat direktori jika belum ada
    if not os.path.exists(data['download_path']):
        os.makedirs(data['download_path'])

    # Mengambil video dari setiap pesan
    for message in messages.messages:
        if message.media and isinstance(message.media, types.MessageMediaVideo):
            video = message.media.video
            video_path = client.download_media(video, data['download_path'])
            print(f"Video {video.id} diunduh ke: {video_path}")

    # Menyimpan objek data
    with open('data.pkl', 'wb') as f:
        pickle.dump(data, f)

# Menjalankan fungsi download_videos
if __name__ == '__main__':
    download_videos()
