import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import tareas


class TasksTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "tareas.json"

    def run_command(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            tareas.main(["--archivo", str(self.path), *args])
        return output.getvalue()

    def test_persistence_completion_and_filter(self):
        self.run_command("agregar", "Aprender Python")
        self.run_command("agregar", "Revisar código")
        self.run_command("completar", "1")
        self.assertIn("1. [x] Aprender Python", self.run_command("listar"))
        pending = self.run_command("listar", "--pendientes")
        self.assertNotIn("Aprender Python", pending)
        self.assertIn("2. [ ] Revisar código", pending)

    def test_empty_task_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.run_command("agregar", "   ")
        self.assertFalse(self.path.exists())

    def test_missing_id_does_not_change_data(self):
        self.run_command("agregar", "Una tarea")
        original = self.path.read_bytes()
        with self.assertRaises(SystemExit):
            self.run_command("completar", "99")
        self.assertEqual(original, self.path.read_bytes())

    def test_invalid_data_is_preserved(self):
        for content in ("{invalid", json.dumps([{"id": "wrong"}])):
            self.path.write_text(content, encoding="utf-8")
            with self.assertRaises(SystemExit):
                self.run_command("agregar", "Otra tarea")
            self.assertEqual(content, self.path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
