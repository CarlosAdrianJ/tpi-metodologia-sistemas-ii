import json
from pathlib import Path
from typing import Protocol

from src.modelos import Solicitud


class RepositorioSolicitudes(Protocol):
    def obtener_todas(self) -> list[Solicitud]:
        ...

    def guardar_todas(self, solicitudes: list[Solicitud]) -> None:
        ...


class RepositorioSolicitudesJSON:
    def __init__(self, ruta_archivo: Path | None = None):
        if ruta_archivo is None:
            ruta_archivo = (
                Path(__file__).resolve().parent.parent
                / "datos"
                / "solicitudes.json"
            )

        self.ruta_archivo = ruta_archivo

    def obtener_todas(self) -> list[Solicitud]:
        if not self.ruta_archivo.exists():
            return []

        try:
            with open(
                self.ruta_archivo,
                "r",
                encoding="utf-8",
            ) as archivo:
                datos = json.load(archivo)

            return [
                Solicitud.desde_diccionario(solicitud)
                for solicitud in datos
            ]

        except (
            json.JSONDecodeError,
            OSError,
            KeyError,
            TypeError,
            ValueError,
        ):
            return []

    def guardar_todas(
        self,
        solicitudes: list[Solicitud],
    ) -> None:
        self.ruta_archivo.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        datos = [
            solicitud.convertir_diccionario()
            for solicitud in solicitudes
        ]

        with open(
            self.ruta_archivo,
            "w",
            encoding="utf-8",
        ) as archivo:
            json.dump(
                datos,
                archivo,
                ensure_ascii=False,
                indent=4,
            )