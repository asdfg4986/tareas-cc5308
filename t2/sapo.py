#!/usr/bin/env python3
"""Starter kit SAPO en Python.

Este archivo entrega estructura de subcomandos y TODOs. No implementa la tarea.
Restriccion: la implementacion final no debe invocar comandos como ps, lsof,
ss, netstat o kill.
"""

from __future__ import annotations

import sys
import os

SAPO_OK = 0
SAPO_ERROR = 1
SAPO_USAGE = 2


def is_help_arg(arg: str | None) -> bool:
    return arg in {"help", "-h", "--help"}


def parse_pid(text: str) -> int:
    try:
        pid = int(text, 10)
    except ValueError:
        print(f"sapo: PID invalido: {text}", file=sys.stderr)
        raise SystemExit(SAPO_USAGE)
    if pid <= 0:
        print(f"sapo: PID invalido: {text}", file=sys.stderr)
        raise SystemExit(SAPO_USAGE)
    return pid


def print_global_help(out=sys.stdout) -> None:
    print(
        """Uso:
  sapo <comando> [opciones]

Comandos:
  ps                 Lista procesos del usuario actual
  find <pattern>     Busca procesos por nombre o comando
  files <PID>        Lista recursos abiertos por un proceso
  ports              Lista puertos TCP/UDP abiertos y procesos asociados
  kill <PID>         Envia una senal a un proceso usando pidfd

Ayuda:
  sapo -h | --help
  sapo <comando> help""",
        file=out,
    )


def print_ps_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo ps [opciones]

Opciones:
  -a, --all          Muestra procesos de todos los usuarios

Debe leer informacion desde /proc.""", file=out)


def print_find_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo find <pattern>

Busca procesos cuyo nombre o comando coincidan con el patron.
Documenten si usan regex o globs.""", file=out)


def print_files_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo files <PID>

Lista archivos, pipes, sockets u otros recursos abiertos por PID.
Debe inspeccionar /proc/<PID>/fd.""", file=out)


def print_ports_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo ports

Lista puertos TCP/UDP abiertos indicando el proceso asociado.
Debe cruzar /proc/net/tcp|udp con /proc/<PID>/fd usando inodes.""", file=out)


def print_kill_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo kill [opciones] <PID>

Opciones sugeridas:
  -s, --signal <SIG>  Senal a enviar. Ej: TERM, KILL, 15, 9

Debe usar pidfd_open y pidfd_send_signal.""", file=out)


def cmd_ps(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_ps_help()
        return SAPO_OK

    show_all = False
    for arg in argv:
        if arg in {"-a", "--all"}:
            show_all = True
        else:
            print(f"sapo ps: opcion desconocida: {arg}", file=sys.stderr)
            print_ps_help(sys.stderr)
            return SAPO_USAGE

    # TODO:
    # - recorrer /proc
    # - detectar entradas numericas
    # - leer /proc/<PID>/status
    # - leer /proc/<PID>/cmdline
    # - filtrar por UID actual salvo -a/--all
    # - imprimir tabla
    _ = show_all
    print("sapo ps: TODO implementar", file=sys.stderr)
    return SAPO_ERROR


def cmd_find(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_find_help()
        return SAPO_OK
    if len(argv) != 1:
        print("sapo find: falta <pattern>", file=sys.stderr)
        print_find_help(sys.stderr)
        return SAPO_USAGE

    pattern = argv[0]
    # TODO:
    # - reutilizar la lectura de procesos de sapo ps
    # - comparar pattern contra nombre y comando
    # - imprimir solo coincidencias
    _ = pattern
    print("sapo find: TODO implementar", file=sys.stderr)
    return SAPO_ERROR


def cmd_files(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_files_help()
        return SAPO_OK
    if len(argv) != 1:
        print("sapo files: falta <PID>", file=sys.stderr)
        print_files_help(sys.stderr)
        return SAPO_USAGE

    pid = parse_pid(argv[0])
    # TODO:
    # - abrir /proc/<PID>/fd
    # - recorrer entradas numericas
    # - usar os.readlink para obtener el destino de cada FD
    # - imprimir FD y destino
    _ = pid
    print("sapo files: TODO implementar", file=sys.stderr)
    return SAPO_ERROR


def cmd_ports(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_ports_help()
        return SAPO_OK
    if argv:
        print("sapo ports: no recibe argumentos", file=sys.stderr)
        print_ports_help(sys.stderr)
        return SAPO_USAGE

    # TODO:
    # - leer /proc/net/tcp y /proc/net/udp
    # - extraer protocolo, direccion local, puerto, estado e inode
    # - recorrer /proc/<PID>/fd de los procesos
    # - buscar links tipo socket:[INODE]
    # - cruzar inodes con procesos
    print("sapo ports: TODO implementar", file=sys.stderr)
    return SAPO_ERROR


def cmd_kill(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_kill_help()
        return SAPO_OK

    signal_arg = "TERM"
    i = 0
    while i < len(argv):
        if argv[i] in {"-s", "--signal"} and i + 1 < len(argv):
            signal_arg = argv[i + 1]
            i += 2
        else:
            break

    if len(argv) - i != 1:
        print("sapo kill: falta <PID>", file=sys.stderr)
        print_kill_help(sys.stderr)
        return SAPO_USAGE

    pid = parse_pid(argv[i])
    # TODO:
    # - convertir signal_arg a numero de senal
    # - abrir pidfd con os.pidfd_open o syscall equivalente
    # - enviar senal con signal.pidfd_send_signal o syscall equivalente
    # - cerrar pidfd
    _ = (pid, signal_arg)
    print("sapo kill: TODO implementar", file=sys.stderr)
    return SAPO_ERROR


def main(argv: list[str]) -> int:
    if len(argv) < 2 or is_help_arg(argv[1]):
        print_global_help()
        return SAPO_OK

    cmd = argv[1]
    sub_argv = argv[2:]
    commands = {
        "ps": cmd_ps,
        "find": cmd_find,
        "files": cmd_files,
        "ports": cmd_ports,
        "kill": cmd_kill,
    }
    if cmd not in commands:
        print(f"sapo: comando desconocido: {cmd}", file=sys.stderr)
        print_global_help(sys.stderr)
        return SAPO_USAGE
    return commands[cmd](sub_argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
