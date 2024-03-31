import numpy as np 
import open3d as d3
import time 
import timeit
import os 

path = os.path.join(os.path.dirname(__file__), ".." , "Data", "pc.ply")
points_1 = d3.io.read_point_cloud(path)
change_of_points = np.asarray(points_1.points)
# print(change_of_points)
N=5
def k(data,k):
    cen = data[np.random.choice(len(data), size = k , replace=False)]
    while True:
        d = np.linalg.norm(data[:,None] - cen[None,:], axis=2)
        clus = np.argmin(d , axis=1)
        new_c = np.array([data[clus == i].mean(axis=0) for i in range(k)])
        if np.allclose(new_c , cen):
            break
        cen = new_c
    return cen, clus

Time_Taken = timeit.timeit(lambda : k(change_of_points,N) , number=1)

cen , clus = k(change_of_points, N)
c_c = [[0,0,1],[1,0,1],[0,1,0],[1,1,0],[1,0,0]]
colors = [c_c[c] for c in clus]
points_1.colors = d3.utility.Vector3dVector(colors)
d3.visualization.draw_geometries([points_1])
print(f"Time : {Time_Taken} ")
