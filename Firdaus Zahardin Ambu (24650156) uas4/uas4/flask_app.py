from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import socket
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'presensi_murni_2026'

# --- DATA STORAGE (IN-MEMORY) ---
# Menggunakan struktur yang sedikit lebih rapi untuk memudahkan pencarian
users = [{"id": 1, "username": "admin", "password": "123", "role": "Admin", "nim": "-"}]
data_pertemuan = []
kehadiran = {} 

# --- UTILS ---
def get_ip():
    """Mengambil IP Local mesin untuk keperluan tampilan di home."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def login_required(role=None):
    """Fungsi pembantu (opsional) untuk validasi session secara cepat."""
    user_role = session.get('user_role')
    if not user_role:
        return False
    if role and user_role != role:
        return False
    return True

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('home.html', ip=get_ip())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        
        # Mencari user dengan list comprehension yang lebih bersih
        user = next((item for item in users if item['username'] == u and item['password'] == p), None)
        
        if user:
            session.update({
                'user_login': user['username'],
                'user_role': user['role'],
                'nim': user.get('nim', '-')
            })
            
            # Mapping redirect berdasarkan role
            redirect_map = {
                'Admin': 'admin_page',
                'Dosen': 'dashboard_dosen',
                'Mahasiswa': 'dashboard_mahasiswa'
            }
            return redirect(url_for(redirect_map.get(user['role'], 'login')))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- MODUL ADMIN ---

@app.route('/Admin')
def admin_page():
    if not login_required('Admin'): return redirect(url_for('login'))
    # Filter untuk tidak menampilkan admin utama di daftar
    list_users = [u for u in users if u['id'] != 1]
    return render_template('tampilan_admin.html', users=list_users)

@app.route('/add_user', methods=['POST'])
def add_user():
    if not login_required('Admin'): return redirect(url_for('login'))
    
    u = request.form.get('username')
    p = request.form.get('password')
    r = request.form.get('role')
    n = request.form.get('nim', '-')

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
    if not login_required('Admin'): return redirect(url_for('login'))
    global users
    users = [u for u in users if u['id'] != user_id]
    return redirect(url_for('admin_page'))

# --- MODUL DOSEN ---

@app.route('/dashboard/dosen')
def dashboard_dosen():
    if not login_required('Dosen'): return redirect(url_for('login'))
    return render_template('dashboard_dosen.html')

@app.route('/dosen/pertemuan', defaults={'id_p': None})
@app.route('/dosen/pertemuan/<int:id_p>')
def dosen_pertemuan(id_p):
    if not login_required('Dosen'): return redirect(url_for('login'))
    
    p_detail = next((p for p in data_pertemuan if p['id'] == id_p), None)
    list_hadir = kehadiran.get(id_p, []) if id_p else []
    
    return render_template('pertemuan_dosen.html', 
                           pertemuan=data_pertemuan, 
                           p_detail=p_detail, 
                           list_hadir=list_hadir)

@app.route('/dosen/daftar_mahasiswa')
def dosen_daftar_mahasiswa():
    if not login_required('Dosen'): return redirect(url_for('login'))
    list_mhs = [u for u in users if u['role'] == 'Mahasiswa']
    return render_template('daftar_mahasiswa_dosen.html', mahasiswa=list_mhs)

@app.route('/dosen/tambah', methods=['POST'])
def tambah_pertemuan():
    if not login_required('Dosen'): return redirect(url_for('login'))
    
    new_id = data_pertemuan[-1]['id'] + 1 if data_pertemuan else 1
    data_pertemuan.append({
        "id": new_id, 
        "nama": request.form.get('nama'), 
        "tanggal": request.form.get('tanggal'), 
        "mulai": request.form.get('mulai'),
        "selesai": request.form.get('selesai')
    })
    return redirect(url_for('dosen_pertemuan'))

@app.route('/dosen/hapus_semua')
def hapus_semua():
    if not login_required('Dosen'): return redirect(url_for('login'))
    data_pertemuan.clear()
    kehadiran.clear()
    return redirect(url_for('dosen_pertemuan'))

@app.route('/dosen/submit_absen', methods=['POST'])
def submit_absen():
    # API ini biasanya dipanggil oleh scanner/sistem otomatis
    data = request.json
    id_p = int(data.get('id_p'))
    info_mhs = data.get('info_mhs')
    
    if id_p not in kehadiran: 
        kehadiran[id_p] = []
    
    # Cek duplikasi absen
    if any(h['info'] == info_mhs for h in kehadiran[id_p]):
        return jsonify({"status": "error", "message": "Mahasiswa sudah absen!"})
    
    kehadiran[id_p].append({
        "info": info_mhs, 
        "waktu": datetime.now().strftime("%H:%M:%S")
    })
    return jsonify({"status": "success"})

# --- MODUL MAHASISWA ---

@app.route('/dashboard/mahasiswa')
def dashboard_mahasiswa():
    if not login_required('Mahasiswa'): return redirect(url_for('login'))
    return render_template('dashboard_mahasiswa.html')

@app.route('/mahasiswa/pertemuan', defaults={'id_p': None})
@app.route('/mahasiswa/pertemuan/<int:id_p>')
def mahasiswa_pertemuan(id_p):
    if not login_required('Mahasiswa'): return redirect(url_for('login'))
    
    p_detail = next((p for p in data_pertemuan if p['id'] == id_p), None)
    return render_template('pertemuan_mahasiswa.html', 
                           pertemuan=data_pertemuan, 
                           p_detail=p_detail)

if __name__ == '__main__':
    # Flask menjalankan server pada port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)