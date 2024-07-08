import turtle
import math
import pygame
import sys

# globals
mapa = []
spread = 45
base_angle = 180
my_axis = []
mx_axis = []
my_index = 0
mx_index = 0

# init map
# mapa ma współżędne y , x - uwaga y liczone od góry
with open('map.txt') as map:
	for m in map:
		mapa.append(m.replace('\n', ''))

def find_start():
	x = 0
	y = 0
	for m in mapa:
		for n in m:
			if n == 'S':
				mapa[y] = mapa[y].replace('S', '0')
				return [y, x]
			x += 1
		y += 1
		x = 0


def recalc_axis(type):
	current_index = 0
	moves = []
	x0 = start_pos[0]
	y0 = start_pos[1]
	d = 100
	lastx = None
	lasty = None

# wyznaczanie osi ruchu przód / tył 
	if type == 'y':
	# cofanie się do najbliższej przeszkody (z tyłu)
		theta_radians = math.radians(base_angle - 180)
		x1 = x0 + int(d * math.cos(theta_radians))
		y1 = y0 + int(d * math.sin(theta_radians))
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		sx = 1 if x0 < x1 else -1
		sy = 1 if y0 < y1 else -1
		err = dx - dy
		while(mapa[x0][y0] == '0'):
			lastx = x0
			lasty = y0
			e2 = 2 * err
			if e2 > -dy:
				err -= dy
				x0 += sx
			if e2 < dx:
				err += dx
				y0 += sy
			current_index += 1

		if lastx:
			x0 = lastx
		if lasty:
			y0 = lasty

	# zapisywanie pozycji ruchu na osi przód tył do najbliższej przeszkody (z przodu)
		theta_radians = math.radians(base_angle)
		x1 = x0 + int(d * math.cos(theta_radians))
		y1 = y0 + int(d * math.sin(theta_radians))
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		sx = 1 if x0 < x1 else -1
		sy = 1 if y0 < y1 else -1
		err = dx - dy
		while(mapa[x0][y0] == '0'):
			e2 = 2 * err
			if e2 > -dy:
				err -= dy
				x0 += sx
			if e2 < dx:
				err += dx
				y0 += sy
			moves.append([x0, y0]) 
		return (current_index ,moves)

# wyznaczanie osi ruchu lewo / prawo 
	if type == 'x':
	# przesunięcie się do najbliższej przeszkody (po lewej)
		theta_radians = math.radians(base_angle + 90)
		x1 = x0 + int(d * math.cos(theta_radians))
		y1 = y0 + int(d * math.sin(theta_radians))
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		sx = 1 if x0 < x1 else -1
		sy = 1 if y0 < y1 else -1
		err = dx - dy
		while(mapa[x0][y0] == '0'):
			lastx = x0
			lasty = y0
			e2 = 2 * err
			if e2 > -dy:
				err -= dy
				x0 += sx
			if e2 < dx:
				err += dx
				y0 += sy
			current_index += 1

		if lastx:
			x0 = lastx
		if lasty:
			y0 = lasty

	# zapisywanie pozycji ruchu na osi lewo/prawo do najbliższej przeszkody (z prawej)
		theta_radians = math.radians(base_angle - 90)
		x1 = x0 + int(d * math.cos(theta_radians))
		y1 = y0 + int(d * math.sin(theta_radians))
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		sx = 1 if x0 < x1 else -1
		sy = 1 if y0 < y1 else -1
		err = dx - dy
		while(mapa[x0][y0] == '0'):
			e2 = 2 * err
			if e2 > -dy:
				err -= dy
				x0 += sx
			if e2 < dx:
				err += dx
				y0 += sy
			moves.append([x0, y0]) 
		return (current_index ,moves)

def find_collision(x0, y0, rad):

	def plot_line(x0, y0, x1, y1):
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		sx = 1 if x0 < x1 else -1
		sy = 1 if y0 < y1 else -1
		err = dx - dy

		while True:
			if mapa[x0][y0] == '1':
				return (x0, y0, 0)
			if mapa[x0][y0] == 'A':
				return (x0, y0, 1)
			e2 = 2 * err
			if e2 > -dy:
				err -= dy
				x0 += sx
			if e2 < dx:
				err += dx
				y0 += sy

	# Długość linii
	d = 100

	# Przeliczanie kąta na radiany
	theta_radians = math.radians(rad)

	# Obliczanie współrzędnych punktu końcowego
	x1 = x0 + int(d * math.cos(theta_radians))
	y1 = y0 + int(d * math.sin(theta_radians))
	result = plot_line(x0, y0, x1, y1)
	return result

def calc_dist(a, b):
	if a == 0:
		return b
	if b == 0:
		return a
	return math.sqrt(a * a + b * b)


start_pos = find_start()

def re_calc_distances(start_pos):
	colors = []
	distances = []
	start_angle = base_angle + spread
	end_angle = base_angle - spread
	curr_a = spread

	while (start_angle != end_angle):
		colis = find_collision(start_pos[0], start_pos[1], start_angle)
		colors.append(colis[2])
		dist = calc_dist(abs(start_pos[0] - colis[0]), abs(start_pos[1] - colis[1]))
		curr_r = math.radians(curr_a)
		dist = math.cos(curr_r) * dist
		distances.append(dist)
		start_angle -= 1
		curr_a -= 1
	return [distances, colors]

dist_col = re_calc_distances(start_pos)
distances = dist_col[0]
print(distances)
colors = dist_col[1]

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
width, height = 1500, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pionowa Linia z Pygame")

# Kolory (RGB)
background_color = (255, 255, 255)  # Biały
line_color = [[124, 128, 125], [39, 78, 140]]

pygame.key.set_repeat(50, 50)

axis_data = recalc_axis('y')
my_axis = axis_data[1]
my_index = axis_data[0]

axis_data = recalc_axis('x')
mx_axis = axis_data[1]
mx_index = axis_data[0]

# Główna pętla programu
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:

			if pygame.key.name(event.key) == 'left':
				mx_index -= 1
				start_pos = mx_axis[mx_index]
				axis_data = recalc_axis('y')
				my_axis = axis_data[1]
				my_index = axis_data[0]
				dist_col = re_calc_distances(start_pos)
				distances = dist_col[0]
				colors = dist_col[1]

			if pygame.key.name(event.key) == 'right':
				mx_index += 1
				start_pos = mx_axis[mx_index]
				axis_data = recalc_axis('y')
				my_axis = axis_data[1]
				my_index = axis_data[0]
				dist_col = re_calc_distances(start_pos)
				distances = dist_col[0]
				colors = dist_col[1]

			if pygame.key.name(event.key) == 'up':
				my_index += 1
				start_pos = my_axis[my_index]
				axis_data = recalc_axis('x')
				mx_axis = axis_data[1]
				mx_index = axis_data[0]
				dist_col = re_calc_distances(start_pos)
				distances = dist_col[0]
				colors = dist_col[1]

			if pygame.key.name(event.key) == 'down':
				if my_index != 0:
					my_index -= 1
				start_pos = my_axis[my_index]
				axis_data = recalc_axis('x')
				mx_axis = axis_data[1]
				mx_index = axis_data[0]
				dist_col = re_calc_distances(start_pos)
				distances = dist_col[0]
				colors = dist_col[1]

			if pygame.key.name(event.key) == 'a':
				base_angle += 5
				axis_data = recalc_axis('y')
				my_axis = axis_data[1]
				my_index = axis_data[0]
				axis_data = recalc_axis('x')
				mx_axis = axis_data[1]
				mx_index = axis_data[0]
				dist_col = re_calc_distances(start_pos)
				distances = dist_col[0]
				colors = dist_col[1]

			if pygame.key.name(event.key) == 'd':
				base_angle -= 5
				axis_data = recalc_axis('y')
				my_axis = axis_data[1]
				my_index = axis_data[0]
				axis_data = recalc_axis('x')
				mx_axis = axis_data[1]
				mx_index = axis_data[0]
				dist_col = re_calc_distances(start_pos)
				distances = dist_col[0]
				colors = dist_col[1]

	# Wypełnij tło
	screen.fill(background_color)

	# Rysowanie pionowej linii (start_x, start_y, end_x, end_y), szerokość linii 5
	x_pos = 10
	i = 0
	for d in distances:
		if d == 0:
			height = 1000
		else:
			height = 5000 / (d * 0.7)
		color = line_color[colors[i]]
		darken = (100 - d) / 100
		if darken < 0 :
			darken = 0.1
		darker_color = []
		for c in color:
			darker_color.append(c * darken)
		# print(darker_color)
		pygame.draw.line(screen, darker_color, (x_pos, 500 - height / 2), (x_pos, 500 + height / 2), 15)
		x_pos += 15
		i += 1

	# Aktualizacja ekranu
	pygame.display.flip()

# Zakończenie Pygame
pygame.quit()
sys.exit()



