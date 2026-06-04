#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>

int argsc = 0;
int commandsHistorySize = 0;
char* commandsHistory[100];
char old_wd[1024];

void show_prompt() {
    // TODO: mostrar prompt
    printf("my-first-shell> ");
}

char* read_input() {
    char* line = NULL;
    size_t len = 0;
    if (getline(&line, &len, stdin) == -1) {
        free(line);
        exit(0);
    }
    return line;
}

char** parse_command(char* buf) {
    // TODO: parsear comando

    buf[strcspn(buf, "\n")] = 0; // Eliminar el salto de línea al final

    commandsHistory[commandsHistorySize] = strdup(buf);
    commandsHistorySize++;

    int buffer_size = 64;
    char** tokens = malloc(buffer_size * sizeof(char*));
    if (tokens == NULL) {
        perror("Error al asignar memoria");
        exit(1);
    }

    char* rest;

    char* token = strtok_r(buf, " \n", &rest);

    while(token != NULL) {
        tokens[argsc] = token;
        argsc++;
        token = strtok_r(NULL, " \n", &rest);
    }
    tokens[argsc] = NULL;

    for (int i = 0; i < argsc; i++) {
        if (tokens[i][0] == '$' && strlen(tokens[i]) > 1) {
            char* env_var = getenv(tokens[i] + 1);

            if (env_var != NULL) {
                tokens[i] = env_var;

            } else {
                tokens[i] = "";
            }
        }
    }

    return tokens;
}

void execute_command(char** cmd) {
    // TODO: ejecutar comando

    if (cmd[0] == NULL) {
        return;

    } else if (strcmp(cmd[0], "exit") == 0) {
        exit(0);

    } else if (strcmp(cmd[0], "cd") == 0) {
        char current_wd[1024];
        getcwd(current_wd, sizeof(current_wd));
        char* target = NULL;

        if (argsc > 2) {
            fprintf(stderr, "cd: demasiados argumentos\n");

        } else if (argsc == 1) {
            target = getenv("HOME");

        } else if (strcmp(cmd[1], "-") == 0) {
            if (strlen(old_wd) == 0) {
                fprintf(stderr, "cd: no hay directorio anterior\n");
                return;
            }
            target = old_wd;
            printf("%s\n", target);

        } else {
            target = cmd[1];

        }

        if (chdir(target) == -1) {
            fprintf(stderr, "cd: %s: directorio no encontrado\n", target);

        } else {
            strcpy(old_wd, current_wd);
        }
        
        return;

    } else if (strcmp(cmd[0], "pwd") == 0) {
        char wd[1024];

        getcwd(wd, sizeof(wd));
        printf("%s\n", wd);

        return;

    } else if (strcmp(cmd[0], "history") == 0) {
        for (int i = 0; i < commandsHistorySize; i++) {
            printf("%i %s\n", i + 1, commandsHistory[i]);
        }
        return;

    } else if (strcmp(cmd[0], "export") == 0) {
        if (argsc < 2) {
            fprintf(stderr, "export: se requiere un argumento\n");

        } else if (argsc > 2) {
            fprintf(stderr, "export: demasiados argumentos\n");

        } else {
            char* rest;

            char* name = strtok_r(cmd[1], "=", &rest);
            char* value = strtok_r(NULL, "=", &rest);

            if (name == NULL || value == NULL) {
                fprintf(stderr, "export: formato inválido, se esperaba 'NOMBRE=VALOR'\n");
                return;
            }

            if (setenv(name, value, 1) == -1) {
                fprintf(stderr, "export: no se pudo definir la variable '%s' con el valor '%s'\n", name, value);
            }
        }
        return;

    } else if (strcmp(cmd[0], "unset") == 0) {
        if (argsc < 2) {
            fprintf(stderr, "unset: se requiere un argumento\n");

        } else if (argsc > 2) {
            fprintf(stderr, "unset: demasiados argumentos\n");

        } else {
            if (unsetenv(cmd[1]) == -1) {
                fprintf(stderr, "unset: no se pudo eliminar la variable '%s'\n", cmd[1]);
            }
        }
        return;
    }

    pid_t pid = fork();

    if (pid == 0) {
        if (execvp(cmd[0], cmd) == -1) {
            fprintf(stderr, "Comando no encontrado\n");
        }
        exit(1);
    } else {
        int status;
        waitpid(pid, &status, 0);
    }
}

int main() {
  while (1) {
    show_prompt();
    char* buf = read_input();
    char** cmd = parse_command(buf);
    execute_command(cmd);
    free(buf);
    free(cmd);
    argsc = 0;
  }
  return 0;
}
