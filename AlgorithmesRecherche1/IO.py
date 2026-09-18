#Eliel

from pathlib import Path
import numpy.typing as npt
import numpy as np

MATRIX_DIM = 3


class IO:

    @staticmethod
    def write_file(path: str | Path, grilles: list[npt.NDArray[np.int32]]) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            for i, grille in enumerate(grilles):
                if i > 0:
                    f.write("\n")
                for ligne in grille:
                    f.write("\t".join("" if int(v) == 0 else str(int(v)) for v in ligne) + "\n")

    @staticmethod
    def read_file(path: str | Path) -> npt.NDArray[np.int32]:
        with open(path, "r", encoding="utf-8-sig") as f:
            lignes: list[str] = [ligne.rstrip("\r\n") for ligne in f]

        lignes = [ligne for ligne in lignes if ligne != ""]

        grille: list[list[int]] = []
        for ligne in lignes:
            cases: list[str] = ligne.split("\t")
            grille.append([int(case) if case.strip() != "" else 0 for case in cases])

        data: npt.NDArray[np.int32] = np.array(grille, dtype=np.int32)

        if data.shape != (MATRIX_DIM, MATRIX_DIM):
            raise ValueError(f"{path} : grille de taille {data.shape}, attendu {MATRIX_DIM}x{MATRIX_DIM}")
        if sorted(data.flatten().tolist()) != list(range(MATRIX_DIM * MATRIX_DIM)):
            raise ValueError(f"{path} : la grille doit contenir chaque valeur de 0 à {MATRIX_DIM * MATRIX_DIM - 1} une seule fois")

        return data