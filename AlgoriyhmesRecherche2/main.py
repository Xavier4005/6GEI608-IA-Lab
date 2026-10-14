import numpy as np
import numpy.typing as npt

def main():
    t : set[tuple[int,int]] = set[tuple[int,int]]()

    t.add((1,1))
    t.add((2,1))
    t.add((6,3))
    t.add((8,9))

    if (8,9) in t:
        print("Oui")
    else:
        print("non")

    if (1,1) in t:
        print("Oui")
    else:
        print("non")


if __name__ == "__main__":
    main()



def genetic_resolve(sudoku : npt.NDArray[np.int32], frezz_number : set[tuple[int,int]]) -> npt.NDArray[np.int32]:
    
    pass



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

