# TechFix & Ventas - Backend API (Flask + MySQL)

Este repositorio contiene la API REST para el sistema de gestión de inventario de hardware y seguimiento de taller **TechFix & Ventas**.
> 👉 **webfinal-frontend.vercel.app**

## 🚀 Enlace de Producción
* **Backend Vivo (Render):** https://api-techfix-backend.onrender.com

---

## 💻 Instrucciones para despliegue local (Desarrollo)

Si deseas correr este servidor en tu propia computadora, sigue estos pasos:

### 1. Crear y activar entorno virtual
``
python -m venv venv
venv\Scripts\activate
``

### 2. Instalar dependencias
``
pip install -r requirements.txt
``

### 3. Configurar variables de entorno
Crea un archivo llamado .env en la raíz del proyecto y ajusta tus credenciales (Base de datos y SMTP de Gmail) siguiendo el formato necesario.

### 4. Base de datos
Importa el archivo sistema_pcs.sql en tu gestor de base de datos MySQL/MariaDB (por ejemplo, usando phpMyAdmin).

### 5. Crear usuario administrador
``
python create_user.py
``

### 6. Ejecutar servidor
``
gunicorn app:app
``
# O de manera local tradicional: python app.py

## Endpoints principales del sistema
* **El sistema expone las siguientes rutas principales:**
* **GET, POST, PUT, DELETE /componentes (Gestión de inventario)
* **GET, POST, PUT, DELETE /reparaciones (Gestión de equipos en taller)
* **POST /login (Inicio de sesión)
* **GET /sesion (Validación de estado)
* **POST /logout (Cierre de sesión)

## Estructura de archivos principales
* **app.py: Rutas y endpoints.
* **db.py: Conexión a la base de datos MySQL.
* **validators.py: Validaciones de entrada de datos del usuario.
* **security.py: Hash y verificación de contraseñas.
* **email_service.py: Lógica de envío de correos mediante SMTP.
* **models.py: Modelos de datos para componentes y reparaciones.
