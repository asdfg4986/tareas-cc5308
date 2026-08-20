# Repositorio de Tareas — CC5308 Administracion de Sistemas Linux

**Autor:** Franco Iturra H.

## Descripcion

Este repositorio contiene los proyectos practicos desarrollados para el curso CC5308. Las tareas se centran en la interaccion directa con la API del sistema operativo Linux, la gestion del ciclo de vida de los procesos, el manejo de memoria y el analisis de recursos del sistema a bajo nivel.

## Estructura del Repositorio

**t1/** : Interprete de Comandos (Shell) Minimalista
Una shell interactiva escrita en C. Implementa la lectura y parseo de comandos, creacion y sincronizacion de procesos (mediante llamadas al sistema como fork, waitpid y execvp) y comandos integrados nativos (built-ins) como cd, export, unset y history. Utiliza gestion dinamica de memoria para la tokenizacion segura.

**t2/** : SAPO (System Analyzer for Processes and Open resources)
Una herramienta CLI escrita en Python para la auditoria de sistemas Linux. Interactua directamente con el pseudo-sistema de archivos /proc para emular utilidades clasicas como ps, find, lsof (files), netstat (ports) y kill. Destaca por el mapeo cruzado de descriptores de archivos (fd) con sockets de red y el envio seguro de señales utilizando llamadas modernas como pidfd_open para evitar condiciones de carrera.

## Requisitos Generales

- Entorno Linux (distribucion compatible con POSIX y la estructura virtual de /proc).
- Compilador de C (gcc o clang) y GNU Make para compilar la Tarea 1.
- Python 3.9 o superior para ejecutar la Tarea 2.

## Instrucciones de Uso

Cada directorio contiene su propio archivo Makefile y un README dedicado con instrucciones detalladas de compilacion, ejecucion y arquitectura.

Para probar cualquiera de las herramientas, navega al directorio correspondiente y consulta su documentacion especifica.

Para la Tarea 1:
```bash
cd t1
make run
```

Para la Tarea 2:
```bash
cd t2
./sapo help
```
