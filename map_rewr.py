def map_rewr(file, mult):
	map_str = ''
	with open(file) as f:
		for x in f:
			map_str += x 
	mapa = map_str.split('\n')
	with open("new_map", 'w') as new_map:
		for line in mapa:
			if len(line) == 0:
				continue
			j = 0
			while(j < mult):
				for x in line:
					i = 0
					while(i < mult):
						new_map.write(x);
						i += 1
				new_map.write('\n')
				j += 1

map_rewr('map_small.txt', 2)
