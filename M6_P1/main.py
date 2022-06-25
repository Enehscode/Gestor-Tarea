from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea

# Inicializar web server
app = Flask(__name__)

@app.route("/")  # Ruta inicial al entrar a la pág (raíz)
def home():
    todas_las_tareas = db.session.query(Tarea).order_by(Tarea.categoria.desc())
    for t in todas_las_tareas:
        print(t)

    return render_template("index.html", listaTareas = todas_las_tareas)  # Como pág principal nos devolverá el archivo HTML

@app.route("/crear-tarea", methods=["POST"])
def crear():
    tarea = Tarea(contenido=request.form['contenido_tarea'], categoria=request.form['categoria_tarea'], fecha=request.form['fecha_limite'], hecha=False, edit=False)
    db.session.add(tarea)  # Añadir el objeto Tarea de la bd
    db.session.commit()  # Ejecutar la operación pendiente de la bd
    db.session.close()
    return redirect(url_for("home"))

@app.route("/eliminar-tarea/<id>")
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=id).delete()
    db.session.commit()
    db.session.close()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=id).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    db.session.close()
    return redirect(url_for("home"))

@app.route("/editar/<id>")
def editar(id):
    tarea = db.session.query(Tarea).filter_by(id=id).first()
    tarea.edit = True
    db.session.commit()
    db.session.close()
    return redirect(url_for("home"))

@app.route("/editar-tarea/<id>", methods=["POST"])
def editar_tarea(id):

    nContenido = request.form['nuevo_contenido']
    nCategoria = request.form['nCategoria']
    nFecha = request.form['nueva_fecha']

    if nContenido != "" and nCategoria != "Seleccione una categoria" and nFecha != "":  # funciona
        db.session.query(Tarea).filter(Tarea.id == id).update({"contenido": nContenido, "categoria": nCategoria, "fecha": nFecha, "edit": False})

    elif nContenido != "" and nCategoria == "Seleccione una categoria" and nFecha == "": # funciona
        db.session.query(Tarea).filter(Tarea.id == id).update({"contenido": nContenido,"edit": False})

    elif nContenido != "" and nCategoria != "Seleccione una categoria" and nFecha == "": # funciona
        db.session.query(Tarea).filter(Tarea.id == id).update({"contenido": nContenido, "categoria": nCategoria, "edit": False})

    elif nContenido == "" and nCategoria != "Seleccione una categoria" and nFecha == "":  # funciona
        db.session.query(Tarea).filter(Tarea.id == id).update({"categoria": nCategoria, "edit": False})

    elif nContenido == "" and nCategoria == "Seleccione una categoria" and nFecha != "":  # funciona
        db.session.query(Tarea).filter(Tarea.id == id).update({"fecha": nFecha, "edit": False})

    elif nContenido == "" and nCategoria != "Seleccione una categoria" and nFecha != "": # Funciona
        db.session.query(Tarea).filter(Tarea.id == id).update({"categoria": nCategoria, "fecha": nFecha, "edit": False})

    elif nContenido != "" and nCategoria == "Seleccione una categoria" and nFecha != "":
        db.session.query(Tarea).filter(Tarea.id == id).update({"contenido": nContenido, "categoria": Tarea.categoria, "fecha": nFecha, "edit": False})

    else:
        db.session.query(Tarea).filter(Tarea.id == id).update({"edit": False})

    db.session.commit()
    db.session.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)  # Arrancar web server. Debug por consola (True)
