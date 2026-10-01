
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from src.modelos import (
    DatosSolicitud,
    EstadoSolicitud,
    Estudiante,
    PrioridadSolicitud,
    Responsable,
)
from src.repositorio import (
    ErrorRepositorio,
    RepositorioSolicitudesJSON,
)
from src.servicio import ServicioSolicitudes


class TestSolicitudes(unittest.TestCase):
    def setUp(self):
        self.temporal = TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)

        self.ruta = (
            Path(self.temporal.name)
            / "datos"
            / "solicitudes.json"
        )

        self.repositorio = RepositorioSolicitudesJSON(self.ruta)
        self.servicio = ServicioSolicitudes(self.repositorio)

    def registrar(
        self,
        legajo="1001",
        nombre="Jorge Gomez",
        tipo="Certificado de alumno regular",
        prioridad=PrioridadSolicitud.MEDIA,
    ):
        datos = DatosSolicitud(
            estudiante=Estudiante(
                legajo=legajo,
                nombre=nombre,
                email="estudiante@example.com",
            ),
            tipo=tipo,
            descripcion="Solicitud de prueba",
            prioridad=prioridad,
        )

        return self.servicio.registrar_solicitud(datos)

    def test_archivo_inexistente_devuelve_lista_vacia(self):
        self.assertEqual(self.repositorio.obtener_todas(), [])
        self.assertFalse(self.ruta.exists())

    def test_registro_con_valores_iniciales(self):
        solicitud = self.registrar()

        self.assertEqual(solicitud.numero, 1)
        self.assertEqual(solicitud.estudiante.legajo, "1001")
        self.assertEqual(solicitud.prioridad, PrioridadSolicitud.MEDIA)
        self.assertEqual(solicitud.estado, EstadoSolicitud.PENDIENTE)
        self.assertIsNone(solicitud.responsable)

        datetime.strptime(
            solicitud.fecha_creacion,
            "%d/%m/%Y %H:%M",
        )

        self.assertTrue(self.ruta.exists())

    def test_numeracion_continua_despues_de_recargar(self):
        self.registrar()

        servicio_recargado = ServicioSolicitudes(
            RepositorioSolicitudesJSON(self.ruta)
        )

        datos = DatosSolicitud(
            estudiante=Estudiante(
                "1002",
                "Ana Martinez",
                "ana@example.com",
            ),
            tipo="Equivalencia",
            descripcion="Evaluacion de una materia",
            prioridad=PrioridadSolicitud.BAJA,
        )

        solicitud = servicio_recargado.registrar_solicitud(datos)

        self.assertEqual(solicitud.numero, 2)

    def test_buscar_por_numero(self):
        solicitud = self.registrar()

        self.assertIs(
            self.servicio.buscar_por_numero(solicitud.numero),
            solicitud,
        )
        self.assertIsNone(self.servicio.buscar_por_numero(999))

    def test_cambiar_estado_y_persistir(self):
        solicitud = self.registrar()

        resultado = self.servicio.cambiar_estado(
            solicitud.numero,
            EstadoSolicitud.EN_PROCESO,
        )

        self.assertTrue(resultado)
        self.assertEqual(
            solicitud.estado,
            EstadoSolicitud.EN_PROCESO,
        )

        recuperada = self.repositorio.obtener_todas()[0]

        self.assertEqual(
            recuperada.estado,
            EstadoSolicitud.EN_PROCESO,
        )

    def test_cambiar_estado_de_solicitud_inexistente(self):
        resultado = self.servicio.cambiar_estado(
            999,
            EstadoSolicitud.RESUELTA,
        )

        self.assertFalse(resultado)
        self.assertFalse(self.ruta.exists())

    def test_asignar_responsable_y_persistir(self):
        solicitud = self.registrar()
        responsable = Responsable(
            "Mariana Lopez",
            "Departamento de Alumnos",
        )

        resultado = self.servicio.asignar_responsable(
            solicitud.numero,
            responsable,
        )

        self.assertTrue(resultado)
        self.assertEqual(solicitud.responsable, responsable)

        recuperada = self.repositorio.obtener_todas()[0]

        self.assertEqual(recuperada.responsable, responsable)

    def test_asignar_responsable_a_solicitud_inexistente(self):
        resultado = self.servicio.asignar_responsable(
            999,
            Responsable("Mariana Lopez", "Alumnos"),
        )

        self.assertFalse(resultado)
        self.assertFalse(self.ruta.exists())

    def test_buscar_por_nombre_y_legajo(self):
        solicitud = self.registrar()
        self.registrar(legajo="1002", nombre="Ana Martinez")

        for valor in ("  JORGE  ", "1001"):
            with self.subTest(valor=valor):
                resultados = self.servicio.buscar_solicitudes(
                    "estudiante",
                    valor,
                )

                self.assertEqual(resultados, [solicitud])

    def test_filtrar_por_tipo_prioridad_y_estado(self):
        solicitud = self.registrar(
            prioridad=PrioridadSolicitud.ALTA
        )
        self.registrar(
            legajo="1002",
            nombre="Ana Martinez",
            tipo="Equivalencia",
        )

        self.servicio.cambiar_estado(
            solicitud.numero,
            EstadoSolicitud.EN_PROCESO,
        )

        casos = (
            ("tipo", "CERTIFICADO"),
            ("prioridad", "alta"),
            ("estado", "  En proceso  "),
        )

        for criterio, valor in casos:
            with self.subTest(criterio=criterio):
                resultados = self.servicio.buscar_solicitudes(
                    criterio,
                    valor,
                )

                self.assertEqual(resultados, [solicitud])

    def test_buscar_por_responsable_y_area(self):
        solicitud = self.registrar()
        self.registrar(legajo="1002", nombre="Ana Martinez")

        self.servicio.asignar_responsable(
            solicitud.numero,
            Responsable(
                "Mariana Lopez",
                "Departamento de Alumnos",
            ),
        )

        for valor in ("MARIANA", "alumnos"):
            with self.subTest(valor=valor):
                resultados = self.servicio.buscar_solicitudes(
                    "responsable",
                    valor,
                )

                self.assertEqual(resultados, [solicitud])

    def test_busqueda_sin_resultados_y_criterio_invalido(self):
        self.registrar()

        self.assertEqual(
            self.servicio.buscar_solicitudes(
                "estudiante",
                "inexistente",
            ),
            [],
        )

        self.assertEqual(
            self.servicio.buscar_solicitudes(
                "criterio_invalido",
                "Jorge",
            ),
            [],
        )

    def test_resumen_sin_solicitudes(self):
        self.assertEqual(
            self.servicio.obtener_resumen(),
            {
                "total": 0,
                "pendientes": 0,
                "en_proceso": 0,
                "resueltas": 0,
            },
        )

    def test_resumen_con_distintos_estados(self):
        self.registrar()
        segunda = self.registrar(
            legajo="1002",
            nombre="Ana Martinez",
        )
        tercera = self.registrar(
            legajo="1003",
            nombre="Lucia Fernandez",
        )

        self.servicio.cambiar_estado(
            segunda.numero,
            EstadoSolicitud.EN_PROCESO,
        )
        self.servicio.cambiar_estado(
            tercera.numero,
            EstadoSolicitud.RESUELTA,
        )

        self.assertEqual(
            self.servicio.obtener_resumen(),
            {
                "total": 3,
                "pendientes": 1,
                "en_proceso": 1,
                "resueltas": 1,
            },
        )

    def test_guardar_y_recuperar_informacion_completa(self):
        solicitud = self.registrar()

        recuperadas = self.repositorio.obtener_todas()

        self.assertEqual(len(recuperadas), 1)
        self.assertEqual(
            recuperadas[0].convertir_diccionario(),
            solicitud.convertir_diccionario(),
        )

    def test_obtener_solicitudes_devuelve_copia_de_lista(self):
        self.registrar()

        solicitudes = self.servicio.obtener_solicitudes()
        solicitudes.clear()

        self.assertEqual(
            len(self.servicio.obtener_solicitudes()),
            1,
        )
    def test_json_invalido_genera_error_controlado(self):
           self.ruta.parent.mkdir(
               parents=True,
               exist_ok=True,
           )
   
           self.ruta.write_text(
               "{ contenido inválido",
               encoding="utf-8",
           )
   
           with self.assertRaisesRegex(
               ErrorRepositorio,
               "JSON inválido",
           ):
               self.repositorio.obtener_todas()

if __name__ == "__main__":
    unittest.main()

  