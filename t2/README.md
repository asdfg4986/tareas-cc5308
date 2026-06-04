# Starter kit Tarea 2 — SAPO en Python

Estructura mínima para partir la Tarea 2 en Python. No implementa los comandos: deja funciones y `TODOs`.

## Construcción

```bash
make
```

Esto crea un ejecutable `./sapo` copiando `sapo.py`.

## Uso

```bash
./sapo --help
./sapo ps help
./sapo find help
./sapo files help
./sapo ports help
./sapo kill help
```

## Subcomandos esperados

```bash
./sapo ps
./sapo ps --all
./sapo find <pattern>
./sapo files <PID>
./sapo ports
./sapo kill <PID>
./sapo kill --signal TERM <PID>
```

## Restricción importante

La implementación de `sapo` no debe invocar comandos existentes de Linux como `ps`, `lsof`, `ss`, `netstat` o `kill`.

Sí pueden usar esos comandos manualmente durante el desarrollo para comparar resultados.

## Hitos sugeridos

1. Completar ayuda y parsing de opciones.
2. Recorrer `/proc` y detectar directorios numéricos.
3. Leer `/proc/<PID>/status` y `/proc/<PID>/cmdline`.
4. Implementar `sapo ps`.
5. Reutilizar la lectura de procesos para `sapo find`.
6. Leer `/proc/<PID>/fd` para `sapo files`.
7. Parsear `/proc/net/tcp` y `/proc/net/udp`.
8. Cruzar sockets por inode con `/proc/<PID>/fd`.
9. Implementar `sapo kill` usando `pidfd_open` y `pidfd_send_signal`.
