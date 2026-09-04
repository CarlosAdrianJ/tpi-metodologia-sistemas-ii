import json
from datetime import datetime
from pathlib import Path


class Estudiante:
    def __init__(self, legajo, nombre, email):
        self.legajo = legajo
        self.nombre = nombre
        self.email = email

    def convertir_diccionario(self):
        return {
            "legajo": self.legajo,
            "nombre": self.nombre,
            "email": self.email
        }


class Responsable:
    def __init__(self, nombre, area):
        self.nombre = nombre
        self.area = area

    def convertir_diccionario(self):
        return {
            "nombre": self.nombre,
            "area": self.area
        }


class Estado:
    PENDIENTE = "Pendiente"
    EN_PROCESO = "En proceso"
    RESUELTA = "Resuelta"


class Solicitud:
    def __init__(
        self,
        numero,
        estudiante,
        tipo,
        descripcion,
        prioridad,
        estado,
        responsable,
        fecha_creacion
    ):
        self.numero = numero
        self.estudiante = estudiante
        self.tipo = tipo
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.estado = estado
        self.responsable = responsable
        self.fecha_creacion = fecha_creacion

    def convertir_diccionario(self):
        return {
            "numero": self.numero,
            "estudiante": self.estudiante,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "responsable": self.responsable,
            "fecha_creacion": self.fecha_creacion
        }


class SistemaSolicitudes:
    def __init__(self):
        self.ruta_archivo = (
            Path(__file__).resolve().parent.parent
            / "datos"
            / "solicitudes.json"
        )
        self.solicitudes = self.cargar_datos()

    def cargar_datos(self):
        if not self.ruta_archivo.exists():
            return []

        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, OSError):
            return []

    def guardar_datos(self):
        self.ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

        with open(self.ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(
                self.solicitudes,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    def registrar_solicitud(self):
        print("\nREGISTRAR SOLICITUD")

        legajo = input("Legajo del estudiante: ").strip()
        while not legajo:
            print("El legajo no puede estar vacío.")
            legajo = input("Legajo del estudiante: ").strip()

        nombre = input("Nombre y apellido: ").strip()
        while not nombre:
            print("El nombre no puede estar vacío.")
            nombre = input("Nombre y apellido: ").strip()

        email = input("Correo electrónico: ").strip()
        while not email:
            print("El correo no puede estar vacío.")
            email = input("Correo electrónico: ").strip()

        tipo = input("Tipo de solicitud: ").strip()
        while not tipo:
            print("El tipo no puede estar vacío.")
            tipo = input("Tipo de solicitud: ").strip()

        descripcion = input("Descripción: ").strip()
        while not descripcion:
            print("La descripción no puede estar vacía.")
            descripcion = input("Descripción: ").strip()

        prioridad = input("Prioridad (Baja/Media/Alta): ").strip().capitalize()
        while prioridad not in ["Baja", "Media", "Alta"]:
            print("La prioridad ingresada no es válida.")
            prioridad = input(
                "Prioridad (Baja/Media/Alta): "
            ).strip().capitalize()

        estudiante = Estudiante(legajo, nombre, email)
        numero = len(self.solicitudes) + 1

        solicitud = Solicitud(
            numero,
            estudiante.convertir_diccionario(),
            tipo,
            descripcion,
            prioridad,
            Estado.PENDIENTE,
            None,
            datetime.now().strftime("%d/%m/%Y %H:%M")
        )

        self.solicitudes.append(solicitud.convertir_diccionario())
        self.guardar_datos()

        print(f"\nSolicitud número {numero} registrada correctamente.")

    def cambiar_estado(self):
        print("\nCAMBIAR ESTADO")

        try:
            numero = int(input("Número de solicitud: "))
        except ValueError:
            print("El número ingresado no es válido.")
            return

        solicitud_encontrada = None

        for solicitud in self.solicitudes:
            if solicitud["numero"] == numero:
                solicitud_encontrada = solicitud
                break

        if solicitud_encontrada is None:
            print("No se encontró la solicitud.")
            return

        print("1. Pendiente")
        print("2. En proceso")
        print("3. Resuelta")

        opcion = input("Seleccione el nuevo estado: ").strip()

        if opcion == "1":
            nuevo_estado = "Pendiente"
        elif opcion == "2":
            nuevo_estado = "En proceso"
        elif opcion == "3":
            nuevo_estado = "Resuelta"
        else:
            print("La opción ingresada no es válida.")
            return

        solicitud_encontrada["estado"] = nuevo_estado
        self.guardar_datos()

        print("Estado actualizado correctamente.")

    def asignar_responsable(self):
        print("\nASIGNAR RESPONSABLE")

        try:
            numero = int(input("Número de solicitud: "))
        except ValueError:
            print("El número ingresado no es válido.")
            return

        solicitud_encontrada = None

        for solicitud in self.solicitudes:
            if solicitud["numero"] == numero:
                solicitud_encontrada = solicitud
                break

        if solicitud_encontrada is None:
            print("No se encontró la solicitud.")
            return

        nombre = input("Nombre del responsable: ").strip()
        while not nombre:
            print("El nombre no puede estar vacío.")
            nombre = input("Nombre del responsable: ").strip()

        area = input("Área responsable: ").strip()
        while not area:
            print("El área no puede estar vacía.")
            area = input("Área responsable: ").strip()

        responsable = Responsable(nombre, area)
        solicitud_encontrada["responsable"] = (
            responsable.convertir_diccionario()
        )

        self.guardar_datos()
        print("Responsable asignado correctamente.")

    def buscar_solicitudes(self):
        print("\nBUSCAR O FILTRAR SOLICITUDES")
        print("1. Buscar por estudiante")
        print("2. Filtrar por tipo")
        print("3. Filtrar por prioridad")
        print("4. Filtrar por estado")
        print("5. Filtrar por área responsable")

        opcion = input("Seleccione un criterio: ").strip()
        valor = input("Ingrese el valor buscado: ").strip().lower()
        resultados = []

        for solicitud in self.solicitudes:
            if opcion == "1":
                nombre = solicitud["estudiante"]["nombre"].lower()
                if valor in nombre:
                    resultados.append(solicitud)
            elif opcion == "2":
                if valor in solicitud["tipo"].lower():
                    resultados.append(solicitud)
            elif opcion == "3":
                if valor == solicitud["prioridad"].lower():
                    resultados.append(solicitud)
            elif opcion == "4":
                if valor == solicitud["estado"].lower():
                    resultados.append(solicitud)
            elif opcion == "5":
                responsable = solicitud["responsable"]
                if responsable is not None:
                    if valor in responsable["area"].lower():
                        resultados.append(solicitud)
            else:
                print("La opción ingresada no es válida.")
                return

        if not resultados:
            print("No se encontraron solicitudes.")
            return

        print("\nRESULTADOS")

        for solicitud in resultados:
            self.mostrar_solicitud(solicitud)

    def mostrar_solicitud(self, solicitud):
        responsable = solicitud["responsable"]

        if responsable is None:
            responsable_texto = "Sin asignar"
        else:
            responsable_texto = (
                f'{responsable["nombre"]} - {responsable["area"]}'
            )

        print("-" * 60)
        print(f'Número: {solicitud["numero"]}')
        print(
            f'Estudiante: {solicitud["estudiante"]["nombre"]} '
            f'- Legajo: {solicitud["estudiante"]["legajo"]}'
        )
        print(f'Tipo: {solicitud["tipo"]}')
        print(f'Descripción: {solicitud["descripcion"]}')
        print(f'Prioridad: {solicitud["prioridad"]}')
        print(f'Estado: {solicitud["estado"]}')
        print(f'Responsable: {responsable_texto}')
        print(f'Fecha: {solicitud["fecha_creacion"]}')

    def generar_reporte(self):
        print("\nREPORTE BÁSICO DE SOLICITUDES")

        if not self.solicitudes:
            print("No hay solicitudes registradas.")
            return

        for solicitud in self.solicitudes:
            self.mostrar_solicitud(solicitud)

        cantidad_pendientes = 0
        cantidad_en_proceso = 0
        cantidad_resueltas = 0

        for solicitud in self.solicitudes:
            if solicitud["estado"] == "Pendiente":
                cantidad_pendientes += 1
            elif solicitud["estado"] == "En proceso":
                cantidad_en_proceso += 1
            elif solicitud["estado"] == "Resuelta":
                cantidad_resueltas += 1

        print("-" * 60)
        print(f"Total de solicitudes: {len(self.solicitudes)}")
        print(f"Pendientes: {cantidad_pendientes}")
        print(f"En proceso: {cantidad_en_proceso}")
        print(f"Resueltas: {cantidad_resueltas}")

    def ejecutar(self):
        while True:
            print("\nSISTEMA DE GESTIÓN DE SOLICITUDES ACADÉMICAS")
            print("1. Registrar solicitud")
            print("2. Cambiar estado")
            print("3. Asignar responsable")
            print("4. Buscar o filtrar solicitudes")
            print("5. Generar reporte básico")
            print("6. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.registrar_solicitud()
            elif opcion == "2":
                self.cambiar_estado()
            elif opcion == "3":
                self.asignar_responsable()
            elif opcion == "4":
                self.buscar_solicitudes()
            elif opcion == "5":
                self.generar_reporte()
            elif opcion == "6":
                print("Programa finalizado.")
                break
            else:
                print("La opción ingresada no es válida.")


if __name__ == "__main__":
    sistema = SistemaSolicitudes()
    sistema.ejecutar()