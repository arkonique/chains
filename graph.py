import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random as rd
import math

# Add noise
def noise_scaling(x):
    return x+rd.random()*(-1)**(rd.randint(0,1))

# Generate random grid
def generate_grid(m,n,num_x,num_y):
    X = np.linspace(0,m,num_x)
    Y = np.linspace(0,n,num_y)
    X,Y=np.meshgrid(X,Y)
    X=[i for s in X for i in s]
    Y=[i for s in Y for i in s]
    X=[noise_scaling(x) for x in X]
    Y=[noise_scaling(y) for y in Y]
    return tuple(zip(X,Y))

# Generate voronoi diagram
def generate_voronoi(grid):
    vor = Voronoi(grid)
    vertices=vor.vertices
    edges=vor.ridge_vertices
    # Remove all vertices outside the grid
    vertices=[v.tolist() for v in vertices if v[0]>=0 and v[0]<=10 and v[1]>=0 and v[1]<=10]
    # Join two vertices if they are very close
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            if i!=j and math.sqrt((vertices[i][0]-vertices[j][0])**2+(vertices[i][1]-vertices[j][1])**2)<0.01:
                vertices[j]=vertices[i]
    # Remove duplicate vertices
    vertices=list(set([tuple(v) for v in vertices]))
    '''
    # Update edges to reflect the new vertex indices
    for i in range(len(edges)):
        for j in range(len(edges[i])):
            try:
                edges[i][j]=vertices.index(vor.vertices[edges[i][j]].tolist())
                #print(vor.vertices[edges[i][j]])
                #print(edges[i][j])
            except:
                #print(vertices.index(vor.vertices[edges[i][j]]))
                edges[i][j]=-100
                #print(edges[i][j])
    # Remove all edges with a vertex outside the grid
    edges=[e for e in edges if e[0]!=-100 and e[1]!=-100]
    '''
    # Calculate angle from horizontal for each edge
    angles=[math.degrees(math.atan2(vertices[e[1]][1]-vertices[e[0]][1],vertices[e[1]][0]-vertices[e[0]][0])) for e in edges]
    # Assign random weights to each edge
    return vor,vertices,edges,angles

# Plot voronoi diagram
def plot_voronoi(vertices,edges,angles,weights):
    # Plot vertices
    plt.scatter([v[0] for v in vertices],[v[1] for v in vertices],c='r',s=2)
    # Plot edges
    for i in range(len(edges)):
        plt.plot([vertices[edges[i][0]][0],vertices[edges[i][1]][0]],[vertices[edges[i][0]][1],vertices[edges[i][1]][1]],c=(0,0,0,weights[i]))
    # Write angle on each edge
    for i in range(len(edges)):
        plt.text((vertices[edges[i][0]][0]+vertices[edges[i][1]][0])/2,(vertices[edges[i][0]][1]+vertices[edges[i][1]][1])/2,round(angles[i],2),fontsize=10)

    plt.show()


# main
if __name__ == "__main__":
    # Generate grid
    grid = generate_grid(10,10,30,30)
    # Generate Voronoi
    vor,vertices,edges,angles = generate_voronoi(grid)
    # Assign random weights to each edge
    weights=[rd.random() for e in edges]
    plot_voronoi(vertices,edges,angles,weights)
