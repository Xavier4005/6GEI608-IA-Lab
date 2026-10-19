from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np
import numpy.typing as npt
from timeit import default_timer as timer
from math import inf
import random
from itertools import combinations




def get_number_conflic(sudoku : npt.NDArray[np.int32]) -> int:
    lignes : list[int] = [0] * 9
    colonnes : list[int] = [0] * 9
    blocs : list[int] = [0] * 9

    nb_conflit : int = 0

    for (ligne, colonne), valeur in np.ndenumerate(sudoku):
        valeur_py = int(valeur)

        if valeur_py == 0:
            continue

        bloc : int = 3 * (ligne // 3) + (colonne // 3)

        masque : int = 1 << (valeur_py - 1)

        # Teste pour les lignes
        if (lignes[ligne] & masque) == 0:
            lignes[ligne] |=  masque
        else:
            nb_conflit += 1

        # Teste pour les colonnes
        if (colonnes[colonne] & masque) == 0:
            colonnes[colonne] |=  masque
        else:
            nb_conflit += 1

        # Teste pour les blocs
        if (blocs[bloc] & masque) == 0:
            blocs[bloc] |= masque
        else:
            nb_conflit += 1


    return nb_conflit

# Hill climbing (Eliel)


MAX_REDEMARRAGES : int = 100          # nombre maximal de redémarrages aléatoires


@dataclass
class Resultat:
    solution: npt.NDArray[np.int32] | None   # grille résolue, ou None en cas d'échec
    meilleure_grille: npt.NDArray[np.int32]   # meilleure grille rencontrée
    temps: float
    iterations: int
    redemarrages: int
    resolu: bool
    conflits_finaux: int
    historique: list[tuple[int, int]] = field(default_factory=list)
    voisins_evalues: int = 0


def doublons(valeurs : npt.NDArray[np.int32]) -> int:

    return 9 - len(set(valeurs.tolist()))


def bloc_de(grille : npt.NDArray[np.int32], ligne : int, colonne : int) -> npt.NDArray[np.int32]:
    l0, c0 = 3 * (ligne // 3), 3 * (colonne // 3)
    return grille[l0:l0 + 3, c0:c0 + 3].ravel()


def cout_local(grille : npt.NDArray[np.int32], ligne : int, c1 : int, c2 : int) -> int:

    cout = doublons(grille[:, c1]) + doublons(grille[:, c2])
    cout += doublons(bloc_de(grille, ligne, c1))
    if c1 // 3 != c2 // 3:
        cout += doublons(bloc_de(grille, ligne, c2))
    return cout


def cases_libres_par_ligne(sudoku : npt.NDArray[np.int32]) -> list[list[int]]:

    return [[c for c in range(9) if sudoku[l, c] == 0] for l in range(9)]


def remplir_lignes(sudoku : npt.NDArray[np.int32], libres : list[list[int]]) -> npt.NDArray[np.int32]:

    grille = sudoku.copy()
    for l in range(9):
        presents = set(sudoku[l][sudoku[l] != 0].tolist())
        manquants = [v for v in range(1, 10) if v not in presents]
        random.shuffle(manquants)
        grille[l, libres[l]] = manquants
    return grille


def successeurs(libres : list[list[int]]) -> list[tuple[int, int, int]]:
    return [(l, c1, c2) for l in range(9) for c1, c2 in combinations(libres[l], 2)]


def meilleur_successeur(grille : npt.NDArray[np.int32],
                        mouvements : list[tuple[int, int, int]]) -> tuple[int, tuple[int, int, int]]:
    meilleur_delta : int = 10 ** 9
    meilleurs : list[tuple[int, int, int]] = []

    for l, c1, c2 in mouvements:
        avant = cout_local(grille, l, c1, c2)
        grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]
        delta = cout_local(grille, l, c1, c2) - avant
        grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]

        if delta < meilleur_delta:
            meilleur_delta, meilleurs = delta, [(l, c1, c2)]
        elif delta == meilleur_delta:
            meilleurs.append((l, c1, c2))

    return meilleur_delta, random.choice(meilleurs)


def monter(grille : npt.NDArray[np.int32], mouvements : list[tuple[int, int, int]],
           historique : list[tuple[int, int]], iteration_depart : int) -> tuple[int, int, int]:
    cout = get_number_conflic(grille)
    iterations = 0
    voisins = 0
    historique.append((iteration_depart, cout))

    while mouvements:
        delta, (l, c1, c2) = meilleur_successeur(grille, mouvements)
        voisins += len(mouvements)

        if delta >= 0:
            break

        grille[l, c1], grille[l, c2] = grille[l, c2], grille[l, c1]
        cout += delta
        iterations += 1
        historique.append((iteration_depart + iterations, cout))

    return cout, iterations, voisins


def hill_climbing_resolve(sudoku : npt.NDArray[np.int32], graine : int | None = None) -> Resultat:

    if graine is not None:
        random.seed(graine)

    libres = cases_libres_par_ligne(sudoku)
    mouvements = successeurs(libres)

    start : float = timer()
    iterations : int = 0
    voisins : int = 0
    meilleure_grille = sudoku.copy()
    meilleur_cout : float = inf
    historique : list[tuple[int, int]] = []

    for redemarrage in range(MAX_REDEMARRAGES):
        grille = remplir_lignes(sudoku, libres)
        cout, it, v = monter(grille, mouvements, historique, iterations)
        iterations += it
        voisins += v

        if cout < meilleur_cout:
            meilleur_cout = cout
            meilleure_grille = grille.copy()

        if cout == 0:
            return Resultat(grille, grille, timer() - start, iterations, redemarrage,
                            True, 0, historique, voisins)

    return Resultat(None, meilleure_grille, timer() - start, iterations, MAX_REDEMARRAGES,
                    False, int(meilleur_cout), historique, voisins)

def generate_sudoku_aleatoire(sudoku : npt.NDArray[np.int32], lignes : npt.NDArray, colonnes : npt.NDArray) -> npt.NDArray[np.int32]:
    sudoku_rempli : npt.NDArray[np.int32] = np.random.randint(1, 10, sudoku.shape, np.int32)
    sudoku_rempli[lignes, colonnes] = sudoku[lignes, colonnes]

    return sudoku_rempli

def croisement_blocs(parent_A: npt.NDArray[np.int32], parent_B: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
    #Générer un masque 3x3 de booléens (True = Parent A, False = Parent B)
    masque_blocs = np.random.rand(3, 3) < 0.5

    #Étendre le masque à la taille 9x9 (chaque booléen est répété en matrice 3x3)
    masque_2d = np.kron(masque_blocs, np.ones((3, 3), dtype=bool))

    #Combiner les deux parents
    enfant = np.where(masque_2d, parent_A, parent_B)
    return enfant

@dataclass
class Individu:
    sudoku: npt.NDArray[np.int32]
    fitness: int

def genetic_resolve(sudoku : npt.NDArray[np.int32], frezz_number : set[tuple[int,int]]) -> npt.NDArray[np.int32] | None:
    # Variable de contrôle
    nombre_individue : int = 1000
    pourcentage_elitisme : int = 5
    nomtre_maximal_iteration : int = 10000

    population_actuelle : list[Individu] = list[Individu]()

    start: float = timer()

    # Transformation en tableux une seul fois pour la génération de toute les 1000 individue de la généation 1
    lignes_brut , colonnes_brut = zip(*frezz_number)
    lignes = np.array(lignes_brut)
    colonnes = np.array(colonnes_brut)

    # Création de la première population
    for _ in range(nombre_individue):
        sudoku_rempli : npt.NDArray[np.int32] = generate_sudoku_aleatoire(sudoku, lignes, colonnes)
        fitness = -get_number_conflic(sudoku_rempli)
        population_actuelle.append(Individu(sudoku_rempli, fitness))

    population_actuelle.sort(key=lambda ind: ind.fitness, reverse=True)

    # Génération des population suivante et arrêt quand résultat trouver

    # Génération de list de bloc pour les mutation
    #Dictionnaire pour grouper les cases libres par bloc (0 à 8)
    cases_libres_par_bloc : dict[int, list[tuple[int, int]]] = {i: [] for i in range(9)}

    # 2. Une seule liste globale de toutes les cases libres (utile pour l'inter-bloc)
    toutes_cases_libres : list[tuple[int, int]] = []

    for l in range(9):
        for c in range(9):
            pos = (l, c)
            if pos not in frezz_number:
                bloc = 3 * (l // 3) + (c // 3)
                cases_libres_par_bloc[bloc].append(pos)
                toutes_cases_libres.append(pos)

    # 3. Filtrer uniquement les blocs qui ont au moins 2 cases libres (pour le swap intra-bloc)
    blocs_mutables : list[int] = [b for b, cases in cases_libres_par_bloc.items() if len(cases) >= 2]

    # Variables de contrôle adaptatif
    taux_mutation_base : float = 0.10
    taux_mutation_actuel : float = taux_mutation_base
    seuil_stagnation : int = 50

    meilleure_fitness_precedente : int = population_actuelle[0].fitness
    compteur_stagnation : int = 0


    nombre_iteration : int = 1
    while population_actuelle[0].fitness != 0 and nombre_iteration < nomtre_maximal_iteration:
        population_suivante : list[Individu]
        # Garder le pourcentage a garder de la dernière génération
        nb_elites : int = int(len(population_actuelle) * (pourcentage_elitisme / 100))
        nb_elites = max(1, nb_elites)

        population_suivante = population_actuelle[:nb_elites]

        # Pour le reste des individue on vas faire du crosovers entre deux individie ou l'on choisie le meilleur entre 5 candida choisie aléatoirement pour chauqe parent
        # nous alons aussie faire des mutation alléatoire avec un pourcentage choisie

        for _ in range(nombre_individue - nb_elites):
            parent_A : Individu
            parent_B : Individu

            tournoi = random.sample(population_actuelle, 5)
            parent_A =  max(tournoi, key=lambda ind: ind.fitness)

            tournoi = random.sample(population_actuelle, 5)
            parent_B =  max(tournoi, key=lambda ind: ind.fitness)

            enfant : npt.NDArray[np.int32] = croisement_blocs(parent_A.sudoku, parent_B.sudoku).copy()

            # Appliquer la mutation
            # Choisir ci l'on fait une mutation
            if random.random() < taux_mutation_actuel:
                # 90% de chance de faire une permutation  dasn un bloc et 10% de chance de faire des lien interbloc
                if random.random() < 0.90 and blocs_mutables:
                    bloc_choisi : int = random.choice(blocs_mutables)
                    coords : list[tuple[int,int]] = random.sample(cases_libres_par_bloc[bloc_choisi], 2)
                else:
                    coords = random.sample(toutes_cases_libres, 2)

                enfant[coords[0]], enfant[coords[1]] = enfant[coords[1]], enfant[coords[0]]

            fitness = -get_number_conflic(enfant)
            population_suivante.append(Individu(enfant, fitness))

        population_actuelle = population_suivante
        population_actuelle.sort(key=lambda ind: ind.fitness, reverse=True)

        meilleure_fitness_actuelle = population_actuelle[0].fitness

        # Détection de la stagnation
        if meilleure_fitness_actuelle == meilleure_fitness_precedente:
            compteur_stagnation += 1
        else:
            compteur_stagnation = 0
            meilleure_fitness_precedente = meilleure_fitness_actuelle
            taux_mutation_actuel = taux_mutation_base

        # Si stagnation prolongée, on augmente le taux de mutation
        if compteur_stagnation >= seuil_stagnation:
            # On monte le taux de mutation
            taux_mutation_actuel = 0.35

            compteur_stagnation = 0

        nombre_iteration += 1


    end: float = timer()

    execute_time = end - start

    if population_actuelle[0].fitness == 0:
        return population_actuelle[0].sudoku
    else:
        return None


def est_valide(grille : npt.NDArray[np.int32], puzzle : npt.NDArray[np.int32]) -> bool:
    """Vérifie les trois règles du Sudoku et que les cases du puzzle sont intactes."""
    figees = puzzle != 0
    return get_number_conflic(grille) == 0 and bool(np.all(grille != 0)) \
        and bool(np.array_equal(grille[figees], puzzle[figees]))


TAILLE_GRILLE : int = 9
DOSSIER_PUZZLES : Path = Path(__file__).parent / "puzzles"
DOSSIER_RESULTATS : Path = Path(__file__).parent / "resultats"


@dataclass
class Puzzle:
    nom: str
    grille: npt.NDArray[np.int32]
    metadonnees: dict[str, str]


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

        if get_number_conflic(data) != 0:
            raise ValueError(f"{path} : les chiffres donnés se contredisent déjà")

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


NB_EXECUTIONS : int = 10

ALGORITHMES : dict[str, Callable[..., Resultat]] = {
    "hill_climbing": hill_climbing_resolve,
}


def main():
    puzzles = IO.read_all(DOSSIER_PUZZLES)
    print(f"{len(puzzles)} puzzle(s) chargé(s) depuis « {DOSSIER_PUZZLES} »")

    for nom_algorithme, resoudre in ALGORITHMES.items():
        print(f"\n=== {nom_algorithme} ===")

        for puzzle in puzzles:
            difficulte = puzzle.metadonnees.get("Difficulty", "?")

            for numero in range(1, NB_EXECUTIONS + 1):
                res = resoudre(puzzle.grille, graine=numero)

                if res.resolu and not est_valide(res.solution, puzzle.grille):
                    raise RuntimeError(f"Solution invalide : {puzzle.nom}, exécution {numero}")

                IO.export_statistiques(DOSSIER_RESULTATS, puzzle.nom, nom_algorithme, numero,
                                       res.historique, res.iterations, res.temps)
                IO.write_solution(
                    DOSSIER_RESULTATS / puzzle.nom / nom_algorithme / f"solution_{numero:02d}.txt",
                    puzzle, res)

                print(f"{puzzle.nom} ({difficulte}) exéc. {numero:2d} | "
                      f"résolu : {'oui' if res.resolu else 'non'} | {res.temps:7.3f} s | "
                      f"{res.iterations:>7} itérations")

    print(f"\nStatistiques enregistrées dans « {DOSSIER_RESULTATS} »")


#[0,0] en-bas a gauche

#Eliel
#Utilisation d'une matrice 9x9 pour représenter le sudoku
# euristique hill glambing : nombre de conflit avec les autre nombre ex : 8 7 8 =  4

#Xavier
# Algorythme génétique : fitnesse même que heuristique, calcul sélection sélection fitness individue / fitnesse total génération, séparation par prorata du fitness en horizontalement

#Eliel
#IO

#Xavier
#Fonction heuristique / fitness

#Comment définir les noeud du sodoku
#
if __name__ == "__main__":
    main()