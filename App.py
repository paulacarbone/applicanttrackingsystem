from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)


app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'atsbbdd'
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

@app.route('/candidatos')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM candidatos')
    data = cur.fetchall()
    return render_template('index.html', candidatos = data)

@app.route('/add_contact', methods = ['POST'])    
def add_contact():
    if request.method == 'POST':
       nombrecandidato = request.form['nombrecandidato']
       apellidocandidato = request.form['apellidocandidato']
       telefono = request.form['telefono']  
       mail = request.form['mail']
       linkedin = request.form['linkedin']
       cur= mysql.connection.cursor()
       cur.execute('INSERT INTO candidatos (nombrecandidato, apellidocandidato, telefono, mail, linkedin) VALUES(%s, %s, %s, %s, %s)',(nombrecandidato,apellidocandidato,telefono,mail,linkedin))
    
       mysql.connection.commit()
       flash('Candidato añadido exitosamente')
       return redirect(url_for('Index'))

@app.route('/edit/<idcandidato>')    
def get_contact(idcandidato):
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM candidatos WHERE idcandidato = %s',[idcandidato])
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', candidato = data[0])


@app.route('/update/<idcandidato>', methods = ['POST'])    
def update_contact(idcandidato):
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
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM candidatos WHERE idcandidato = {0}'.format(idcandidato))
    mysql.connection.commit()
    flash('Candidato eliminado exitosamente')
    return redirect(url_for('Index'))


if(__name__=='__main__'):
    app.run(port = 3007, debug = True) 