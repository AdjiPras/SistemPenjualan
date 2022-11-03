from flask import Flask, request, jsonify, render_template, json, redirect, redirect, url_for, session, make_response
from flask_mongoengine import MongoEngine #ModuleNotFoundError: No module named 'flask_mongoengine' = (venv) C:\flaskmyproject>pip install flask-mongoengine
from datetime import datetime
from models import MModel
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, ElementNotInteractableException
from time import sleep
from database import dbBrainly
from pymongo import MongoClient

# import pymongo
import datetime
# import config2
import config

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["brainlydb"]

application = Flask(__name__)
application.config['SECRET_KEY'] = 'sfh7^erw9*(%sadHGw%R'

# today = datetime.today()
model = MModel()
html_source = ''
 
app = Flask(__name__)
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'brainlydb',
#     'host': 'localhost',
#     'port': 27017
# }
# db = MongoEngine()
# db.init_app(app)

# ============================================================================================================  
# Index
@application.route('/')
def index():
	if 'data_nama' in session:
		# current_time_date = today.strftime("%B %d, %Y")
		data_nama = session['data_nama']
		return render_template('index.html', data_nama=data_nama)
	return render_template('login.html')

# login	
@application.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if model.authenticate(username, password):
			data_nama = model.getUserForSession(username)
			session['data_nama'] = data_nama
			return redirect(url_for('index'))
		msg = 'Username/Password salah.'
		return render_template('login.html', msg=msg)
	return render_template('login.html')

# Logout	
@application.route('/logout')
def logout():
	session.pop('data_nama', '')
	return redirect(url_for('index'))

# ================================ DATA BARANG ================================
@application.route('/masterbarang')
def barang():
    if 'data_nama' in session:
        data_nama = session['data_nama']
        username = data_nama[1]
        container_barang = [] 
        container_barang = model.selectBarang()
        return render_template('data_barang.html', container_barang=container_barang, data_nama=data_nama)
    return render_template('login.html')

@application.route('/insert_barang', methods=['GET', 'POST'])
def insert_barang():
	if 'data_nama' in session:
		if request.method == 'POST':
			kode_barang = request.form['kode_barang']
			nama_barang = request.form['nama_barang']
			jenis_barang = request.form['jenis_barang']
			data_b = (kode_barang, nama_barang, jenis_barang)
			model.insertBarang(data_b)
			return redirect(url_for('barang'))
		else:
			data_nama = session['data_nama']
			return render_template('insert_barang.html', data_nama=data_nama)
	return render_template('login.html')

@application.route('/update_bg', methods=['GET', 'POST'])
def update_bg():
	if 'data_nama' in session:
		kode_barang = request.form['kode_barang']
		nama_barang = request.form['nama_barang']
		jenis_barang = request.form['jenis_barang']
		data_bg = (kode_barang, nama_barang, jenis_barang)
		model.updateBarang(data_bg)
		return redirect(url_for('barang'))
	return render_template('login.html')

@application.route('/update_barang/<kode_barang>')
def update_barang(kode_barang):
	if 'data_nama' in session:
		data_bg = model.getBarangbyNo(kode_barang)
		data_nama = session['data_nama']
		return render_template('edit_barang.html', data_bg=data_bg, data_nama=data_nama)
	return redirect(url_for('login'))

@application.route('/delete_barang/<kode_barang>')
def delete_barang(kode_barang):
	if 'data_nama' in session:
		model.deleteBarang(kode_barang)
		return redirect(url_for('barang'))
	return render_template('login.html')


# ================================ DATA BARANG ================================
@application.route('/supplier')
def supplier():
    if 'data_nama' in session:
        data_nama = session['data_nama']
        username = data_nama[1]
        container_supplier = [] 
        container_supplier = model.selectSupplier()
        return render_template('data_supplier.html', container_supplier=container_supplier, data_nama=data_nama)
    return render_template('login.html')

@application.route('/insert_supplier', methods=['GET', 'POST'])
def insert_supplier():
	if 'data_nama' in session:
		if request.method == 'POST':
			kode_supplier = request.form['kode_supplier']
			nama_supplier = request.form['nama_supplier']
			alamat = request.form['alamat']
			no_telepon = request.form['no_telepon']
			data_s = (kode_supplier, nama_supplier, alamat, no_telepon)
			model.insertSupplier(data_s)
			return redirect(url_for('supplier'))
		else:
			data_nama = session['data_nama']
			return render_template('insert_supplier.html', data_nama=data_nama)
	return render_template('login.html')

# @application.route('/update_bg', methods=['GET', 'POST'])
# def update_bg():
# 	if 'data_nama' in session:
# 		kode_barang = request.form['kode_barang']
# 		nama_barang = request.form['nama_barang']
# 		jenis_barang = request.form['jenis_barang']
# 		data_bg = (kode_barang, nama_barang, jenis_barang)
# 		model.updateBarang(data_bg)
# 		return redirect(url_for('barang'))
# 	return render_template('form_login.html')

# @application.route('/update_barang/<kode_barang>')
# def update_barang(kode_barang):
# 	if 'data_nama' in session:
# 		data_bg = model.getBarangbyNo(kode_barang)
# 		data_nama = session['data_nama']
# 		return render_template('edit_barang.html', data_bg=data_bg, data_nama=data_nama)
# 	return redirect(url_for('login'))

@application.route('/delete_supplier/<kode_supplier>')
def delete_supplier(kode_supplier):
	if 'data_nama' in session:
		model.deleteSupplier(kode_supplier)
		return redirect(url_for('supplier'))
	return render_template('login.html')
    
# ======================================= pengguna ================================

@application.route('/pengguna')
def pengguna():
    if 'data_nama' in session:
        data_nama = session['data_nama']
        username = data_nama[1]
        container = [] 
        container = model.selectPengguna()
        return render_template('pengguna.html', container=container, data_nama=data_nama)
    return render_template('login.html')

# menambahkan data pengguna.
@application.route('/insert_pengguna', methods=['GET', 'POST'])
def insert_pengguna():
	if 'data_nama' in session:
		if request.method == 'POST':
			pengguna_id = request.form['pengguna_id']
			username = request.form['username']
			password = request.form['password']
			tipe_pengguna = request.form['tipe_pengguna']
			pengguna_nama = request.form['pengguna_nama']
			data_p = (pengguna_id, username, password, tipe_pengguna, pengguna_nama)
			model.insertPengguna(data_p)
			return redirect(url_for('pengguna'))
		else:
			data_nama = session['data_nama']
			return render_template('insert_pengguna.html', data_nama=data_nama)
	return render_template('login.html')

# edit / update data pengguna.
@application.route('/update_pg', methods=['GET', 'POST'])
def update_pg():
	if 'data_nama' in session:
		pengguna_id = request.form['pengguna_id']
		username = request.form['username']
		password = request.form['password']
		tipe_pengguna = request.form['tipe_pengguna']
		pengguna_nama = request.form['pengguna_nama']
		data_pg = (username, password, tipe_pengguna, pengguna_nama, pengguna_id)
		model.updatePengguna(data_pg)
		return redirect(url_for('pengguna'))
	return render_template('login.html')

@application.route('/update_pengguna/<pengguna_id>')
def update_pengguna(pengguna_id):
	if 'data_nama' in session:
		data_pg = model.getUserbyNo(pengguna_id)
		data_nama = session['data_nama']
		return render_template('edit_pengguna.html', data_pg=data_pg, data_nama=data_nama)
	return redirect(url_for('login')) 

# menghapus data pengguna.
@application.route('/delete_pengguna/<pengguna_id>')
def delete_pengguna(pengguna_id):
	if 'data_nama' in session:
		model.deletePengguna(pengguna_id)
		return redirect(url_for('pengguna'))
	return render_template('login.html')

# ======================================= menampilkan laporan ================================

@application.route('/laporan')
def laporan():
    if 'data_nama' in session:
        container_lp = []
        container_lp = model.selectLaporan()
        data_nama = session['data_nama']
        return render_template('laporan.html', container_lp=container_lp, data_nama=data_nama)
    return render_template('login.html')

# tambah laporan.
@application.route('/insert_laporan', methods=['GET', 'POST'])
def insert_laporan():
    if 'data_nama' in session:
        if request.method == 'POST':
            no = request.form['no']
            username = request.form['username']
            mata_pelajaran = request.form['mata_pelajaran']
            tanggal_lapor = datetime.datetime.now()
            tanggal_proses = 0
            status = None
            data_lp = (no, username, mata_pelajaran, tanggal_lapor, tanggal_proses, status)
            model.insertLaporan(data_lp)
            return redirect(url_for('laporan'))
        else:
            data_nama = session['data_nama']
            return render_template('tambah_laporan.html', data_nama=data_nama)
    return render_template('login.html')

# proses edit / update data laporan.
@application.route('/update_lp', methods=['GET', 'POST'])
def update_lp():
    if 'data_nama' in session:
        pengguna_id = request.form['pengguna_id']
        username = request.form['username']
        mata_pelajaran = request.form['mata_pelajaran']
        tanggal_lapor = datetime.datetime.now()
        tanggal_proses = datetime.datetime.now()
        status = request.form['status']
        data_lp = (username, mata_pelajaran, tanggal_lapor, tanggal_proses, status, pengguna_id)
        model.updateLaporan(data_lp)
        return redirect(url_for('laporan'))
    return render_template('login.html')

# edit / update data laporan.
@application.route('/update_laporan/<no>')
def update_laporan(no):
    if 'data_nama' in session:
        data_lp = model.getLaporbyNo(no)
        data_nama = session['data_nama']
        return render_template('edit_laporan.html', data_lp=data_lp, data_nama=data_nama)
    return render_template('login.html')

if __name__ == '__main__':
    application.run(debug=True)