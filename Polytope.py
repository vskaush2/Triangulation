import itertools
from joblib import Parallel, delayed
from Simplex import *


class Polytope:

    def __init__(self, vertices_list):
        self.vertices_list = vertices_list
        self.n=len(self.vertices_list[0])
        self.candidate_simplices = self.get_candidate_simplices_for_triangulation()

    def get_candidate_simplices_for_triangulation(self):
        all_simplices = itertools.combinations(self.vertices_list, self.n + 1)
        candidate_simplices_for_triangulation = [list(vertices_tuple) for vertices_tuple in all_simplices
                                                 if Simplex(vertices_tuple).is_valid_simplex()]
        return candidate_simplices_for_triangulation

    def triangulation(self,n_trials=100):
        Delta = [self.candidate_simplices[0]]
        print("Added Simplex 1")
        tau = 0
        foundnewsimplex = True
        while foundnewsimplex:
            try:
                tau = next(i for i in range(tau + 1, len(self.candidate_simplices))
                                 if are_pairwise_disjoint(self.candidate_simplices[i], Delta, n_trials))
                Delta.append(self.candidate_simplices[tau])
                print("Added Simplex {}".format(len(Delta)))
            except:
                foundnewsimplex = False
        return Delta

    def compute_volume(self,n_trials = 100):
        Delta = self.triangulation(n_trials)
        simplex_volumes = [Simplex(simplex_vertices_list).volume for simplex_vertices_list in Delta]
        volume=np.sum(simplex_volumes)
        return volume






















