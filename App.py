from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

app = Flask(__name__)


app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'atsbbdd'
user = {}
mysql = MySQL(app)
app.secret_key = 'mysecretkey'


@app.route('/', methods = ['GET', 'POST'])
def login():
    global user
    error = ''
    
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s AND password = %s', (usuario, password,))
        user = cursor.fetchone()
       
        if user:
            session['loggedin'] = True
            return redirect(url_for('Index'))       
        else:  
            error = '¡Usuario/contraseña Incorrecto!'

    if session.get('loggedin') == True:
        return redirect(url_for('Index'))
    else:
        return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    global user
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('usuario', None)
    user = {}
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
   
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
        account = cursor.fetchone()
        
        if account:
            error = '¡El usuario ya existe!'
        else:                     
            cursor.execute('INSERT INTO usuarios VALUES (null, %s, %s, %s, %s)', (nombre, apellido, usuario, password,))
            mysql.connection.commit()
            msg = '¡Usuario registrado correctamente!'
            return render_template('login.html', msg = msg)
    return render_template('register.html', error = error)

@app.route('/index')
def Index():
    if len(user) == 0:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estados')
    estados = cur.fetchall()
    cur.execute('SELECT * FROM candidatos')
    candidatos = cur.fetchall()
    return render_template('index.html', candidatos = candidatos, estados = estados)

@app.route('/add-contact', methods = ['GET', 'POST'])    
def add_contact():
    global user
    if len(user) == 0:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('add-contact.html')
    elif request.method == 'POST':
       nombrecandidato = request.form['nombrecandidato']
       apellidocandidato = request.form['apellidocandidato']
       telefono = request.form['telefono']  
       mail = request.form['mail']
       linkedin = request.form['linkedin']
       cur= mysql.connection.cursor()
       estado_inicial = 1
       cur.execute('INSERT INTO candidatos (nombrecandidato, apellidocandidato, telefono, mail, linkedin, idEstado) VALUES(%s, %s, %s, %s, %s, %s)',(nombrecandidato,apellidocandidato,telefono,mail,linkedin,estado_inicial))
       # Guardar historial de estados
       cur.execute("""
            INSERT INTO candidatos_estados
            VALUES (null, %s, LAST_INSERT_ID(), %s)
            """, (datetime.now(), estado_inicial))
       mysql.connection.commit()
       flash('Candidato añadido exitosamente')
       return redirect(url_for('Index'))

@app.route('/edit/<idcandidato>')    
def edit_contact(idcandidato):
    global user
    if len(user) == 0:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM candidatos WHERE idcandidato = %s',[idcandidato])
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', candidato = data[0])

@app.route('/state/<idcandidato>', methods = ['GET', 'POST'])    
def edit_contact_state(idcandidato):
    global user
    if len(user) == 0:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur = mysql.connection.cursor() 

        cur.execute('SELECT * FROM estados')
        estados = cur.fetchall()

        cur.execute('SELECT * FROM candidatos_estados where idcandidato = %s', [idcandidato])
        historial_estados = cur.fetchall()

        cur.execute('SELECT * FROM candidatos WHERE idcandidato = %s',[idcandidato])
        candidato = cur.fetchall()
        return render_template('edit-contact-state.html', candidato = candidato[0], estados = estados, historial_estados = historial_estados)
    elif request.method == 'POST':
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE candidatos
            SET idestado = %s
            WHERE idcandidato = %s
            """, (estado, idcandidato))
        # Guardar historial de estados
        cur.execute("""
            INSERT INTO candidatos_estados
            VALUES (null, %s, %s, %s)
            """, (datetime.now(), idcandidato, estado))
        mysql.connection.commit()
        flash('Candidato actualizado correctamente')
        return redirect(url_for('Index'))

@app.route('/update/<idcandidato>', methods = ['POST'])    
def update_contact(idcandidato):
    global user
    if len(user) == 0:
        return redirect(url_for('login'))
    if request.method == 'POST':
       nombrecandidato = request.form['nombrecandidato']
       apellidocandidato = request.form['apellidocandidato']
       telefono = request.form['telefono']
       mail = request.form['mail']
       linkedin = request.form['linkedin']
       cur = mysql.connection.cursor()
       cur.execute("""
            UPDATE candidatos
            SET nombrecandidato = %s,
                apellidocandidato = %s,
                telefono = %s,
                mail = %s,
                linkedin = %s
            WHERE idcandidato = %s
            """, (nombrecandidato,apellidocandidato,telefono,mail,linkedin,idcandidato))
    mysql.connection.commit()
    flash('Candidato actualizado correctamente')
    return redirect(url_for('Index')) 


@app.route('/delete/<string:idcandidato>')    
def delete_contact(idcandidato):
    global user
    if len(user) == 0:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM candidatos WHERE idcandidato = {0}'.format(idcandidato))
    mysql.connection.commit()
    flash('Candidato eliminado exitosamente')
    return redirect(url_for('Index'))


if(__name__=='__main__'):
    app.run(port = 3006, debug = True) 