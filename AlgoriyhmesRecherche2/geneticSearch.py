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

        freez_number : set[tuple[int, int]] = [tuple(c) for c in indices]
        return freez_number
    
    def generate_sudoku_aleatoire(sudoku : npt.NDArray[np.int32], lignes : npt.NDArray, colonnes : npt.NDArray) -> npt.NDArray[np.int32]:
        sudoku_rempli : npt.NDArray[np.int32] = np.random.randint(1, 10, sudoku.shape, np.int32)
        sudoku_rempli[lignes, colonnes] = sudoku[lignes, colonnes]

        return sudoku_rempli

    def croisement_blocs(self,parent_A: npt.NDArray[np.int32], parent_B: npt.NDArray[np.int32]) -> npt.NDArray[np.int32]:
        #Générer un masque 3x3 de booléens (True = Parent A, False = Parent B)
        masque_blocs = np.random.rand(3, 3) < 0.5

        #Étendre le masque à la taille 9x9 (chaque booléen est répété en matrice 3x3)
        masque_2d = np.kron(masque_blocs, np.ones((3, 3), dtype=bool))

        #Combiner les deux parents
        enfant = np.where(masque_2d, parent_A, parent_B)
        return enfant

    def genetic_resolve(self,sudoku : npt.NDArray[np.int32]) -> Resultat:
        # Variable de contrôle
        nombre_individue : int = 1000
        pourcentage_elitisme : int = 5
        nomtre_maximal_iteration : int = 10000

        frezz_number = self.generate_frezz_number(sudoku)

        population_actuelle : list[Individu] = list[Individu]()

        start: float = timer()

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

                enfant : npt.NDArray[np.int32] = self.croisement_blocs(parent_A.sudoku, parent_B.sudoku).copy()

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