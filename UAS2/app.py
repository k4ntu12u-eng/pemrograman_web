from flask import Flask, render_template, request, redirect, url_for, session
from utils import konversi_nilai_ke_label, konversi_label_ke_bobot
import os

app = Flask(__name__)
app.secret_key = "kunci_rahasia_anda" 

@app.route('/')
def index():
    if 'data' not in session:
        session['data'] = {
            "nama": "", "nim": "",
            "list_matkul": [], "list_sks": [], "list_nilai": []
        }
    return render_template('index.html', data=session['data'], ip=hitung_ip())

@app.route('/update_biodata', methods=['POST'])
def update_biodata():
    data = session['data']
    data['nama'] = request.form.get('nama')
    data['nim'] = request.form.get('nim')
    session['data'] = data
    return redirect(url_for('index'))

@app.route('/tambah_nilai', methods=['POST'])
def tambah_nilai():
    data = session['data']
    matkul = request.form.get('matkul')
    sks = int(request.form.get('sks'))
    nilai = float(request.form.get('nilai'))
    
    data['list_matkul'].append(matkul)
    data['list_sks'].append(sks)
    data['list_nilai'].append(nilai)
    
    session['data'] = data
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.pop('data', None)
    return redirect(url_for('index'))

def hitung_ip():
    data = session.get('data')
    if not data or not data['list_sks']:
        return 0
    
    total_sks = sum(data['list_sks'])
    total_poin = 0
    for i in range(len(data['list_sks'])):
        label = konversi_nilai_ke_label(data['list_nilai'][i])
        bobot = konversi_label_ke_bobot(label)
        total_poin += (bobot * data['list_sks'][i])
    
    return round(total_poin / total_sks, 2) if total_sks > 0 else 0

if __name__ == '__main__':
    app.run(debug=True)