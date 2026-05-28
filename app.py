import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from dotenv import load_dotenv

from db import get_connection
from validators import validar_componente, validar_reparacion, validar_login, validar_contacto
from security import verificar_password
from email_service import enviar_correo_contacto
from models import Componente, Reparacion

import re
from markupsafe import escape

def sanitizar_nombre(nombre):
    # Validar que el dato sea realmente texto
    if not isinstance(nombre, str):
        return "Invitado"
    
    # Limpiar espacios en blanco a los lados y escapar caracteres HTML (ej. <script>)
    nombre = escape(nombre.strip())
    
    # Limitar a 64 caracteres para que no desborde la base de datos
    if len(nombre) > 64:
        nombre = nombre[:64]
        
    # Verificar que solo contenga letras, números, espacios y acentos válidos
    if not re.match(r"^[a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ.-]+$", nombre):
        return "Invitado"
        
    return nombre or "Invitado"

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_temporal_desarrollo")

# Permite conectar el frontend de Vue con este backend
CORS(app, supports_credentials=True)

@app.route("/")
def inicio():
    return jsonify({
        "mensaje": "Backend Flask activo",
        "proyecto": "Sistema de Venta de PC y Reparaciones"
    }), 200

# ==========================================
# RUTAS PARA COMPONENTES (INVENTARIO)
# ==========================================
@app.route("/componentes", methods=["GET"])
def obtener_componentes():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM componentes")
    componentes = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(componentes), 200

@app.route("/componentes", methods=["POST"])
def agregar_componente():
    data = request.json
    errores = validar_componente(data)
    if errores:
        return jsonify({"errores": errores}), 400

    conexion = get_connection()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO componentes (nombre, categoria, descripcion, precio, stock, activo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        data.get("nombre"),
        data.get("categoria"),
        data.get("descripcion", ""),
        float(data.get("precio", 0)),
        int(data.get("stock", 0)),
        bool(data.get("activo", True))
    )
    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Componente agregado correctamente", "id": nuevo_id}), 201

# ==========================================
# RUTAS PARA REPARACIONES (TALLER)
# ==========================================
@app.route("/reparaciones", methods=["GET"])
def obtener_reparaciones():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reparaciones")
    reparaciones = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(reparaciones), 200

@app.route("/reparaciones", methods=["POST"])
def agregar_reparacion():
    data = request.json
    errores = validar_reparacion(data)
    if errores:
        return jsonify({"errores": errores}), 400

    conexion = get_connection()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO reparaciones (cliente_nombre, equipo, problema, estado, costo)
        VALUES (%s, %s, %s, %s, %s)
    """
    valores = (
        sanitizar_nombre(data.get("cliente_nombre", "")),
        data.get("equipo"),
        data.get("problema", ""),
        data.get("estado", "En revisión"),
        float(data.get("costo", 0))
    )
    cursor.execute(sql, valores)
    conexion.commit()

    # --- Enviar correo de aviso ---
    try:
        from email_service import enviar_correo_contacto
        asunto = "Nuevo Equipo en Taller - TechFix"
        cuerpo = f"Hola administrador,\n\nSe acaba de registrar un nuevo equipo ({data.get('equipo')}) para el cliente {valores[0]}.\nEstado actual: {data.get('estado')}."
        
        import os
        correo_destino = os.getenv("MAIL_TO")
        enviar_correo_contacto(correo_destino, asunto, cuerpo)
    except Exception as e:
        print("Aviso: No se pudo enviar el correo", e)
    # ------------------------------------

    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Reparación registrada correctamente", "id": nuevo_id}), 201

# ==========================================
# LOGIN Y SESIÓN 
# ==========================================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    errores = validar_login(data)
    if errores:
        return jsonify({"errores": errores}), 400

    correo = data.get("correo")
    password = data.get("password")

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    if not verificar_password(password, usuario["password"]):
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401

    session["usuario_id"] = usuario["id"]
    session["nombreUsuario"] = usuario["nombre"]
    session["correo"] = usuario["correo"]
    session["autenticado"] = True

    return jsonify({
        "mensaje": "Sesión iniciada correctamente",
        "sesion": {
            "nombreUsuario": usuario["nombre"],
            "correo": usuario["correo"],
            "autenticado": True
        }
    }), 200

@app.route("/sesion", methods=["GET"])
def obtener_sesion():
    if session.get("autenticado"):
        return jsonify({
            "nombreUsuario": session.get("nombreUsuario"),
            "correo": session.get("correo"),
            "autenticado": True
        }), 200
    return jsonify({
        "nombreUsuario": "Invitado",
        "correo": None,
        "autenticado": False
    }), 200

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200

# ==========================================
# CONTACTO / CORREO
# ==========================================
@app.route("/contacto", methods=["POST"])
def contacto():
    data = request.json
    errores = validar_contacto(data)
    if errores:
        return jsonify({"errores": errores}), 400

    enviar_correo_contacto(
        data.get("nombre", "Cliente"),
        data.get("correo"),
        data.get("mensaje")
    )
    return jsonify({"mensaje": "Correo enviado correctamente"}), 200

# ==========================================
# ELIMINACION
# ==========================================
@app.route("/componentes/<int:id>/desactivar", methods=["PUT"])
def desactivar_componente(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        # Eliminamos el registro físicamente de la base de datos
        sql = "DELETE FROM componentes WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return jsonify({"mensaje": "Componente eliminado correctamente"}), 200
    except Exception as e:
        print("Error al eliminar componente:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route("/reparaciones/<int:id>", methods=["DELETE"])
def eliminar_reparacion(id):
    try:
        conexion = get_connection()
        cursor = conexion.cursor()
        
        # Eliminamos la reparación de la base de datos
        sql = "DELETE FROM reparaciones WHERE id = %s"
        cursor.execute(sql, (id,))
        conexion.commit()
        
        cursor.close()
        conexion.close()
        
        return jsonify({"mensaje": "Reparación eliminada correctamente"}), 200
    except Exception as e:
        print("Error al eliminar reparación:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    app.run(debug=True)