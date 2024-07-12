import mysql.connector

def buat_koneksi():
  koneksi_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password ="",
    database="crud"
  )
  if koneksi_db.is_connected():
    print("Koneksi Berhasil")
  else:
    print("Koneksi Gagal")
  return koneksi_db
if __name__ == "__main__":
  buat_koneksi()