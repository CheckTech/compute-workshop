import compute_rhino3d.Util
import compute_rhino3d.Grasshopper as gh
import rhino3dm
import json

compute_rhino3d.Util.authToken = ADD_TOKEN_HERE

pt1 = rhino3dm.Point3d(0, 0, 0)
circle = rhino3dm.Circle(pt1, 5)
angle = 20

# convert circle to curve and stringify
curve = json.dumps(circle.ToNurbsCurve().Encode())

# create list of input trees
curve_tree = gh.DataTree("RH_IN:curve")
curve_tree.Append([0], [curve])
rotate_tree = gh.DataTree("RH_IN:rotate")
rotate_tree.Append([0], [angle])
trees = [curve_tree, rotate_tree]

output = gh.EvaluateDefinition('workshop_step5.ghx', trees)
# print(output)

# decode results
branch = output['values'][0]['InnerTree']['{ 0; }']
lines = [rhino3dm.CommonObject.Decode(json.loads(item['data'])) for item in branch]

# create a 3dm file with results
model = rhino3dm.File3dm()
for l in lines:
    model.Objects.AddCurve(l) # they're actually LineCurves...

model.Write('workshop_step5.3dm')