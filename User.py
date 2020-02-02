class User:
    tipo = ""

    def __init__(self, nombre, usuario, publicaciones, seguidores, seguidos, descripcion):
        self.nombre = nombre
        self.usuario = usuario
        self.publicaciones = publicaciones
        self.seguidores = seguidores
        self.seguidos = seguidos
        self.descripcion = descripcion