from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import socket
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'presensi_murni_2026'

# DATABASE MEMORI
# Admin default untuk login awal
users = [{"id": 1, "username": "admin", "password": "123", "role": "Admin", "nim": "-"}]
data_pertemuan = []
kehadiran = {} 

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/')
def home():
    return render_template('home.html', ip=get_ip())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form.get('username'), request.form.get('password')
        found = next((user for user in users if user['username'] == u and user['password'] == p), None)
        if found:
            session.update({'user_login': found['username'], 'user_role': found['role'], 'nim': found.get('nim', '-')})
            if found['role'] == 'Admin': return redirect(url_for('admin_page'))
            if found['role'] == 'Dosen': return redirect(url_for('dashboard_dosen'))
            if found['role'] == 'Mahasiswa': return redirect(url_for('dashboard_mahasiswa'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- BAGIAN ADMIN ---
@app.route('/Admin')
def admin_page():
    if session.get('user_role') != 'Admin': return redirect(url_for('login'))
    display_users = [u for u in users if u['id'] != 1]
    return render_template('tampilan_admin.html', users=display_users)

@app.route('/add_user', methods=['POST'])
def add_user():
    u, p, r, n = request.form.get('username'), request.form.get('password'), request.form.get('role'), request.form.get('nim', '-')
    # Validasi Nama Ganda
    if any(user['username'] == u for user in users):
        session['error_admin'] = "Sudah ada datanya yang dimasukan!"
        return redirect(url_for('admin_page'))
    if u and p:
        new_id = users[-1]['id'] + 1 if users else 1
        users.append({"id": new_id, "username": u, "password": p, "role": r, "nim": n})
        session.pop('error_admin', None)
    return redirect(url_for('admin_page'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return redirect(url_for('admin_page'))

# --- BAGIAN DOSEN ---
@app.route('/dashboard/dosen')
def dashboard_dosen():
    if session.get('user_role') != 'Dosen': return redirect(url_for('login'))
    return render_template('dashboard_dosen.html')

@app.route('/dosen/pertemuan')
@app.route('/dosen/pertemuan/<int:id_p>')
def dosen_pertemuan(id_p=None):
    if session.get('user_role') != 'Dosen': return redirect(url_for('login'))
    p_detail = next((p for p in data_pertemuan if p['id'] == id_p), None)
    list_hadir = kehadiran.get(id_p, []) if id_p else []
    return render_template('pertemuan_dosen.html', pertemuan=data_pertemuan, p_detail=p_detail, list_hadir=list_hadir)

@app.route('/dosen/daftar_mahasiswa')
def dosen_daftar_mahasiswa():
    if session.get('user_role') != 'Dosen': return redirect(url_for('login'))
    # Mengambil list user dengan role Mahasiswa untuk ditampilkan
    list_mhs = [u for u in users if u['role'] == 'Mahasiswa']
    return render_template('daftar_mahasiswa_dosen.html', mahasiswa=list_mhs)

@app.route('/dosen/tambah', methods=['POST'])
def tambah_pertemuan():
    new_id = data_pertemuan[-1]['id'] + 1 if data_pertemuan else 1
    data_pertemuan.append({
        "id": new_id, "nama": request.form.get('nama'), 
        "tanggal": request.form.get('tanggal'), "mulai": request.form.get('mulai'),
        "selesai": request.form.get('selesai')
    })
    return redirect(url_for('dosen_pertemuan'))

@app.route('/dosen/hapus_semua')
def hapus_semua():
    global data_pertemuan, kehadiran
    data_pertemuan.clear()
    kehadiran.clear()
    return redirect(url_for('dosen_pertemuan'))

@app.route('/dosen/submit_absen', methods=['POST'])
def submit_absen():
    data = request.json
    id_p, info_mhs = int(data.get('id_p')), data.get('info_mhs')
    if id_p not in kehadiran: kehadiran[id_p] = []
    if any(h['info'] == info_mhs for h in kehadiran[id_p]):
        return jsonify({"status": "error", "message": "Mahasiswa sudah absen!"})
    kehadiran[id_p].append({"info": info_mhs, "waktu": datetime.now().strftime("%H:%M:%S")})
    return jsonify({"status": "success"})

# --- BAGIAN MAHASISWA ---
@app.route('/dashboard/mahasiswa')
def dashboard_mahasiswa():
    if session.get('user_role') != 'Mahasiswa': return redirect(url_for('login'))
    return render_template('dashboard_mahasiswa.html')

@app.route('/mahasiswa/pertemuan')
@app.route('/mahasiswa/pertemuan/<int:id_p>')
def mahasiswa_pertemuan(id_p=None):
    if session.get('user_role') != 'Mahasiswa': return redirect(url_for('login'))
    p_detail = next((p for p in data_pertemuan if p['id'] == id_p), None)
    return render_template('pertemuan_mahasiswa.html', pertemuan=data_pertemuan, p_detail=p_detail)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)