class Componente:
    """Modelo para representar un componente de computadora en el inventario."""
    
    def __init__(self, id, nombre, categoria, descripcion, precio=0.0, stock=0, activo=True):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.activo = activo

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "precio": float(self.precio), # Convertimos a float para que no haya error al mandar el JSON a Vue
            "stock": self.stock,
            "activo": bool(self.activo)
        }

class Reparacion:
    """Modelo para representar el seguimiento de la reparación de un equipo."""
    
    def __init__(self, id, cliente_nombre, equipo, problema, estado='En revisión', costo=0.0):
        self.id = id
        self.cliente_nombre = cliente_nombre
        self.equipo = equipo
        self.problema = problema
        self.estado = estado
        self.costo = costo

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_nombre": self.cliente_nombre,
            "equipo": self.equipo,
            "problema": self.problema,
            "estado": self.estado,
            "costo": float(self.costo)
        }