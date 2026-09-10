# Diagnóstico de calidad del sistema inicial

## Objetivo

El objetivo de este diagnóstico es analizar la calidad interna de la versión inicial del Sistema de Gestión de Solicitudes Académicas, identificando deuda técnica y code smells que puedan dificultar su mantenimiento y evolución.

Aunque las funcionalidades principales fueron verificadas correctamente, el código se encuentra concentrado principalmente en el archivo `src/main.py`. Esto genera oportunidades de mejora relacionadas con la distribución de responsabilidades, la duplicación de código y el acoplamiento.

## Problemas detectados

| N.º | Problema detectado | Ubicación | Consecuencia | Prioridad |
|---|---|---|---|---|
| 1 | Large Class o God Class | Clase `SistemaSolicitudes` | Concentra demasiadas responsabilidades | Alta |
| 2 | Long Method | Método `registrar_solicitud` | Dificulta la lectura, modificación y prueba | Alta |
| 3 | Código duplicado | Búsqueda por número en diferentes métodos | Una modificación debe repetirse en varios lugares | Alta |
| 4 | Long Parameter List | Constructor de `Solicitud` | Aumenta la posibilidad de errores al crear objetos | Media |
| 5 | Primitive Obsession | Estados y prioridades representados mediante textos | Permite valores inconsistentes o inválidos | Media |
| 6 | Data Class | Entidades con escaso comportamiento propio | La lógica termina concentrada en otras clases | Media |
| 7 | Acoplamiento con JSON | Lectura y escritura realizadas desde el sistema | Dificulta cambiar la forma de almacenamiento | Alta |
| 8 | Condicionales extensos | Menú y métodos de búsqueda | Dificultan agregar nuevas opciones | Media |

## Priorización

Los problemas de mayor prioridad son la concentración de responsabilidades, los métodos extensos, la duplicación de código y el acoplamiento directo con el archivo JSON.

Estas situaciones serán tratadas mediante la separación del sistema en componentes más pequeños, la extracción de métodos, la centralización de búsquedas y la creación de una clase específica para la persistencia.

## Conclusión

La versión inicial cumple con las funcionalidades solicitadas y presenta una calidad externa adecuada. Sin embargo, su calidad interna puede mejorarse mediante la aplicación de principios SOLID, Clean Code y técnicas de refactoring.

Las mejoras deberán conservar el comportamiento externo ya verificado y serán acompañadas por pruebas para comprobar que el sistema continúa funcionando correctamente.