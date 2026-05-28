def validar_componente(data):
    errores = {}
    if not data.get("nombre") or str(data.get("nombre")).strip() == "":
        errores["nombre"] = "El nombre del componente es obligatorio."
    if not data.get("categoria") or str(data.get("categoria")).strip() == "":
        errores["categoria"] = "La categoría es obligatoria."
    return errores

def validar_reparacion(data):
    errores = {}
    if not data.get("cliente_nombre") or str(data.get("cliente_nombre")).strip() == "":
        errores["cliente_nombre"] = "El nombre del cliente es obligatorio."
    if not data.get("equipo") or str(data.get("equipo")).strip() == "":
        errores["equipo"] = "El nombre del equipo es obligatorio."
    return errores

def validar_login(data):
    errores = {}
    if not data.get("correo"): errores["correo"] = "El correo es obligatorio."
    if not data.get("password"): errores["password"] = "La contraseña es obligatoria."
    return errores

def validar_contacto(data):
    errores = {}
    if not data.get("correo"): errores["correo"] = "El correo es obligatorio."
    if not data.get("mensaje"): errores["mensaje"] = "El mensaje es obligatorio."
    return errores