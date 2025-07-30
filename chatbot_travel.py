# --------------------------------#
# Chatbot Final Test

# Membuat bot chat dengan sistem :
# 1. Bot bisa menjawab pertanyaan dari user dengang menggunakan datachat di database
# 2. Bot harus bisa menganalisis budget yang dimiliki oleh user, dan bot akan mencarikan harga wisata yang cocok dengan budget user

# --------------------------------#


# --------------------------------#
# Yang saya tambahin adalah :
# 1. Bot bisa memahami pertanyaan yang ada di database meskipun pertanyaan user tidak 100% sama dengan yang ada di database
# --------------------------------#


# --------------------------------#
#  Untuk Struktur Database nya saya SS aja kalo mau lihat, saya kirim via imgur aja
#  https://imgur.com/a/XJgnds1
# --------------------------------#



# Import Library
import mysql.connector # Library unutk sambungin python dengan mysql
import re # Library untuk deteksi angka dari string

# Koneksi buat ke database mysql 
connect = mysql.connector.connect (
    host="localhost",
    user="root",
    password="",
    database="travel_bot"
)

# Untuk perantara python dengan mysql
cursor = connect.cursor()


# Menetapkan bot saat awal menjadi false agar bot off
bot = False

# Keterangan
print('''
    Bot Travel Siap Digunakan :D
    Ketik On/Off untuk mengaktifkan Bot/Mematikan bot
    Ketik /q untuk keluar
    Ketik /help untuk melihat daftar pertanyaan
''')

# Selama bot dalam keadaan true, maka akan menjalan kan code di bawah
while True: 
    user_input = input("Anda : ").lower()
    
    # Fungsi On/Off/Exit
        # Fungsi On Bot
    if user_input == "on":
        if bot:
            print("Bot Sudah On")
        else :
            bot = True
            print("Bot Telah Diaktifkan")
            
        # Fungsi Off Bot
    elif user_input == "off":
        if bot :
            bot = False
            print("Bot Telah Di Matikan")
        else :
            print("Bot Sudah Mati")
        
        # Fungsi Exit Bot
    elif user_input == "/q" :
        break

        # Fungsi Help
    elif user_input == "/help" :
        # Query
        cursor.execute("SELECT pertanyaan FROM chatbot")
        daftar_pertanyaan = cursor.fetchall()
        
        # Fungsi Untuk menampilkan daftar pertanyaan 
        if daftar_pertanyaan:
            print("Berikut Daftar Pertanyaan Yang Bisa Saya Jawab ^_^")
            # Ngambil dari kolom pertanyaan
            for i, row in enumerate(daftar_pertanyaan, 1):
                print(f" {i}. {row[0]}")    

    
    
    # -----------------------------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------------------------#
    
    
    
    # Kalau bot aktif, bisa proses code di bawah
    elif bot:
        
        # Cek kalau input berisi angka (budget)
        temuan_harga = re.search(r'\b(\d{2,})[.,]?\d*\b', user_input.replace('.', '').replace(',', ''))
        if temuan_harga:
            budget = int(temuan_harga.group(1))

            # Query buat nge ambil paket yang sesuai
            cursor.execute("SELECT nama_paket, tempat, harga, kontak_sales FROM paket_wisata WHERE harga <= %s", (budget,))
            hasil = cursor.fetchall()

            # kondisi kalo uang cukup buat salah satu paket wisata
            if hasil:   
                print("Evangeline : Ini pilihan paket yang cocok sama budget kamu : ")
                for i, row in enumerate(hasil, 1):
                    print(f"  Opsi {i}: {row[0]} ke {row[1]} - Rp{row[2]:,} (Hubungi : {row[3]})") # 0 = nama_paket, 1 = tempat , 2 = harga, 3 = No tlp sales

            else:
                print("Evangeline : Budget kamu belum cukup untuk paket yang tersedia, coba tanya langsung ke sales ya.")
        
        else:
            # Fungsi untuk Kalau bukan angka/budget, maka akan menjawab pertanyaan yang di ambil dari database datachat
            # Pake LIKE untuk kalo pertanyaan user ada yang sama dengan pertanyaan di data base, jadi pertanyaan user gak harus 100% sama dengan pertanyaan yang ada di data base (Sorry kalo ribet penjelasan nya :D)
            cursor.execute("SELECT jawaban FROM chatbot WHERE %s LIKE CONCAT('%%', pertanyaan, '%%') LIMIT 1", (user_input,))
            hasil = cursor.fetchone()
            if hasil:
                print(f"Evangeline : {hasil[0]}")
            else:
                print("Evangeline : Maaf, saya belum tahu jawaban dari pertanyaan itu.")

    else:
        print("Bot sedang mati, ketik 'on' untuk menyalakannya.")



    # -----------------------------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------------------------#
    # -----------------------------------------------------------------------------------------------------------------------------------#


# Tutup koneksi dari mysql
cursor.close()
connect.close()