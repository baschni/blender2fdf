import bpy
from pprint import pprint

OUTPUT_FILE = "C:\\Users\\basch\\Documents\\02_Code\\42\\42fdf_new\\cervin2.fdf"

obdata = bpy.context.object.data

print('Vertices:')
print(len(obdata.vertices))
xl = []
yl = []
zl = []

colors = {
    0: "0x228B22", 
    0.3: "0x92816d",
    0.8: "0xFFFFFF"
}

for v in obdata.vertices:
    xl.append(v.co.x)
    yl.append(v.co.y)
    zl.append(v.co.z)

min_x, min_y, min_z = min(xl), min(yl), min(zl)
max_x, max_y, max_z = max(xl), max(yl), max(zl)

Z_SCALE = 1
X_MAX = 80
Y_MAX = int((max_y - min_y) / (max_x - min_x) * X_MAX)
Z_MAX = int((max_z - min_z) / (max_x - min_x) * X_MAX * Z_SCALE)

def get_color(z):
    for threshold, color in dict(sorted(colors.items(), reverse=True)).items():
        if z >= threshold * Z_MAX:
            return color    

def generate_map():
    return [[0] * (X_MAX + 1) for i in range(0,(Y_MAX + 1))]


map = generate_map()
amount = generate_map()

print(min_x, min_y, min_z);
print(max_x, max_y, max_z);
print(X_MAX, Y_MAX, Z_MAX)
print(map)

for v in obdata.vertices:
    x = int((v.co.x - min_x) / (max_x - min_x) * X_MAX)
    y = int((v.co.y - min_y) / (max_y - min_y) * Y_MAX)
    z = ((v.co.z - min_z) / (max_z - min_z) * Z_MAX)
    map[y][x] += z
    amount[y][x] += 1

    
for y in range(0, Y_MAX + 1):
    for x in range(0, X_MAX + 1):
        map[y][x] = int(map[y][x] / amount[y][x])    


with open(OUTPUT_FILE, "w", newline='') as f:
    for y in range(Y_MAX, -1, -1):
        f.write(" ".join([str(i) + "," + get_color(i) for i in map[y]]) + "\n")