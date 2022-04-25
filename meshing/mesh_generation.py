import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math

class Vertex:
    def __init__(self, x,y,z, global_i=None):
        self.x = x
        self.y = y
        self.z = z
        self.global_i = global_i
        self.theta = self.get_theta()
        self.r = np.sqrt(x**2 + y**2)
    def get_theta(self):
        # if self.x == 0:
        #     if self.y > 0:
        #         return np.pi / 2
        #     elif self.y < 0:
        #         return 3 * np.pi /2
        # else:
        return np.arctan2(self.y, self.x)
    def __str__(self):
        return '    ( {} {} {}) // {}'.format(self.x,self.y,self.z,self.global_i)
    def flip_z(self):
        return Vertex(self.x, self.y, -1*self.z, self.global_i + 32)
    def plot(self, vert2):
        plt.plot([self.x, vert2.x], [self.y, vert2.y], 'o-k')

class Arc:
    def __init__(self, v0, v1):
        self.v0 = v0
        self.v1 = v1
        self.vmid = self.find_mid()

    def find_mid(self):
        xsign = 1
        ysign = 1
        if (self.v0.x + self.v1.x)/2 < 0:
            xsign = -1
        if (self.v0.y + self.v1.y)/2 < 0:
            ysign = -1
        
        theta = (self.v1.theta - self.v0.theta)/2 + self.v0.theta
        x = math.copysign(self.v0.r * np.cos(theta),xsign )
        y = math.copysign(self.v0.r * np.sin(theta),ysign )
        z = self.v0.z
        return Vertex(x,y,z)

    def __str__(self):
        return 'arc {} {} ( {} {} {})'.format(self.v0.global_i, self.v1.global_i, self.vmid.x, self.vmid.y, self.vmid.z)

class Face:
    def __init__(self, v0, v1, v2, v3):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    def local_node(self, i):
        if i == 0 or i == 4:
            return self.v0
        elif i == 1 or i == 5:
            return self.v1
        elif i == 2 or i == 6:
            return self.v2
        elif i == 3 or i == 7:
            return self.v3
    def generate_back_face(self):
        v4 = self.v0.flip_z()
        v5 = self.v1.flip_z()
        v6 = self.v2.flip_z()
        v7 = self.v3.flip_z()
        return Face(v4, v5, v6, v7)
    def nodes(self):
        return [self.v0, self.v1, self.v2, self.v3]
    def plot(self):
        nodes = self.nodes()
        [nodes[i].plot(nodes[i+1]) for i in range(len(nodes)-1)]
        nodes[-1].plot(nodes[0])

class Block:
    def __init__(self, front_face, i, nx1=1, nx2=1, nx3=1, ex1=1, ex2=1, ex3=1):
        self.front = front_face
        self.back = self.front.generate_back_face()
        self.index = i
        self.nx1 = int(nx1)
        self.nx2 = int(nx2)
        self.nx3 = int(nx3)
        self.ex1 = ex1
        self.ex2 = ex2
        self.ex3 = ex3
    def local_node(self,i):
        if i <= 3:
            return self.front.local_node(i)
        elif i >= 4:
            return self.back.local_node(i)
    def __str__(self):
        global_nodes = [int(self.local_node(i).global_i) for i in range(8)]
        global_nodes_str = ' '.join(str(n) for n in global_nodes)
        return '    // block {}\n   hex ({}) ({} {} {}) simpleGrading ( {} {} {})'.format(self.index, global_nodes_str, self.nx1, self.nx2, self.nx3, self.ex1, self.ex2, self.ex3)

class Index:
    def __init__(self):
        self.current = 0
    def i(self):
        index = self.current
        self.current += 1
        return index

def generate_circle(r, z, index, n=8):
    dtheta = 2 * np.pi / n
    current_theta = 0
    current_x = r
    current_y = 0
    nodes = []
    for i in range(n):
        nodes.append(Vertex(current_x, current_y, z, index.i()))
        current_theta += dtheta
        current_x = r*np.cos(current_theta)
        current_y = r*np.sin(current_theta)
    return nodes

def generate_square(lw, lf, h, delta, z, index):
    nodes = []
    cx = lw #current x
    cy = 0 #current y
    append = lambda : nodes.append(Vertex(cx,cy,z,index.i()))

    append()
    cy += delta
    append()
    cy += h-delta
    append()
    cx += -1*(lw-delta)
    append()
    cx += -1*delta
    append()
    cx += -1*delta
    append()
    cx += -1*(lf-delta)
    append()
    cy += -1*(h-delta)
    append()
    cy += -1*delta
    append()
    cy += -1*delta
    append()
    cy += -1*(h-delta)
    append()
    cx += lf-delta
    append()
    cx += delta
    append()
    cx += delta
    append()
    cx +=lw-delta
    append()
    cy += h - delta
    append()

    return nodes

def generate_faces(n):
    # n = list of 31 nodes
    # this function is largely a abstraction tool
    faces = []
    append = lambda v0, v1, v2, v3: faces.append(Face(n[v0],n[v1],n[v2],n[v3]))

    # circles and rectangles are defined counter clockwise
    # assuming

    # circle
    append(0,8,9,1)#0
    append(1,9,10,2)#1
    append(2,10,11,3)#2
    append(3,11,12,4)#3
    append(4,12,13,5)#4
    append(5,13,14,6)#5
    append(6,14,15,7)#6
    append(7,15,8,0)#7

    # square and rectangle
    append(8,16,17,9)#8
    append(9,17,18,19)#9
    append(9,19,20,10)#10
    append(10,20,21,11)#11
    append(11,21,22,23)#12
    append(11,23,24,12)#13
    append(12,24,25,13)#14
    append(13,25,26,27)#15
    append(13,27,28,14)#16
    append(14,28,29,15)#17
    append(15,29,30,31)#18
    append(15,31,16,8)#19

    return faces

def generate_arcs(blocks):
    # blocks = list of blocks
    # this function is largely a abstraction tool
    arcs = []
    append = lambda x1, x2: arcs.append(Arc(x1,x2))
    for block in blocks:
        for face in [block.front, block.back]:
            x1 = face.v0
            x2 = face.v3
            append(x1,x2)
            x1 = face.v1
            x2 = face.v2
            append(x1,x2)
        
    return arcs

def main(d=1, r=0.5, h=3, lw=3, lf=3, dz=-0.05, nx= [10, 20, 30, 30, 30, 30], ex=[2,1,4,1,4,4], user_name = 'n/a', file_name = 'fig'):
    if dz > 0:
        dz = -1*dz

    # generate front nodes
    nodes_index = Index()
    nodes = []
    nodes += generate_circle(d/2,dz,nodes_index)
    nodes += generate_circle(d/2+r,dz,nodes_index)
    delta = (d/2+r)*np.sqrt(2)/2
    nodes += generate_square(lw,lf, h, delta, dz, nodes_index)
    nodes += [node.flip_z() for node in nodes]
    
    # generate front faces
    faces = generate_faces(nodes)
    [face.plot() for face in faces]
    if file_name.endswith('blockMeshDict'):
        file_name = file_name.replace('blockMeshDict','fig')
    plt.savefig(file_name + '.png')

    # generate blocks
    block_index = Index()
    blocks = [Block(face, block_index.i()) for face in faces]

    circles = [blocks[i] for i in range(8)]
    rectangles = [blocks[i] for i in [8,10,13,16,19,11,14,17]]
    squares = [blocks[i] for i in [9,12,15,18]]

    nx1c= nx[0] #circle dof1
    nx2c = nx[1] #circle dof2
    nx1r = [0, 0, 0, 0]
    nx1r[0] = nx[2] # rectangel dof1, east
    nx1r[1] = nx[3] # north
    nx1r[2] = nx[4] # west
    nx1r[3] = nx[5] # south
    
    exr = ex[0] #radial
    exns = ex[1] #north/south
    exe = ex[2] #east (wake)
    exw = ex[3] #west (fore)

    for circle in circles:
        circle.nx1 = nx1c
        circle.nx2 = nx2c
        circle.ex1 = exr
        circle.ex2 = 1

    j = 0
    for rectangle in rectangles:
        rectangle.nx1 = nx1r[j % 4]
        rectangle.nx2 = nx2c
        rectangle.ex2 = 1
        j += 1

    j = 0
    for square in squares:
        square.nx1 = nx1r[j % 4]
        square.nx2 = nx1r[(j+1) % 4]
        j += 1

    for i in [8,9,19]:
        blocks[i].ex1 = exe
    for i in [10,11,12,16,17,18]:
        blocks[i].ex1 =  exns
    for i in [13,14,15]:
        blocks[i].ex1 = exw

    blocks[9].ex2 = exns
    blocks[12].ex2 = exw
    blocks[15].ex2 = exns
    blocks[18].ex2 = exe

    # create arcs
    arcs = generate_arcs(circles)

    # Create output
    output = ['\n']
    a = lambda newline: output.append(newline + '\n') # short hand
    a('// User: {}'.format(user_name))
    a('// Mesh generated on {}'.format(datetime.now().strftime("%m/%d/%Y %H:%M:%S")))
    a('')
    a('// Lf = {}'.format(lf))
    a('// Lw = {}'.format(lw))
    a('// R = {}'.format(r))
    a('// D = {}'.format(d))
    a('// H = {}'.format(h))
    a('')
    a('FoamFile')
    a('{')
    a(' version 2.0;')
    a(' format  ascii;')
    a(' class   dictionary;')
    a(' object  blockMeshDict;')
    a('}')
    a('')
    a('convertToMeters  1.0;')
    a('')
    a('vertices')
    a('(')
    [a(str(v)) for v in nodes]
    a(');')
    a('')
    a('blocks')
    a('(')
    [a(str(b)) for b in blocks]
    a(');')
    a('')
    a('')
    a('edges')
    a('(')
    a('')
    [a(str(arc)) for arc in arcs]
    a('')
    a(');')
    a('')
    a('boundary')
    a('(')
    a(' inlet')
    a(' {')
    a('     type patch;')
    a('     faces')
    a('     (')
    a('         (22 54 55 23)')
    a('         (23 55 56 24)')
    a('         (24 56 57 25)')
    a('         (25 57 58 26)')
    a('     );')
    a(' }')
    a(' outlet')
    a(' {')
    a('     type patch;')
    a('     faces')
    a('     (')
    a('         (18 50 49 17)')
    a('         (17 49 48 16)')
    a('         (16 48 63 31)')
    a('         (31 63 62 30)')
    a('     );')
    a(' }')
    a(' cylinder')
    a(' {')
    a('     type wall;')
    a('     faces')
    a('     (')
    a('         (0 32 33 1)')
    a('         (1 33 34 2)')
    a('         (2 34 35 3)')
    a('         (3 35 36 4)')
    a('         (4 36 37 5)')
    a('         (5 37 38 6)')
    a('         (6 38 39 7)')
    a('         (7 39 32 0)')
    a('     );')
    a(' }')
    a(' top')
    a(' {')
    a('     type symmetryPlane;')
    a('     faces')
    a('     (')
    a('         (22 54 53 21)')
    a('         (21 53 52 20)')
    a('         (20 52 51 19)')
    a('         (19 51 50 18)')
    a('     );')
    a(' }')
    a(' bottom')
    a(' {')
    a('     type symmetryPlane;')
    a('     faces')
    a('     (')
    a('         (26 58 59 27)')
    a('         (27 59 60 28)')
    a('         (28 60 61 29)')
    a('         (29 61 62 30)')
    a('     );')
    a(' }')
    a('')
    a(');')

    return ''.join(output)

if __name__ == '__main__':
    file_name = input("Enter the file name: ")
    user_name = input('Enter a user name: ')
    d = float(input("Enter d, the diameter of the cylinder: "))
    r = float(input("Enter r, the width of the circular region: "))
    h = float(input("Enter h, which is half of the height of the mesh: "))
    lw = float(input("Enter L_w: "))
    lf = float(input("Enter L_f: "))
    dz = float(input("Enter dz, which is the distance of one of the faces from the z axis: "))

    nx1c = int(input("Enter the number of cells in direction 1 for the circle mesh blocks: "))
    nx2c = int(input("Enter the number of cells in direction 2 for the circle mesh blocks: "))
    nx1r = int(input("Enter the number of cells for the rectangle mesh blocks in the east direction: "))
    nx2r = int(input("Enter the number of cells for the rectangle mesh blocks in the north direction: ")) 
    nx3r = int(input("Enter the number of cells for the rectangle mesh blocks in the west direction: ")) 
    nx4r = int(input("Enter the number of cells for the rectangle mesh blocks in the south direction: ")) 
    nx = [nx1c, nx2c, nx1r,nx2r,nx3r,nx4r]
    # nx = [nx1c,nx2c,nx1r]

    # ex1c = float(input("Enter the expansion ratio in direction 1 for the circle mesh blocks: "))
    # ex2c = float(input("Enter the expansion ratio in direction 2 for the circle mesh blocks: ")) # 1
    # ex1r = float(input("Enter the expansion ratio in direction 1 for the rectangle mesh blocks: "))
    # ex2r = float(input("Enter the expansion ratio in direction 2 for the rectangle mesh blocks: ")) # 1
    # ex1s = float(input("Enter the expansion ratio in direction 1 for the square mesh blocks: ")) # defined by ex1r
    # ex2s = float(input("Enter the expansion ratio in direction 2 for the square mesh blocks: ")) # defined by ex1r
    # ex = [ex1c, ex2c, ex1r, ex2r, ex1s, ex2s]
    exr = float(input("Enter the radial expansion ratio for the circles: "))
    exns = float(input("Enter the North/South expansion ratio"))
    exe = float(input("Enter the east expansion ratio: "))
    exw = float(input("Enter the west expansion ratio: "))
    ex = [exr, exns, exe, exw]

    output = main(d,r,h,lw,lf,dz,nx,ex,user_name, file_name)
    file = open(file_name, 'w')
    file.write(output)