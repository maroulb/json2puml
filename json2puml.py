import sys
import copy
import json

source = sys.argv[1]

print('file: ' + str(source))

graph = open(source, 'r')

graph = json.load(graph)


def createPuml(filename, graph):
	puml = open(filename, 'a')
	puml.write('@startuml\n')
	puml.write('skinparam agent {\n')
	puml.write('     roundCorner 25\n')
	puml.write('}\n')
	puml.write('\n')

	localgraph = copy.deepcopy(graph)
	n = 0
	replaced = {}
	for node in localgraph.keys():
		nn = str(n)
		name = node
		if len(name) > 15:
			name = name.replace(' ', '\\n')
			name = name.replace('_', '\\n')
		line = 'agent "' + name + '" as n' + nn
		puml.write(line + '\n')
		replaced[node] = 'n' + nn
		n = n + 1
	for node in localgraph.keys():
		for value in localgraph[node]:
			localgraph[node][(localgraph[node]).index(value)] = replaced[value]
		localgraph[replaced[node]] = localgraph.pop(node)
	for node in localgraph.keys():
		for value in localgraph[node]:
			line = node + ' --> ' + value
			puml.write(line + '\n')
	puml.write('@enduml')
	puml.close()

pumlName = source.replace('.json', '') + '.puml'
createPuml(pumlName, graph)
