#!/usr/bin/env python3
"""Starter kit SAPO en Python.

Este archivo entrega estructura de subcomandos y TODOs. No implementa la tarea.
Restriccion: la implementacion final no debe invocar comandos como ps, lsof,
ss, netstat o kill.
"""

from __future__ import annotations

import sys
import os
import pwd
import fnmatch
import signal

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
""", file=out)


def print_find_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo find <pattern>

Busca procesos cuyo nombre o comando coincidan con el patron.
Soporta el uso de globs (ej: *python*, bash?, init*),
para usarlo debe poner el patron entre comillas.""", file=out)


def print_files_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo files <PID>

Lista archivos, pipes, sockets u otros recursos abiertos por PID.""", file=out)


def print_ports_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo ports

Lista puertos TCP/UDP abiertos indicando el proceso asociado.""", file=out)


def print_kill_help(out=sys.stdout) -> None:
    print("""Uso:
  sapo kill [opciones] <PID>

Opciones sugeridas:
  -s, --signal <SIG>  Senal a enviar. Ej: TERM, KILL, 15, 9
""", file=out)

def get_processes(uid_searched: int | None = None) -> list[dict]: 
    processes = []  # lista de diccionarios con info de procesos

    try:
        proc_entries = os.listdir("/proc")
    except Exception as e:
        print(f"sapo ps: error al leer /proc: {e}", file=sys.stderr)
        return SAPO_ERROR
    
    for pid in proc_entries:
        if not pid.isdigit():
            continue
    
        status_path = f"/proc/{pid}/status"
        cmdline_path = f"/proc/{pid}/cmdline"

        try:
            process_uid = -1
            process_name = ""
            with open(status_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("Uid:"):
                        process_uid = int(line.split()[1])
                    elif line.startswith("Name:"):
                        process_name = line.split()[1]

            if uid_searched is not None and process_uid != uid_searched:
                continue

            user_name = ""
            if process_uid != -1:
                try:
                    user_name = pwd.getpwuid(process_uid).pw_name
                except KeyError:
                    user_name = str(process_uid)

            command = ""
            with open(cmdline_path, "r", encoding="utf-8") as f:
                cmd = f.read()
                if cmd:
                    command = cmd.replace("\0", " ").strip()
                else:
                    command = f"[{process_name}]"

            processes.append({
                "pid": pid,
                "user": user_name,
                "name": process_name,
                "command": command,
            })

        except Exception as e:
            print(f"sapo ps: error al procesar PID {pid}: {e}", file=sys.stderr)
            continue

    return processes


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
        
    my_uid = os.getuid()
    processes = get_processes(None if show_all else my_uid)

    print(f"{'PID':<8} {'USER':<12} {'NAME':<20} {'COMMAND'}")

    for proc in processes:
        command_text = proc["command"]
        if len(command_text) > 60:
            command_text = command_text[:57] + "..."
        print(f"{proc['pid']:<8} {proc['user']:<12} {proc['name']:<20} {command_text}")

    return SAPO_OK


def cmd_find(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_find_help()
        return SAPO_OK
    if len(argv) != 1:
        print("sapo find: falta <pattern>", file=sys.stderr)
        print_find_help(sys.stderr)
        return SAPO_USAGE
    
    pattern = argv[0]

    processes = get_processes()
    coincidences = []
    for proc in processes:
        if fnmatch.fnmatch(proc["name"], pattern) or fnmatch.fnmatch(proc["command"], pattern):
            coincidences.append(proc)

    if not coincidences:
        print(f"sapo find: no se encontraron procesos que coincidan con '{pattern}'", file=sys.stderr)
        return SAPO_OK
    
    print(f"{'PID':<8} {'USER':<12} {'NAME':<20} {'COMMAND'}")

    for proc in coincidences:
        command_text = proc["command"]
        if len(command_text) > 60:
            command_text = command_text[:57] + "..."
        print(f"{proc['pid']:<8} {proc['user']:<12} {proc['name']:<20} {command_text}")

    return SAPO_OK


def cmd_files(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_files_help()
        return SAPO_OK
    if len(argv) != 1:
        print("sapo files: falta <PID>", file=sys.stderr)
        print_files_help(sys.stderr)
        return SAPO_USAGE

    pid = parse_pid(argv[0])
    fd_path = f"/proc/{pid}/fd"

    try:
        fd_entries = os.listdir(fd_path)
    except FileNotFoundError:
        print(f"sapo files: el proceso {pid} no existe o ya terminó.", file=sys.stderr)
        return SAPO_ERROR
    except PermissionError:
        print(f"sapo files: permiso denegado para inspeccionar el PID {pid}.", file=sys.stderr)
        return SAPO_ERROR
    except OSError as e:
        print(f"sapo files: error al acceder a {fd_path}: {e}", file=sys.stderr)
        return SAPO_ERROR
    
    files = []
    
    for fd in fd_entries:
        if not fd.isdigit():
            continue

        link_path = f"{fd_path}/{fd}"

        try:
            dest = os.readlink(link_path)
            files.append({
                "fd": fd,
                "target": dest,
            })
        except Exception as e:
            continue

    files.sort(key=lambda x: x["fd"])

    print(f"{'FD':<6} {'TARGET'}")

    for f in files:
            print(f"{f['fd']:<6} {f['target']}")

    return SAPO_OK

def read_red_file(path: str, protocol: str) -> dict:
    inodes_red = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()[1:]  # saltar header
            for line in lines:
                parts = line.split()
                if len(parts) < 10:
                    continue
                local_address = parts[1]
                state = parts[3]
                inode = parts[9]
                try:
                    ip_hex, port_hex = local_address.split(":")
                    ip = ".".join(str(int(ip_hex[i:i+2], 16)) for i in range(0, 8, 2))
                    port = int(port_hex, 16)
                    inodes_red[inode] = {
                        "protocol": protocol,
                        "ip": ip,
                        "port": port,
                        "state": state,
                    }
                except Exception:
                    continue
    except Exception as e:
        pass # si no se puede leer el archivo, simplemente no se agregan entradas

    return inodes_red

def get_inodes_processes() -> dict:
    inodes_processes = {}
    try:
        pids = os.listdir("/proc")
    except Exception as e:
        print(f"sapo ports: error al leer /proc: {e}", file=sys.stderr)
        return inodes_processes
    
    for pid in pids:
        if not pid.isdigit():
            continue

        process_name = ""
        try:
            with open(f"/proc/{pid}/status", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("Name:"):
                        process_name = line.split()[1]
                        break
        except Exception as e:
            process_name = "unknown"

        fd_path = f"/proc/{pid}/fd"
        try:
            fds = os.listdir(fd_path)
        except Exception as e:
            continue

        for fd in fds:
            try:
                link = os.readlink(f"{fd_path}/{fd}")
                if link.startswith("socket:[") and link.endswith("]"):
                    inode = link[8:-1]
                    inodes_processes[inode] = {
                        "pid": pid,
                        "process_name": process_name,
                    }
            except Exception as e:
                continue

    return inodes_processes

def cmd_ports(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_ports_help()
        return SAPO_OK
    if argv:
        print("sapo ports: no recibe argumentos", file=sys.stderr)
        print_ports_help(sys.stderr)
        return SAPO_USAGE

    tcp_connections = read_red_file("/proc/net/tcp", "TCP")
    udp_connections = read_red_file("/proc/net/udp", "UDP")

    all_connections = tcp_connections | udp_connections

    inodes_processes = get_inodes_processes()

    tcp_state_map = {
        "01": "ESTABLISHED",
        "02": "SYN_SENT",
        "03": "SYN_RECV",
        "04": "FIN_WAIT1",
        "05": "FIN_WAIT2",
        "06": "TIME_WAIT",
        "07": "CLOSE",
        "08": "CLOSE_WAIT",
        "09": "LAST_ACK",
        "0A": "LISTEN",
        "0B": "CLOSING",
    }

    print(f"{'PROTO':<6} {'LOCAL_ADDRESS':<22} {'STATE':<12} {'PID/PROCESS'}")

    for inode, red_info in all_connections.items():
        protocol = red_info["protocol"]
        ip = red_info["ip"]
        port = red_info["port"]
        state_hex = red_info["state"]
        
        address = f"{ip}:{port}"

        state = tcp_state_map.get(state_hex, state_hex) if protocol == "TCP" else ""

        process_info = inodes_processes.get(inode)
        if process_info:
            process_text = f"{process_info['pid']}/{process_info['process_name']}"
        else:
            process_text = "unknown"

        print(f"{protocol:<6} {address:<22} {state:<12} {process_text}")
    
    return SAPO_OK


def cmd_kill(argv: list[str]) -> int:
    if argv and is_help_arg(argv[0]):
        print_kill_help()
        return SAPO_OK

    signal_arg = "TERM"
    list_signals = False
    i = 0
    while i < len(argv):
        if argv[i] in {"-s", "--signal"} and i + 1 < len(argv):
            signal_arg = argv[i + 1]
            i += 2
        elif argv[i] in {"-l", "--list"}:
            list_signals = True
            i += 1
        else:
            break

    if list_signals:
        signals = sorted([s.name for s in signal.valid_signals() if hasattr(s, 'name')])
        for idx, sig in enumerate(signals, start=1):
            short_name = sig.replace("SIG", "")
            print(f"{short_name:>8}", end="")
            if idx % 5 == 0:
                print()

        print()
        return SAPO_OK

    if len(argv) - i != 1:
        print("sapo kill: falta <PID>", file=sys.stderr)
        print_kill_help(sys.stderr)
        return SAPO_USAGE

    pid = parse_pid(argv[i])
    
    sig_num = -1
    if signal_arg.isdigit():
        sig_num = int(signal_arg)
    else:
        sig_name = signal_arg.upper()
        if not sig_name.startswith("SIG"):
            sig_name = "SIG" + sig_name
        try:
            sig_num = getattr(signal, sig_name)
        except AttributeError:
            print(f"sapo kill: señal desconocida: {signal_arg}", file=sys.stderr)
            return SAPO_ERROR
        
    try:
        fd = os.pidfd_open(pid, 0)

        try:
            signal.pidfd_send_signal(fd, sig_num)
        finally:
            os.close(fd)

    except ProcessLookupError:
        print(f"sapo kill: el proceso {pid} no existe o ya terminó.", file=sys.stderr)
        return SAPO_ERROR
    except PermissionError:
        print(f"sapo kill: permiso denegado para enviar señal al PID {pid}.", file=sys.stderr)
        return SAPO_ERROR
    except OSError as e:
        print(f"sapo kill: error al enviar señal al PID {pid}: {e}", file=sys.stderr)
        return SAPO_ERROR

    return SAPO_OK

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
