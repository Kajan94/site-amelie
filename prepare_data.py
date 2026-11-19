"""Extraire la base SQLite complète fournie avec le projet."""

from pathlib import Path
from shutil import copyfileobj
from tempfile import TemporaryDirectory
from zipfile import ZipFile


def prepare_database(root=None):
    root = Path(root) if root is not None else Path(__file__).resolve().parent
    relative_path = 'model/data/debase_db.sqllite3'
    target = root / relative_path
    if target.is_file():
        return target

    archive_path = root / 'site-amelie.zip'
    if not archive_path.is_file():
        raise FileNotFoundError(
            'Base complète introuvable : conserver site-amelie.zip à la racine '
            'du projet ou placer la base dans model/data/debase_db.sqllite3.'
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path) as archive:
        with TemporaryDirectory(dir=target.parent) as directory:
            temporary_file = Path(directory) / target.name
            with archive.open(f'SAE 1.01/{relative_path}') as source, temporary_file.open('wb') as output:
                copyfileobj(source, output)
            temporary_file.replace(target)
    return target


def main():
    print(f'Base complète disponible : {prepare_database()}')


if __name__ == '__main__':
    main()
