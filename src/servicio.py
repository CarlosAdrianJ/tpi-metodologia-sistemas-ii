from datetime import datetime

from src.modelos import (
    DatosSolicitud,
    EstadoSolicitud,
    Responsable,
    Solicitud,
)
from src.repositorio import RepositorioSolicitudes


class ServicioSolicitudes:
    def __init__(
        self,
        repositorio: RepositorioSolicitudes,
    ):
        self.repositorio = repositorio
        self.solicitudes = repositorio.obtener_todas()

    def registrar_solicitud(
        self,
        datos: DatosSolicitud,
    ) -> Solicitud:
        solicitud = Solicitud(
            numero=self._generar_numero(),
            estudiante=datos.estudiante,
            tipo=datos.tipo,
            descripcion=datos.descripcion,
            prioridad=datos.prioridad,
            estado=EstadoSolicitud.PENDIENTE,
            responsable=None,
            fecha_creacion=datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            ),
        )

        self.solicitudes.append(solicitud)
        self._guardar()
        return solicitud

    def buscar_por_numero(
        self,
        numero: int,
    ) -> Solicitud | None:
        return next(
            (
                solicitud
                for solicitud in self.solicitudes
                if solicitud.numero == numero
            ),
            None,
        )

    def cambiar_estado(
        self,
        numero: int,
        nuevo_estado: EstadoSolicitud,
    ) -> bool:
        solicitud = self.buscar_por_numero(numero)

        if solicitud is None:
            return False

        solicitud.cambiar_estado(nuevo_estado)
        self._guardar()
        return True

    def asignar_responsable(
        self,
        numero: int,
        responsable: Responsable,
    ) -> bool:
        solicitud = self.buscar_por_numero(numero)

        if solicitud is None:
            return False

        solicitud.asignar_responsable(responsable)
        self._guardar()
        return True

    def buscar_solicitudes(
        self,
        criterio: str,
        valor: str,
    ) -> list[Solicitud]:
        valor_normalizado = valor.strip().lower()

        filtros = {
            "estudiante": lambda solicitud: (
                valor_normalizado
                in solicitud.estudiante.nombre.lower()
                or valor_normalizado
                in solicitud.estudiante.legajo.lower()
            ),
            "tipo": lambda solicitud: (
                valor_normalizado in solicitud.tipo.lower()
            ),
            "prioridad": lambda solicitud: (
                valor_normalizado
                in solicitud.prioridad.value.lower()
            ),
            "estado": lambda solicitud: (
                valor_normalizado
                in solicitud.estado.value.lower()
            ),
            "responsable": lambda solicitud: (
                solicitud.responsable is not None
                and (
                    valor_normalizado
                    in solicitud.responsable.nombre.lower()
                    or valor_normalizado
                    in solicitud.responsable.area.lower()
                )
            ),
        }

        filtro = filtros.get(criterio)

        if filtro is None:
            return []

        return [
            solicitud
            for solicitud in self.solicitudes
            if filtro(solicitud)
        ]

    def obtener_solicitudes(self) -> list[Solicitud]:
        return list(self.solicitudes)

    def obtener_resumen(self) -> dict[str, int]:
        return {
            "total": len(self.solicitudes),
            "pendientes": self._contar_por_estado(
                EstadoSolicitud.PENDIENTE
            ),
            "en_proceso": self._contar_por_estado(
                EstadoSolicitud.EN_PROCESO
            ),
            "resueltas": self._contar_por_estado(
                EstadoSolicitud.RESUELTA
            ),
        }

    def _generar_numero(self) -> int:
        if not self.solicitudes:
            return 1

        return max(
            solicitud.numero
            for solicitud in self.solicitudes
        ) + 1

    def _contar_por_estado(
        self,
        estado: EstadoSolicitud,
    ) -> int:
        return sum(
            solicitud.estado == estado
            for solicitud in self.solicitudes
        )

    def _guardar(self) -> None:
        self.repositorio.guardar_todas(self.solicitudes)