from dataclasses import dataclass
from enum import Enum


class EstadoSolicitud(Enum):
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTA = "Resuelta"


class PrioridadSolicitud(Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"


@dataclass
class Estudiante:
    legajo: str
    nombre: str
    email: str

    def convertir_diccionario(self):
        return {
            "legajo": self.legajo,
            "nombre": self.nombre,
            "email": self.email
        }


@dataclass
class Responsable:
    nombre: str
    area: str

    def convertir_diccionario(self):
        return {
            "nombre": self.nombre,
            "area": self.area
        }


@dataclass
class DatosSolicitud:
    estudiante: Estudiante
    tipo: str
    descripcion: str
    prioridad: PrioridadSolicitud


@dataclass
class Solicitud:
    numero: int
    estudiante: Estudiante
    tipo: str
    descripcion: str
    prioridad: PrioridadSolicitud
    estado: EstadoSolicitud
    responsable: Responsable | None
    fecha_creacion: str

    def cambiar_estado(self, nuevo_estado: EstadoSolicitud):
        self.estado = nuevo_estado

    def asignar_responsable(self, responsable: Responsable):
        self.responsable = responsable

    def convertir_diccionario(self):
        return {
            "numero": self.numero,
            "estudiante": self.estudiante.convertir_diccionario(),
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad.value,
            "estado": self.estado.value,
            "responsable": (
                self.responsable.convertir_diccionario()
                if self.responsable
                else None
            ),
            "fecha_creacion": self.fecha_creacion
        }

    @classmethod
    def desde_diccionario(cls, datos):
        estudiante = Estudiante(
            datos["estudiante"]["legajo"],
            datos["estudiante"]["nombre"],
            datos["estudiante"]["email"]
        )

        responsable = None
        if datos.get("responsable"):
            responsable = Responsable(
                datos["responsable"]["nombre"],
                datos["responsable"]["area"]
            )

        return cls(
            numero=datos["numero"],
            estudiante=estudiante,
            tipo=datos["tipo"],
            descripcion=datos["descripcion"],
            prioridad=PrioridadSolicitud(datos["prioridad"]),
            estado=EstadoSolicitud(datos["estado"]),
            responsable=responsable,
            fecha_creacion=datos["fecha_creacion"]
        )