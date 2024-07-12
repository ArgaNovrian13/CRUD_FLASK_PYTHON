from flask import Flask, redirect, render_template, request, url_for, flash, session
from koneksi import buat_koneksi
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Fungsi bantuan untuk membuat koneksi database
def ambil_koneksi_database():
    if 'username' in session:
        koneksi = buat_koneksi()
        return koneksi
    else:
        return None

# Fungsi untuk menutup koneksi database
def tutup_koneksi_database(koneksi):
    if koneksi is not None:
        koneksi.close()

# Dekorator untuk mengecek login
def cek_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# @app.route("/getstarted")
# def get_started():
#     return render_template("getstarted.html")
@app.route("/")
@cek_login
def index():
    koneksi = ambil_koneksi_database()
    if koneksi:
        cursor = koneksi.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        cursor.execute("SELECT id FROM admin WHERE nama = %s", (session['username'],))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            session['user_id'] = user_id
            koneksi.close()
            return render_template("index.html", items=items, username=session['username'])
        else:
            koneksi.close()
            flash("User tidak ditemukan", "danger")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        koneksi = buat_koneksi()
        cursor = koneksi.cursor()
        cursor.execute("SELECT * FROM admin WHERE nama = %s AND sandi = %s", (username, password))
        admin = cursor.fetchone()
        koneksi.close()
        
        if admin:
            session['username'] = username
            flash(f"Selamat datang, {username}!", 'success')
            return redirect(url_for("index"))
        else:
            flash("Username atau password Anda salah", 'danger')
    
    return render_template("login.html")

@app.route("/profil/<int:id>", methods=['GET', 'POST'])
@cek_login
def profil(id):
    koneksi = ambil_koneksi_database()
    if koneksi:
        cursor = koneksi.cursor()
        cursor.execute("SELECT * FROM admin WHERE id = %s", (id,))
        items = cursor.fetchone()
        koneksi.close()

        if items is None:
            flash("Profil tidak ditemukan", "danger")
            return redirect(url_for('index'))

        if request.method == 'POST':
            nama = request.form['nama']
            sandi = request.form['password']
            koneksi = buat_koneksi()
            cursor = koneksi.cursor()
            cursor.execute("UPDATE admin SET nama = %s, sandi = %s WHERE id = %s", (nama, sandi, id))
            koneksi.commit()
            koneksi.close()
            return redirect(url_for('index'))

        return render_template("profil.html", items=items, id=id)
    else:
        return redirect(url_for("login"))

@app.route("/add", methods=['GET', 'POST'])
@cek_login
def add():
    if request.method == 'POST':
        koneksi = buat_koneksi()
        cursor = koneksi.cursor()
        name = request.form['name']
        price = request.form['price']
        cursor.execute("INSERT INTO items (name, price) VALUES (%s, %s)", (name, price))
        koneksi.commit()
        koneksi.close()
        return redirect(url_for('index'))
    return render_template("add.html")
@app.route("/detail/<int:id>", methods=['GET','POST'])
@cek_login
def detail(id):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
    item = cursor.fetchone()
    koneksi.close()
    
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        koneksi = buat_koneksi()
        cursor = koneksi.cursor()
        cursor.execute("UPDATE items SET name = %s, price = %s WHERE id = %s", (name, price, id))
        koneksi.commit()
        koneksi.close()
        return redirect(url_for('index'))
    
    return render_template("detail.html", item=item)
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
@cek_login
def edit(id):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
    item = cursor.fetchone()
    koneksi.close()
    
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        koneksi = buat_koneksi()
        cursor = koneksi.cursor()
        cursor.execute("UPDATE items SET name = %s, price = %s WHERE id = %s", (name, price, id))
        koneksi.commit()
        koneksi.close()
        return redirect(url_for('index'))
    
    return render_template("edit.html", item=item)

@app.route("/delete/<int:id>", methods=['GET', 'POST'])
@cek_login
def delete(id):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (id,))
    koneksi.commit()
    koneksi.close()
    return redirect(url_for('index'))

@app.route("/search", methods=['POST'])
@cek_login
def search():
    keyword = request.form['keyword']
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    query = "SELECT * FROM items WHERE name LIKE %s OR price LIKE %s"
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
    items = cursor.fetchall()
    koneksi.close()
    return render_template("items.html", items=items)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
