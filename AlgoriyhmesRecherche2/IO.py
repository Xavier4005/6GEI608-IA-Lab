from pathlib import Path
from puzzle import Puzzle
import numpy as np
import numpy.typing as npt
from resultat import Resultat

TAILLE_GRILLE : int = 9

class IO:

    @staticmethod
    def read_file(path: str | Path) -> Puzzle:
        path = Path(path)

        with open(path, "r", encoding="utf-8-sig") as f:
            lignes: list[str] = [
                ligne.strip() for ligne in f
            ]

        lignes = [ligne for ligne in lignes if ligne != ""]

        caracteres: list[str] = []
        metadonnees: dict[str, str] = {}

        for ligne in lignes:
            if ":" in ligne:
                cle, valeur = ligne.split(":", 1)
                metadonnees[cle.strip()] = valeur.strip()
            else:
                caracteres.extend(ch for ch in ligne if ch in ".0123456789")

        if len(caracteres) != TAILLE_GRILLE * TAILLE_GRILLE:
            raise ValueError(
                f"{path} : {len(caracteres)} cases lues, attendu "
                f"{TAILLE_GRILLE * TAILLE_GRILLE} (un seul puzzle par fichier, sans la solution)"
            )

        data: npt.NDArray[np.int32] = np.array(
            [0 if ch in ".0" else int(ch) for ch in caracteres],
            dtype=np.int32
        ).reshape(TAILLE_GRILLE, TAILLE_GRILLE)

        nb_indices: int = int(np.count_nonzero(data))
        if "Number of Givens" in metadonnees and int(metadonnees["Number of Givens"]) != nb_indices:
            raise ValueError(
                f"{path} : {nb_indices} chiffres donnés lus, "
                f"mais les métadonnées en annoncent {metadonnees['Number of Givens']}"
            )

        #if get_number_conflic(data) != 0:
        #    raise ValueError(f"{path} : les chiffres donnés se contredisent déjà")

        return Puzzle(path.stem, data, metadonnees)


    @staticmethod
    def read_all(dossier: str | Path) -> list[Puzzle]:
        fichiers: list[Path] = sorted(Path(dossier).glob("*.txt"))

        if not fichiers:
            raise FileNotFoundError(f"Aucun fichier .txt dans « {dossier} »")

        return [IO.read_file(fichier) for fichier in fichiers]


    @staticmethod
    def write_file(
        path: str | Path,
        historique: list[tuple[int, int]],
        nombre_iterations: int,
        temps_execution: float
    ) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for numero_iteration, valeur in historique:
                f.write(f"{numero_iteration}\t{valeur}\n")

            f.write(f"{nombre_iterations}\n")
            f.write(f"{temps_execution}\n")


    @staticmethod
    def export_statistiques(
        dossier_resultats: str | Path,
        nom_input: str,
        nom_algorithme: str,
        numero_execution: int,
        historique: list[tuple[int, int]],
        nombre_iterations: int,
        temps_execution: float
    ) -> Path:

        dossier = Path(dossier_resultats) / nom_input / nom_algorithme

        dossier.mkdir(parents=True, exist_ok=True)

        fichier = dossier / f"execution_{numero_execution:02d}.txt"

        IO.write_file(
            fichier,
            historique,
            nombre_iterations,
            temps_execution
        )

        return fichier


    @staticmethod
    def grille_en_texte(grille: npt.NDArray[np.int32]) -> str:
        lignes: list[str] = []
        for l in range(TAILLE_GRILLE):
            if l in (3, 6):
                lignes.append("-------|-------|-------")
            valeurs = [str(v) if v != 0 else "." for v in grille[l]]
            lignes.append(" " + " | ".join(" ".join(valeurs[c:c + 3]) for c in (0, 3, 6)))
        return "\n".join(lignes)


    @staticmethod
    def write_solution(path: str | Path, puzzle: Puzzle, resultat: Resultat) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Puzzle : {puzzle.nom}\n")
            f.write(f"Difficulty : {puzzle.metadonnees.get('Difficulty', 'inconnue')}\n")
            f.write(f"Résolu : {'oui' if resultat.resolu else 'non'}\n")
            f.write(f"Redémarrages : {resultat.redemarrages}\n")
            f.write(f"Conflits finaux : {resultat.conflits_finaux}\n\n")
            f.write(f"{'Solution' if resultat.resolu else 'Meilleure grille trouvée'} :\n")
            f.write(IO.grille_en_texte(resultat.meilleure_grille) + "\n")