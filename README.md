# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de Metodología de Sistemas II.

## Alumno

Carlos Jabazze

## Descripción

El proyecto consiste en un sistema de consola que permite registrar y administrar solicitudes académicas realizadas por estudiantes.

## Funcionalidades

- Registrar solicitudes.
- Clasificar solicitudes por tipo, prioridad y estado.
- Cambiar el estado de una solicitud.
- Asignar un responsable o área.
- Buscar y filtrar solicitudes.
- Generar un reporte básico.

## Tecnologías

- Python
- JSON
- Git
- GitHub

## Requisitos

Python 3.10 o superior. No requiere instalar dependencias externas.

## Ejecución

Desde la carpeta principal:

```powershell
python -m src.main
```

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas utilizan archivos temporales y no modifican los datos del sistema.