from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
from timeit import default_timer as timer
import random
from seekAlgorithme import SeekAlgorithme
from individu import Individu
from resultat import Resultat

class GeneticSearch(SeekAlgorithme):
    def generate_frezz_number(self,sudoku : npt.NDArray[np.int32]) -> set[tuple[int,int]]:
        indices = np.argwhere(sudoku != 0)

        freez_number : set[tuple[int, int]] = set([tuple(c) for c in indices])
        return freez_number
    
    def generate_sudoku_aleatoire(self, sudoku: npt.NDArray[np.int32], lignes: npt.NDArray, colonnes: npt.NDArray) -> npt.NDArray[np.int32]:
        sudoku_rempli = sudoku.copy()
        for b_row in range(3):
            for b_col in range(3):
                r_start, c_start = b_row * 3, b_col * 3
                bloc = sudoku_rempli[r_start:r_start+3, c_start:c_start+3]
                presents = bloc[bloc != 0]
                manquants = [v for v in range(1, 10) if v not in presents]
                random.shuffle(manquants)
                for r in range(3):
                    for c in range(3):
                        if bloc[r, c] == 0:
                            bloc[r, c] = manquants.pop()
        return sudoku_rempli

    def croisement_blocs(self,parent_A: npt.NDArray[np.int32], parent_B: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
        #Générer un masque 3x3 de booléens (True = Parent A, False = Parent B)
        masque_blocs = np.random.rand(3, 3) < 0.5

        #Étendre le masque à la taille 9x9 (chaque booléen est répété en matrice 3x3)
        masque_2d = np.kron(masque_blocs, np.ones((3, 3), dtype=bool))

        #Combiner les deux parents
        enfant = np.where(masque_2d, parent_A, parent_B).copy()
        return enfant

    def get_cases_en_conflit(self, grid: npt.NDArray[np.int32], frezz_number: set[tuple[int, int]]) -> list[tuple[int, int]]:
        cases_conflit = []
        # Vérification des doublons par ligne
        for r in range(9):
            vals, counts = np.unique(grid[r, :], return_counts=True)
            doublons = vals[counts > 1]
            for c in range(9):
                if grid[r, c] in doublons and (r, c) not in frezz_number:
                    cases_conflit.append((r, c))
                    
        # Vérification des doublons par colonne
        for c in range(9):
            vals, counts = np.unique(grid[:, c], return_counts=True)
            doublons = vals[counts > 1]
            for r in range(9):
                if grid[r, c] in doublons and (r, c) not in frezz_number:
                    if (r, c) not in cases_conflit:
                        cases_conflit.append((r, c))
                        
        return cases_conflit

    def genetic_resolve(self,sudoku : npt.NDArray[np.int32]) -> Resultat:
        # Variable de contrôle
        nombre_individue : int = 1000
        pourcentage_elitisme : int = 5
        nomtre_maximal_iteration : int = 1000000

        frezz_number = self.generate_frezz_number(sudoku)

        population_actuelle : list[Individu] = list[Individu]()

        start: float = timer()
        historique : list[tuple[int, int]] = list[tuple[int, int]]()
        redemarrage : int = 0

        # Transformation en tableux une seul fois pour la génération de toute les 1000 individue de la généation 1
        lignes_brut , colonnes_brut = zip(*frezz_number)
        lignes = np.array(lignes_brut)
        colonnes = np.array(colonnes_brut)

        # Création de la première population
        for _ in range(nombre_individue):
            sudoku_rempli : npt.NDArray[np.int32] = self.generate_sudoku_aleatoire(sudoku, lignes, colonnes)
            fitness = -self.get_number_conflic(sudoku_rempli)
            population_actuelle.append(Individu(sudoku_rempli, fitness))

        population_actuelle.sort(key=lambda ind: ind.fitness, reverse=True)

            # Génération des population suivante et arrêt quand résultat trouver

        # Génération de list de bloc pour les mutation
        # Dictionnaire pour grouper les cases libres par bloc (0 à 8)
        cases_libres_par_bloc : dict[int, list[tuple[int, int]]] = {i: [] for i in range(9)}

        for l in range(9):
            for c in range(9):
                pos = (l, c)
                if pos not in frezz_number:
                    bloc = 3 * (l // 3) + (c // 3)
                    cases_libres_par_bloc[bloc].append(pos)

        # 3. Filtrer uniquement les blocs qui ont au moins 2 cases libres (pour le swap intra-bloc)
        blocs_mutables : list[int] = [b for b, cases in cases_libres_par_bloc.items() if len(cases) >= 2]

        # Variables de contrôle adaptatif
        taux_mutation_base : float = 0.10
        taux_mutation_actuel : float = taux_mutation_base
        seuil_stagnation : int = 50

        meilleure_fitness_precedente : int = population_actuelle[0].fitness
        compteur_stagnation : int = 0

        historique.append((0, population_actuelle[0].fitness))

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

                enfant : npt.NDArray[np.int32] = self.croisement_blocs(parent_A.sudoku, parent_B.sudoku).copy()

                # Appliquer la mutation
                # Mutation guidée sur les conflits
                if random.random() < taux_mutation_actuel and blocs_mutables:
                    # 1. Identifier les cases impliquées dans des conflits (lignes ou colonnes)
                    cases_en_conflit = self.get_cases_en_conflit(enfant, frezz_number)
                    
                    if cases_en_conflit and random.random() < 0.80:
                        # 80% du temps: cibler un bloc qui contient au moins une case en conflit
                        case_cible = random.choice(cases_en_conflit)
                        bloc_cible = 3 * (case_cible[0] // 3) + (case_cible[1] // 3)
                        
                        if bloc_cible in blocs_mutables and len(cases_libres_par_bloc[bloc_cible]) >= 2:
                            c1 = case_cible
                            # Choisir une autre case libre dans le même bloc
                            autres_cases = [c for c in cases_libres_par_bloc[bloc_cible] if c != c1]
                            c2 = random.choice(autres_cases)
                            enfant[c1], enfant[c2] = enfant[c2], enfant[c1]
                    else:
                        # 20% du temps (ou fallback): mutation uniforme classique intra-bloc
                        bloc_choisi = random.choice(blocs_mutables)
                        coords = random.sample(cases_libres_par_bloc[bloc_choisi], 2)
                        enfant[coords[0]], enfant[coords[1]] = enfant[coords[1]], enfant[coords[0]]

                fitness = -self.get_number_conflic(enfant)
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

            #FULL RESET : Si bloqué trop longtemps
            if compteur_stagnation >= 200:
                # On réinitialise TOUTE la population de zéro)
                population_actuelle = []

                for _ in range(nombre_individue - 1):
                    sudoku_rempli = self.generate_sudoku_aleatoire(sudoku, lignes, colonnes)
                    fitness = -self.get_number_conflic(sudoku_rempli)
                    population_actuelle.append(Individu(sudoku_rempli, fitness))

                population_actuelle.sort(key=lambda ind: ind.fitness, reverse=True)
                taux_mutation_actuel = taux_mutation_base
                compteur_stagnation = 0
                redemarrage += 1
            #STAGNATION LÉGÈRE : Ajustement du taux de mutation
            elif compteur_stagnation >= seuil_stagnation:
                taux_mutation_actuel = 0.35

            historique.append((nombre_iteration, meilleure_fitness_actuelle))
            nombre_iteration += 1


        end: float = timer()

        execute_time = end - start

        if population_actuelle[0].fitness == 0:
            return Resultat(population_actuelle[0].sudoku, population_actuelle[0].sudoku, execute_time, nombre_iteration, redemarrage, True, 0, historique)
        else:
            return Resultat(None, population_actuelle[0].sudoku, execute_time, nombre_iteration, redemarrage, False, population_actuelle[0].fitness, historique)