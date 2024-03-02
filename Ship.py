class Ship: 
	def __init__(self,ship_type, ship_orientation, starting_location):
		self.s_type = ship_type
		self.ship_orientation = ship_orientation
		self.starting_location = starting_location
		self.locations = [] # let the first coordinate in this list be the starting index of the ship (left to right/top to bottom)
		self.hit = False
		self.mini_locations_hit = 0
		self.rows = 10
		self.cols = 10

		# set ship size
		if self.s_type == 1: # Carrier
			self.ship_size = 5
		elif self.s_type == 2: # Battleship
			self.ship_size = 4
		elif self.s_type == 3: # Cruiser
			self.ship_size = 3
		elif self.s_type == 4: # Submarine
			self.ship_size = 3
		elif self.s_type == 5: # Destroyer
			self.ship_size = 2

	def increment_mini_locations():
		mini_locations_hit += 1
		if mini_locations_hit == self.ship_size:
			self.hit = True

	def get_hit_status():
		return self.hit

	def add_ship(self): 
	# checks if ship is valid based on board size constraints. if so, eliggible to add to board AND returns true. if not, returns False
		# check validity of the ship based on size constraints only and not on game board availability
		starting_row, starting_col = self.starting_location[0],self.starting_location[1]
		if self.ship_orientation == "H":
			if starting_col + self.ship_size > self.cols:
				return False
			else:
				for col in range (starting_col, starting_col+self.ship_size):
					self.locations.append((starting_row, col))
		elif self.ship_orientation == "V":
			if starting_row + self.ship_size > self.rows:
				return False
			else:
				for row in range (starting_row, starting_row+self.ship_size):
					self.locations.append((row, starting_col))
		return True
