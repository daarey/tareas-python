# Tareas Python

Una lista de tareas desde la terminal, con almacenamiento local en JSON y sin dependencias externas. Requiere Python 3.10 o posterior.

## Uso

```sh
python tareas.py agregar "Estudiar Python"
python tareas.py listar
python tareas.py completar 1
python tareas.py listar --pendientes
```

Los datos se guardan en `.tareas-python/tareas.json` dentro de tu carpeta de usuario. Puedes elegir otro archivo; la opción va antes del comando:

```sh
python tareas.py --archivo mis-tareas.json agregar "Leer documentación"
```

Las tareas vacías y los identificadores inexistentes se rechazan. Si el archivo está dañado, el programa informa del error sin sobrescribirlo. Las escrituras utilizan un archivo temporal para evitar dejar un JSON incompleto. Utiliza una instancia del programa a la vez.

## Pruebas

```sh
python -m unittest -v
```
