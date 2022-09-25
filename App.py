from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'atsbbdd'
mysql = MySQL(app)


app.secret_key = 'mysecretkey'

@app.route('/')
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
    app.run(port = 3006, debug = True) 