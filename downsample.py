import argparse
import numpy as np
import open3d as d3
from scipy.spatial import KDTree
import timeit

agp = argparse.ArgumentParser()
agp.add_argument('path_of_ply_file' , type=str)
agp.add_argument('N' , type= int) 
agp.add_argument('e' , type= float)
agps = agp.parse_args()

points_1 = d3.io.read_point_cloud(agps.path_of_ply_file)
change_of_points = np.asarray(points_1.points)
KDT = KDTree(change_of_points)
points_2 = []
points_stored = set()
for p, point in enumerate(change_of_points):
    if p in points_stored:
        continue
    points_2.append(point)
    points_stored.add(p)
    _, points_3 = KDT.query(point, k=agps.N+1)
    for k in points_3[1:]:
        if k in points_stored:
            continue
        if np.linalg.norm(point - change_of_points[k]) < agps.e:
            points_stored.add(k)
time = timeit.default_timer()
points_4 = d3.geometry.PointCloud()
points_4.points = d3.utility.Vector3dVector(points_2)
d3.io.write_point_cloud("pc_downsampled.ply" , points_4)
d3.visualization.draw_geometries([points_1])
d3.visualization.draw_geometries([points_4])
ept = timeit.default_timer() - time
print("Time Taken :" , ept)
