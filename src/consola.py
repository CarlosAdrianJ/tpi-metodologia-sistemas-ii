from src.modelos import (
    DatosSolicitud,
    EstadoSolicitud,
    Estudiante,
    PrioridadSolicitud,
    Responsable,
    Solicitud,
)
from src.servicio import ServicioSolicitudes


class ConsolaSolicitudes:
    def __init__(self, servicio: ServicioSolicitudes):
        self.servicio = servicio
        self.opciones = {
            "1": self.registrar_solicitud,
            "2": self.cambiar_estado,
            "3": self.asignar_responsable,
            "4": self.buscar_solicitudes,
            "5": self.generar_reporte,
        }

    def ejecutar(self) -> None:
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "6":
                print("Programa finalizado.")
                break

            operacion = self.opciones.get(opcion)

            if operacion is None:
                print("La opción ingresada no es válida.")
            else:
                operacion()

    def mostrar_menu(self) -> None:
        print("\nSISTEMA DE GESTIÓN DE SOLICITUDES ACADÉMICAS")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar o filtrar solicitudes")
        print("5. Generar reporte básico")
        print("6. Salir")

    def registrar_solicitud(self) -> None:
        print("\nREGISTRAR SOLICITUD")

        legajo = self.solicitar_texto(
            "Legajo del estudiante: "
        )
        nombre = self.solicitar_texto(
            "Nombre y apellido: "
        )
        email = self.solicitar_email()
        tipo = self.solicitar_texto(
            "Tipo de solicitud: "
        )
        descripcion = self.solicitar_texto(
            "Descripción: "
        )
        prioridad = self.seleccionar_prioridad()

        estudiante = Estudiante(
            legajo=legajo,
            nombre=nombre,
            email=email,
        )

        datos = DatosSolicitud(
            estudiante=estudiante,
            tipo=tipo,
            descripcion=descripcion,
            prioridad=prioridad,
        )

        solicitud = self.servicio.registrar_solicitud(datos)

        print(
            f"Solicitud número {solicitud.numero} "
            "registrada correctamente."
        )

    def cambiar_estado(self) -> None:
        print("\nCAMBIAR ESTADO")

        numero = self.solicitar_numero(
            "Número de solicitud: "
        )

        print("1. Pendiente")
        print("2. En proceso")
        print("3. Resuelta")

        opciones = {
            "1": EstadoSolicitud.PENDIENTE,
            "2": EstadoSolicitud.EN_PROCESO,
            "3": EstadoSolicitud.RESUELTA,
        }

        opcion = input(
            "Seleccione el nuevo estado: "
        ).strip()

        estado = opciones.get(opcion)

        if estado is None:
            print("El estado seleccionado no es válido.")
            return

        actualizado = self.servicio.cambiar_estado(
            numero,
            estado,
        )

        if actualizado:
            print("Estado actualizado correctamente.")
        else:
            print("No se encontró la solicitud.")

    def asignar_responsable(self) -> None:
        print("\nASIGNAR RESPONSABLE")

        numero = self.solicitar_numero(
            "Número de solicitud: "
        )
        nombre = self.solicitar_texto(
            "Nombre del responsable: "
        )
        area = self.solicitar_texto(
            "Nombre del área: "
        )

        responsable = Responsable(
            nombre=nombre,
            area=area,
        )

        asignado = self.servicio.asignar_responsable(
            numero,
            responsable,
        )

        if asignado:
            print("Responsable asignado correctamente.")
        else:
            print("No se encontró la solicitud.")

    def buscar_solicitudes(self) -> None:
        print("\nBUSCAR O FILTRAR SOLICITUDES")
        print("1. Buscar por estudiante")
        print("2. Filtrar por tipo")
        print("3. Filtrar por prioridad")
        print("4. Filtrar por estado")
        print("5. Filtrar por responsable o área")

        criterios = {
            "1": "estudiante",
            "2": "tipo",
            "3": "prioridad",
            "4": "estado",
            "5": "responsable",
        }

        opcion = input(
            "Seleccione un criterio: "
        ).strip()

        criterio = criterios.get(opcion)

        if criterio is None:
            print("El criterio seleccionado no es válido.")
            return

        valor = self.solicitar_texto(
            "Ingrese el valor buscado: "
        )

        resultados = self.servicio.buscar_solicitudes(
            criterio,
            valor,
        )

        if not resultados:
            print("No se encontraron solicitudes.")
            return

        print("\nRESULTADOS")
        print("-" * 60)

        for solicitud in resultados:
            self.mostrar_solicitud(solicitud)

    def generar_reporte(self) -> None:
        print("\nREPORTE BÁSICO DE SOLICITUDES")
        print("-" * 60)

        solicitudes = self.servicio.obtener_solicitudes()

        if not solicitudes:
            print("No hay solicitudes registradas.")
            return

        for solicitud in solicitudes:
            self.mostrar_solicitud(solicitud)

        resumen = self.servicio.obtener_resumen()

        print(f"Total de solicitudes: {resumen['total']}")
        print(f"Pendientes: {resumen['pendientes']}")
        print(f"En proceso: {resumen['en_proceso']}")
        print(f"Resueltas: {resumen['resueltas']}")

    def mostrar_solicitud(
        self,
        solicitud: Solicitud,
    ) -> None:
        responsable = "Sin asignar"

        if solicitud.responsable is not None:
            responsable = (
                f"{solicitud.responsable.nombre} - "
                f"{solicitud.responsable.area}"
            )

        print(f"Número: {solicitud.numero}")
        print(
            f"Estudiante: {solicitud.estudiante.nombre} - "
            f"Legajo: {solicitud.estudiante.legajo}"
        )
        print(f"Tipo: {solicitud.tipo}")
        print(f"Descripción: {solicitud.descripcion}")
        print(f"Prioridad: {solicitud.prioridad.value}")
        print(f"Estado: {solicitud.estado.value}")
        print(f"Responsable: {responsable}")
        print(f"Fecha: {solicitud.fecha_creacion}")
        print("-" * 60)

    def seleccionar_prioridad(
        self,
    ) -> PrioridadSolicitud:
        opciones = {
            "1": PrioridadSolicitud.BAJA,
            "2": PrioridadSolicitud.MEDIA,
            "3": PrioridadSolicitud.ALTA,
        }

        while True:
            print("1. Baja")
            print("2. Media")
            print("3. Alta")

            opcion = input(
                "Seleccione la prioridad: "
            ).strip()

            prioridad = opciones.get(opcion)

            if prioridad is not None:
                return prioridad

            print("La prioridad seleccionada no es válida.")

    def solicitar_texto(self, mensaje: str) -> str:
        while True:
            valor = input(mensaje).strip()

            if valor:
                return valor

            print("El valor no puede estar vacío.")

    def solicitar_numero(self, mensaje: str) -> int:
        while True:
            valor = input(mensaje).strip()

            if valor.isdigit():
                return int(valor)

            print("Debe ingresar un número válido.")

    def solicitar_email(self) -> str:
        while True:
            email = input(
                "Correo electrónico: "
            ).strip()

            if "@" in email and "." in email:
                return email

            print("El correo electrónico no es válido.")