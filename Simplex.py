import numpy as np
import scipy as sc
import scipy.special

def is_valid_simplex_param_array(param_array):
    for param in param_array:
        if param < 0:
            return False
    return param_array.sum() < 1




class Simplex:

    def __init__(self,vertices_list):
        self.vertices_list = vertices_list
        self.n = len(self.vertices_list) - 1  # dimension
        self.affine_matrix = self.get_affine_matrix()
        self.volume = self.compute_volume()


    def get_affine_matrix(self):
        A=np.array(self.vertices_list)
        A=A[1:]-A[0]
        affine_matrix = A.T
        return affine_matrix

    def is_valid_simplex(self):
        return np.linalg.det(self.affine_matrix) !=0

    def generate_random_points(self,n_trials=100):
        # random_param_arrays=[np.random.uniform(0,1,self.n) for i in range(n_trials)]
        # random_param_arrays = [param_array for param_array in random_param_arrays
        #                       if is_valid_simplex_param_array(param_array)]
        random_param_arrays = []
        for i in range(n_trials):
            a=np.array(np.random.uniform(0,1))
            for j in range(1,self.n):
                a=np.append(a, np.random.uniform(0,1-a.sum()))
            random_param_arrays.append(np.array(a))

        random_points = [np.array(self.vertices_list[0]) + self.affine_matrix @ param_array
                         for param_array in random_param_arrays]
        return random_points



    def point_is_in_simplex(self,p):
        b = np.array(p) - np.array(self.vertices_list[0])
        param_array= np.linalg.solve(self.affine_matrix,b)
        return is_valid_simplex_param_array(param_array)

    def compute_volume(self):
        volume=np.abs(np.linalg.det(self.affine_matrix))/sc.special.factorial(self.n)
        return volume


def have_disjoint_interiors(simplex1_vertices_list, simplex2_vertices_list,n_trials=100):
    Simplex1=Simplex(simplex1_vertices_list)
    Simplex2=Simplex(simplex2_vertices_list)
    random_simplex1_points=Simplex1.generate_random_points(n_trials)
    try:
        next(point for point in random_simplex1_points if Simplex2.point_is_in_simplex(point))
        return False
    except:
        return True

def are_pairwise_disjoint(simplex_vertices_list, other_simplices_vertices_lists,n_trials=100):
    for other_simplex_vertex_list in other_simplices_vertices_lists:
        if have_disjoint_interiors(other_simplex_vertex_list, simplex_vertices_list , n_trials) == False:
            return False
    return True






