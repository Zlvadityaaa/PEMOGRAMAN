import socket
import threading
import sys

# Konfigurasi client
SERVER_HOST = 'localhost'  # IP server, ganti jika di komputer lain
SERVER_PORT = 12345  # Port server

def receive_messages(client_socket):
    """Thread untuk menerima pesan dari server"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  # Terima pesan
            if message:
                print(f"Pesan dari server: {message} - chat_client.py:15")  # Cetak pesan yang diterima
            else:
                print("[DEBUG] Pesan kosong diterima dari server - chat_client.py:17")
                break
        except Exception as e:
            print(f"[ERROR] Koneksi terputus: {e} - chat_client.py:20")
            sys.exit()  # Keluar jika error

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))  # Terhubung ke server
        print("[DEBUG] Terhubung ke server. Mulai chatting... - chat_client.py:27")
        
        # Mulai thread untuk menerima pesan
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()
        
        while True:
            message = input()  # Input pesan dari user
            if message.lower() == 'quit':  # Opsional: Keluar dengan mengetik 'quit'
                break
            try:
                client_socket.send(message.encode('utf-8'))  # Kirim pesan ke server
                print(f"[DEBUG] Pesan dikirim: {message} - chat_client.py:39")  # Debug: Cetak saat mengirim
            except Exception as e:
                print(f"[ERROR] Gagal mengirim pesan: {e} - chat_client.py:41")
                break
    except Exception as e:
        print(f"[ERROR] Error koneksi: {e} - chat_client.py:44")
    finally:
        client_socket.close()  # Tutup koneksi
        print("[DEBUG] Koneksi client ditutup - chat_client.py:47")
        sys.exit()

if __name__ == "__main__":
    main()