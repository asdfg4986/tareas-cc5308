## Archivos

- `shell.c`: El código fuente del programa.
- `Makefile`: Un makefile para simplificar el proceso de compilación y ejecución del shell.
- `README.md`: Un archivo con las instrucciones para compilar y ejecutar el programa.

## Funcionalidades Avanzadas Implementadas
1. **cd mejorado:** Implementación de `cd` sin argumentos (lleva al home directory) y `cd -` (regresa al directorio anterior).
2. **Sustitucion de variables de entorno:** Implementación de sustitución de variables de entorno usando `$NOMBRE`.

## Instrucciones

Para compilar el programa y generar el ejecutable `./shell`, utiliza el siguiente comando:

```bash
make
```

Si deseas compilar y ejecutar el programa en un solo paso, puedes utilizar:

```bash
make run
```

Para eliminar el archivo compilado, utilice el siguiente comando:

```bash
make clean
```
