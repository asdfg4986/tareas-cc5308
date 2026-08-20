# Tarea 1 — Interprete de Comandos (Shell) Minimalista

**Autor:** Franco Iturra H.

## Descripcion
shell es un interprete de comandos interactivo escrito en C que emula el comportamiento de una terminal UNIX. 

El programa presenta un prompt personalizado (my-first-shell> ), lee la entrada estandar, tokeniza los comandos y los ejecuta. Para los binarios externos, interactua directamente con la API del sistema operativo Linux gestionando el ciclo de vida de los procesos mediante llamadas al sistema nativas (fork, waitpid, execvp).

## Requisitos
- Entorno Linux (requerido para las syscalls de gestion de procesos POSIX).
- Compilador de C (ej. gcc o clang).
- Herramienta make para la construccion.

## Construccion y Ejecucion

Para compilar el programa y generar el ejecutable ./shell, utiliza el archivo Makefile incluido:
```bash
make
```

Si deseas compilar y ejecutar el programa inmediatamente en un solo paso, puedes utilizar:
```bash
make run
```

Para limpiar el entorno y eliminar los archivos binarios compilados, utiliza:
```bash
make clean
```

## Funcionalidades y Comandos Integrados (Built-ins)

Ademas de soportar la ejecucion de cualquier comando binario del sistema, la shell cuenta con los siguientes comandos integrados nativamente en su propio proceso:

**1. Navegacion de directorios (cd)**
- cd: Redirige automaticamente al directorio principal del usuario ($HOME).
-cd -: Regresa al directorio de trabajo anterior, llevando un registro del estado previo del sistema.
- cd <ruta>: Navega a la ruta especificada.

**2. Gestion del Entorno (export y unset)**
- export NOMBRE=VALOR: Permite definir o sobrescribir variables de entorno dinamicamente usando setenv.
- unset NOMBRE: Elimina variables de entorno activas utilizando unsetenv.

**3. Expansion de Variables de Entorno**
El interprete detecta el prefijo $ en los argumentos e inyecta dinamicamente el valor de la variable en tiempo de ejecucion (ej. echo $PATH).

**4. Historial de Comandos (history)**
Mantiene un registro en memoria de todos los comandos ingresados durante la sesion actual, los cuales pueden ser visualizados con el comando history.

**5. Utilidades del Sistema (pwd y exit)**
- pwd: Imprime la ruta del directorio de trabajo actual.
- exit: Termina de forma segura la ejecucion de la shell, liberando los recursos y cerrando el proceso (tambien soporta la salida mediante EOF / Ctrl+D).

## Estructura de Archivos
- shell.c: Codigo fuente central que contiene la logica de lectura (getline), parseo mediante punteros (strtok_r), bifurcacion de procesos y las rutinas de los comandos integrados.
- Makefile: Recetas para simplificar el proceso de compilacion, ejecucion y limpieza del proyecto.

## Decisiones de Diseño

- **Gestion de Procesos Externos:** La ejecucion de programas delega el trabajo a un proceso hijo mediante fork(), mientras la shell principal espera activamente su termino utilizando waitpid(). Esto garantiza que la terminal principal no muera si el comando hijo falla.
- **Ejecucion de Built-ins:** Comandos que modifican el estado de la shell (como cd, export o unset) se ejecutan intencionalmente en el proceso padre. Si se ejecutaran en un proceso hijo, las variables de entorno o el cambio de directorio se destruirian al terminar el hijo, haciendo inutiles los comandos.
- **Manejo de Memoria:** Se utiliza un arreglo dinamico de punteros para el almacenamiento del historial de comandos y la asignacion de tokens del buffer de entrada, garantizando que comandos con multiples argumentos se procesen correctamente sin desbordamientos estaticos basicos.
