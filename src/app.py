from flask import Flask, render_template, request,redirect,url_for
import database as db


app=Flask(__name__)
@app.route('/')
def index():
    cursor=db.database.cursor()
    cursor.execute("SELECT * FROM codoacodo")
    resultado=cursor.fetchall()
    insertarobjeto=[]
    nombresdecolumnas=[column[0] for column in cursor.description]
    for record in resultado:
        insertarobjeto.append(dict(zip(nombresdecolumnas, record)))
    return render_template('index.html', data=insertarobjeto)


@app.route('/persona', methods=['POST'])
def agregarpersona():
    nombre=request.form['nombre']
    telefono=request.form['telefono']
    email=request.form['email']

    if nombre and telefono and email:
        cursor=db.database.cursor()
        sql="INSERT INTO codoacodo (nombre,telefono,email) VALUES (%s,%s,%s)"
        data=(nombre, telefono,email)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cursor=db.database.cursor()
    sql="DELETE FROM codoacodo WHERE id=%s"
    data=(id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('index'))

@app.route('/edit/<string:id>', methods=['POST'])
def editar(id):
    nombre=request.form['nombre']
    telefono=request.form['telefono']
    email=request.form['email']

    if nombre and telefono and email:
        cursor=db.database.cursor()
        sql="UPDATE  codoacodo SET nombre=%s, telefono=%s, email=%s WHERE id=%s"
        data=(nombre, telefono,email,id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True, port=4000)
