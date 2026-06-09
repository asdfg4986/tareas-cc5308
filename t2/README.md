# Tarea 2 — SAPO en Python (Sistema Administrador de Procesos)

**Autor:** Franco Iturra H.

## Descripción
`sapo` es una herramienta de interfaz de línea de comandos (CLI) escrita en Python que emula el comportamiento de utilidades clásicas de administración de sistemas en Linux, tales como `ps`, `pgrep/find`, `lsof`, `ss`/`netstat` y `kill`. 

Esta implementación interactúa directamente con el pseudo-sistema de archivos `/proc` y utiliza llamadas al sistema nativas.

## Requisitos
* Entorno Linux (requerido para la estructura de `/proc` y las syscalls de señales).
* Python 3.9 o superior (esto debido a que utiliza el operador de unión de diccionarios `|`).

## Construcción

Para compilar la herramienta y generar el ejecutable, utiliza el archivo Makefile incluido:

```bash
make
```
Esto generará un archivo ejecutable `./sapo` con los permisos adecuados a partir del script original. Para limpiar el entorno, puedes usar `make clean`.

## Comandos Implementados

La herramienta proporciona los siguientes comandos. Puedes consultar la ayuda global ejecutando `./sapo -h` o `--help`, o la ayuda específica de cada comando con `./sapo <comando> help`.

1. `ps` - Lista de procesos  
Lista los procesos actuales en ejecución del sistema.  
Uso por defecto: `./sapo ps` (Muestra solo los procesos que pertenecen al usuario actual).  
Opciones: `./sapo ps -a` o `--all` (Muestra los procesos de todos los usuarios del sistema).  
2. `find` - Búsqueda de procesos  
Busca procesos cuyo nombre o comando de ejecución coincidan con un patrón específico.  
Permite el uso de globs para la búsqueda de patrones, para evitar la expansión automática de la shell, el patrón debe ir entre comillas.  
Ejemplos de uso: `./sapo find bash`, `./sapo find "*python"`
3. `files` - Recursos abiertos  
Muestra la lista de descriptores de archivo (FD) abiertos por un proceso específico y su destino.  
Uso: `./sapo files <PID>`
4. `ports` - Puertos de red  
Lista las conexiones TCP y UDP activas en el sistema y las cruza con el proceso que las mantiene abiertas.  
Uso: `./sapo ports` (Nota: al ejecutarse con `sudo` se ven los nombres de todos los procesos del sistema).
5. `kill` - Envío de señales  
Envía señales del sistema a un proceso en ejecución de manera segura.  
Si no se especifica una señal, envía `SIGTERM` (15) por defecto.  
Uso por defecto: `./sapo kill <PID>`  
Opciones de señal: `./sapo kill -s 9 <PID>` o `./sapo kill -s KILL <PID>`  
Lista de señales: `./sapo kill -l` o `--list` (Imprime una cuadricula con todas las señales disponibles en el sistema operativo).


## Decisiones de Diseño

Manejo de Concurrencia (OS): Todos los accesos a `/proc` están protegidos por bloques `try/except` asumiendo la naturaleza volátil de los procesos, los cuales pueden nacer o morir en milisegundos durante la lectura.