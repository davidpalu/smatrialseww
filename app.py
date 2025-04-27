from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Create database and materials table if not exists
def init_db():
    conn = sqlite3.connect('study.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            unit TEXT NOT NULL,
            material_link TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect('study.db')

@app.route('/', methods=['GET', 'POST'])
def home():
    con = get_db()
    cur = con.cursor()
    # Get all unique subjects and units for dropdowns
    cur.execute("SELECT DISTINCT subject FROM materials")
    subjects = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT unit FROM materials")
    units = [row[0] for row in cur.fetchall()]
    materials = []
    selected_subject = selected_unit = None
    
    if request.method == 'POST':
        selected_subject = request.form.get('subject')
        selected_unit = request.form.get('unit')
        if selected_subject and selected_unit:
            cur.execute("SELECT * FROM materials WHERE subject=? AND unit=?", (selected_subject, selected_unit))
            materials = cur.fetchall()
    con.close()
    return render_template('home.html', subjects=subjects, units=units, materials=materials, selected_subject=selected_subject, selected_unit=selected_unit)
def view_subject(subject_id):
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT name FROM subjects WHERE id=?", (subject_id,))
    subject = cur.fetchone()
    cur.execute("SELECT * FROM materials WHERE subject_id=?", (subject_id,))
    materials = cur.fetchall()
    con.close()
    return render_template('subject.html', subject=subject, materials=materials)

from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'pdf', 'ppt', 'pptx', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    con = get_db()
    cur = con.cursor()
    # Fetch unique subjects and units for datalists
    cur.execute("SELECT DISTINCT subject FROM materials")
    subjects = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT unit FROM materials")
    units = [row[0] for row in cur.fetchall()]
    con.close()

    if request.method == 'POST':
        subject = request.form['subject']
        unit = request.form['unit']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            material_link = f'/uploads/{filename}'
            con = get_db()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO materials (subject, unit, material_link) VALUES (?, ?, ?)",
                (subject, unit, material_link)
            )
            con.commit()
            con.close()
            return redirect('/')
    return render_template('upload.html', subjects=subjects, units=units)


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
