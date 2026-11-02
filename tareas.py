"""Lista de tareas local, sin dependencias externas."""
import argparse
import json
import os
from pathlib import Path
import tempfile


def load_tasks(path):
    if not path.exists():
        return []
    tasks = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(tasks, list) or any(
        not isinstance(task, dict)
        or type(task.get("id")) is not int
        or not isinstance(task.get("text"), str)
        or type(task.get("done")) is not bool
        for task in tasks
    ):
        raise ValueError("El archivo no contiene una lista de tareas válida.")
    if len({task["id"] for task in tasks}) != len(tasks):
        raise ValueError("El archivo contiene identificadores duplicados.")
    return tasks


def save_tasks(path, tasks):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(tasks, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archivo", type=Path,
                        default=Path.home() / ".tareas-python" / "tareas.json")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("agregar", help="Añadir una tarea")
    add.add_argument("texto")
    listing = commands.add_parser("listar", help="Ver las tareas")
    listing.add_argument("--pendientes", action="store_true")
    done = commands.add_parser("completar", help="Marcar una tarea completada")
    done.add_argument("id", type=int)
    args = parser.parse_args(argv)
    try:
        tasks = load_tasks(args.archivo)
        if args.command == "agregar":
            text = args.texto.strip()
            if not text:
                parser.error("La tarea no puede estar vacía.")
            task_id = max((task["id"] for task in tasks), default=0) + 1
            tasks.append({"id": task_id, "text": text, "done": False})
            save_tasks(args.archivo, tasks)
            print(f"Tarea {task_id} agregada.")
        elif args.command == "listar":
            visible = [task for task in tasks if not args.pendientes or not task["done"]]
            if not visible:
                print("No hay tareas.")
            for task in visible:
                mark = "x" if task["done"] else " "
                print(f"{task['id']}. [{mark}] {task['text']}")
        else:
            task = next((task for task in tasks if task["id"] == args.id), None)
            if task is None:
                parser.error(f"No existe la tarea {args.id}.")
            task["done"] = True
            save_tasks(args.archivo, tasks)
            print(f"Tarea {args.id} completada.")
    except (OSError, ValueError) as error:
        parser.error(f"No se pudieron procesar las tareas: {error}")


if __name__ == "__main__":
    main()
