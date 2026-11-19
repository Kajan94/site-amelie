import sqlite3
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from prepare_data import prepare_database


class PrepareDatabaseTests(unittest.TestCase):
    def test_extracts_existing_database(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "original.sqlite"
            with sqlite3.connect(source) as connection:
                connection.execute("CREATE TABLE verification (valeur INTEGER)")
                connection.execute("INSERT INTO verification VALUES (42)")
            with ZipFile(root / "site-amelie.zip", "w") as archive:
                archive.write(source, "SAE 1.01/model/data/debase_db.sqllite3")
            target = prepare_database(root)
            self.assertEqual(target.read_bytes(), source.read_bytes())
            with sqlite3.connect(target) as connection:
                self.assertEqual(connection.execute("SELECT valeur FROM verification").fetchone(), (42,))

    def test_preserves_existing_file_without_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "model/data/debase_db.sqllite3"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"existing data")
            self.assertEqual(prepare_database(root), target)
            self.assertEqual(target.read_bytes(), b"existing data")

    def test_explains_missing_database(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FileNotFoundError, "site-amelie.zip"):
                prepare_database(Path(directory))


if __name__ == "__main__":
    unittest.main()
