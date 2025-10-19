import socket
import threading
import sys

# Konfigurasi server
HOST = '0.0.0.0'  # Listen di semua interface
PORT = 12345  # Port yang digunakan
clients = []  # List untuk menyimpan koneksi client
lock = threading.Lock()  # Lock untuk akses thread-safe ke list clients

def handle_client(client_socket):
    """Fungsi untuk menangani setiap client di thread terpisah"""
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')  # Terima pesan dari client
            if message:  # Pastikan pesan tidak kosong
                print(f"[DEBUG] Pesan diterima dari client: {message} - chat_server.py:17")  # Debug: Cetak pesan diterima
                broadcast(message, client_socket)  # Broadcast pesan
            else:
                print("[DEBUG] Pesan kosong diterima, menghentikan loop untuk client ini - chat_server.py:20")
                break  # Hentikan jika pesan kosong
    except Exception as e:
        print(f"[ERROR] Error pada client: {e} - chat_server.py:23")  # Debug: Cetak error
    finally:
        with lock:
            if client_socket in clients:  # Pastikan client masih ada sebelum dihapus
                clients.remove(client_socket)
                print("[DEBUG] Client dihapus dari list: - chat_server.py:28", client_socket.getpeername())
        try:
            client_socket.close()  # Tutup koneksi
            print("[DEBUG] Koneksi client ditutup - chat_server.py:31")
        except Exception as e:
            print(f"[ERROR] Gagal menutup socket: {e} - chat_server.py:33")

def broadcast(message, sender_socket):
    """Broadcast pesan ke semua client kecuali pengirim"""
    with lock:
        for client in clients:
            if client != sender_socket:  # Jangan kirim ke pengirim
                try:
                    client.send(message.encode('utf-8'))  # Kirim pesan
                    print(f"[DEBUG] Pesan '{message}' dibroadcast ke: {client.getpeername()} - chat_server.py:42")  # Debug: Cetak saat broadcast
                except Exception as e:
                    print(f"[ERROR] Gagal broadcast ke client: {e} - chat_server.py:44")
                    if client in clients:  # Hapus client jika error
                        clients.remove(client)
                        print("[DEBUG] Client bermasalah dihapus dari list - chat_server.py:47")

# Main server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Maksimal 5 koneksi pending
    print(f"[DEBUG] Server berjalan dan mendengarkan di port {PORT} - chat_server.py:54")
    
    while True:
        try:
            client_socket, addr = server_socket.accept()  # Terima koneksi
            print(f"[DEBUG] Client baru terhubung: {addr} - chat_server.py:59")
            with lock:
                clients.append(client_socket)  # Tambahkan client ke list
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()  # Mulai thread untuk client
        except Exception as e:
            print(f"[ERROR] Error menerima koneksi: {e} - chat_server.py:65")

if __name__ == "__main__":
    main()