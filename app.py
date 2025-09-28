from __future__ import annotations
import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# ==== Config ====
load_dotenv()  # Lee variables desde .env si existe

def get_db_config():
    cfg = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        # Fuerza 6000 como default en lugar de 3306
        "port": int(os.getenv("MYSQL_PORT", "6000")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", "501914"),
        "database": os.getenv("MYSQL_DB", "desarrollo_web"),
    }
    print("DBG MySQL config =>", cfg)
    return cfg


def get_conn():
    try:
        conn = mysql.connector.connect(**get_db_config())
        return conn
    except Error as e:
        print("Error de conexión MySQL:", e)
        raise

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")  # cambia en producción

    @app.route("/")
    def index():
        return redirect(url_for("listar_productos"))

    # ==== CRUD ====
    @app.route("/productos")
    def listar_productos():
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id_producto, nombre, precio, stock, creado_en FROM productos ORDER BY id_producto DESC")
        productos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("index.html", productos=productos)

    @app.route("/crear", methods=["GET", "POST"])
    def crear_producto():
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            precio = request.form.get("precio", "").strip()
            stock = request.form.get("stock", "").strip()

            # Validación básica
            errores = []
            if not nombre:
                errores.append("El nombre es obligatorio.")
            try:
                precio_val = float(precio)
                if precio_val < 0:
                    errores.append("El precio no puede ser negativo.")
            except ValueError:
                errores.append("El precio debe ser numérico.")
            try:
                stock_val = int(stock)
                if stock_val < 0:
                    errores.append("El stock no puede ser negativo.")
            except ValueError:
                errores.append("El stock debe ser un entero.")

            if errores:
                for e in errores:
                    flash(e, "danger")
                return render_template("form.html", modo="crear", form={"nombre": nombre, "precio": precio, "stock": stock})

            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)",
                (nombre, precio_val, stock_val),
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Producto creado correctamente.", "success")
            return redirect(url_for("listar_productos"))

        return render_template("form.html", modo="crear", form={"nombre": "", "precio": "", "stock": ""})

    @app.route("/editar/<int:id_producto>", methods=["GET", "POST"])
    def editar_producto(id_producto: int):
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            precio = request.form.get("precio", "").strip()
            stock = request.form.get("stock", "").strip()

            errores = []
            if not nombre:
                errores.append("El nombre es obligatorio.")
            try:
                precio_val = float(precio)
                if precio_val < 0:
                    errores.append("El precio no puede ser negativo.")
            except ValueError:
                errores.append("El precio debe ser numérico.")
            try:
                stock_val = int(stock)
                if stock_val < 0:
                    errores.append("El stock no puede ser negativo.")
            except ValueError:
                errores.append("El stock debe ser un entero.")

            if errores:
                for e in errores:
                    flash(e, "danger")
                # Vuelve a cargar el registro para mantener consistencia visual
                cur.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
                producto = cur.fetchone()
                cur.close()
                conn.close()
                return render_template("form.html", modo="editar", form={"nombre": nombre, "precio": precio, "stock": stock}, producto=producto)

            cur2 = conn.cursor()
            cur2.execute(
                "UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s",
                (nombre, precio_val, stock_val, id_producto),
            )
            conn.commit()
            cur2.close()
            cur.close()
            conn.close()
            flash("Producto actualizado.", "success")
            return redirect(url_for("listar_productos"))

        # GET: cargar datos actuales
        cur.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cur.fetchone()
        cur.close()
        conn.close()
        if not producto:
            flash("Producto no encontrado.", "warning")
            return redirect(url_for("listar_productos"))
        return render_template("form.html", modo="editar", form=producto, producto=producto)

    @app.route("/eliminar/<int:id_producto>", methods=["GET", "POST"])
    def eliminar_producto(id_producto: int):
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        # Buscar registro
        cur.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cur.fetchone()

        if not producto:
            cur.close()
            conn.close()
            flash("Producto no encontrado.", "warning")
            return redirect(url_for("listar_productos"))

        if request.method == "POST":
            # Confirmado
            cur2 = conn.cursor()
            cur2.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            conn.commit()
            cur2.close()
            cur.close()
            conn.close()
            flash("Producto eliminado.", "success")
            return redirect(url_for("listar_productos"))

        cur.close()
        conn.close()
        # GET: pedir confirmación
        return render_template("confirm_delete.html", producto=producto)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=bool(int(os.getenv("FLASK_DEBUG", "1"))))