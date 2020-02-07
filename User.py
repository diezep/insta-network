class User:
    tipo = ""
    descripcion = ''

    def __init__(self, nombre, usuario, publicaciones, seguidores, seguidos):
        self.nombre = nombre
        self.usuario = usuario
        self.publicaciones = publicaciones
        self.seguidores = seguidores
        self.seguidos = seguidos