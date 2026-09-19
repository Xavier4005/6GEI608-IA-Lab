# Eliel

from pathlib import Path
import numpy.typing as npt
import numpy as np

MATRIX_DIM = 3


class IO:

    @staticmethod
    def write_file(
        path: str | Path,
        tailles_frontiere: list[tuple[int, int]],
        nombre_etats: int,
        temps_execution: float
    ) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for numero_iteration, taille_frontiere in tailles_frontiere:
                f.write(f"{numero_iteration}\t{taille_frontiere}\n")

            f.write(f"{nombre_etats}\n")
            f.write(f"{temps_execution}\n")


    @staticmethod
    def export_statistiques(
        dossier_resultats: str | Path,
        nom_input: str,
        nom_algorithme: str,
        numero_execution: int,
        tailles_frontiere: list[tuple[int, int]],
        nombre_etats: int,
        temps_execution: float
    ) -> Path:

        dossier = Path(dossier_resultats) / nom_input / nom_algorithme

        dossier.mkdir(parents=True, exist_ok=True)

        fichier = dossier / f"execution_{numero_execution:02d}.txt"

        IO.write_file(
            fichier,
            tailles_frontiere,
            nombre_etats,
            temps_execution
        )

        return fichier


    @staticmethod
    def write_solution(path: str | Path, actions: list[str]) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for action in actions:
                f.write(f"{action}\n")


    @staticmethod
    def read_file(path: str | Path) -> npt.NDArray[np.int32]:
        with open(path, "r", encoding="utf-8-sig") as f:
            lignes: list[str] = [
                ligne.rstrip("\r\n") for ligne in f
            ]

        lignes = [ligne for ligne in lignes if ligne != ""]

        grille: list[list[int]] = []

        for ligne in lignes:
            cases: list[str] = ligne.split("\t")

            grille.append([
                int(case) if case.strip() != "" else 0
                for case in cases
            ])

        data: npt.NDArray[np.int32] = np.array(
            grille,
            dtype=np.int32
        )

        if data.shape != (MATRIX_DIM, MATRIX_DIM):
            raise ValueError(
                f"{path} : grille de taille {data.shape}, "
                f"attendu {MATRIX_DIM}x{MATRIX_DIM}"
            )

        if sorted(data.flatten().tolist()) != list(
            range(MATRIX_DIM * MATRIX_DIM)
        ):
            raise ValueError(
                f"{path} : la grille doit contenir chaque valeur "
                f"de 0 à {MATRIX_DIM * MATRIX_DIM - 1} une seule fois"
            )

        return data