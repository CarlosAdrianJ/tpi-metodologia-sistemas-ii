# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de Metodología de Sistemas II.

## Alumno

Carlos Jabazze

## Descripción

El proyecto implementa un sistema de consola para registrar y administrar solicitudes académicas realizadas por estudiantes. Permite controlar su prioridad, estado y responsable, realizar búsquedas y conservar la información mediante un archivo JSON.

El sistema fue desarrollado inicialmente en una única clase y posteriormente refactorizado aplicando principios SOLID, Clean Code y técnicas de refactoring seguro.

## Funcionalidades

- Registrar solicitudes académicas.
- Asignar tipo y prioridad.
- Cambiar el estado de una solicitud.
- Asignar un responsable o área.
- Buscar y filtrar solicitudes.
- Generar un reporte básico.
- Guardar y recuperar información en formato JSON.
- Detectar errores en archivos JSON inválidos.

## Arquitectura

La versión refactorizada distribuye las responsabilidades entre diferentes módulos:

- `modelos.py`: entidades, enumeraciones y comportamiento del dominio.
- `repositorio.py`: contrato de persistencia e implementación mediante JSON.
- `servicio.py`: operaciones y reglas principales del sistema.
- `consola.py`: interacción con el usuario y presentación de resultados.
- `main.py`: creación y conexión de los componentes.

## Estructura del proyecto

```text
datos/
    solicitudes.json
docs/
    diagnostico.md
    evidencias/
src/
    __init__.py
    consola.py
    main.py
    modelos.py
    repositorio.py
    servicio.py
tests/
    test_solicitudes.py
.gitignore
README.md