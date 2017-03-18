#Abstraction of a TV Show


class TVShow:

	def __init__(self, name, season, magnetURL,episode,success):
		self.name=name
		self.season=season
		self.episode=episode
		# self.startDate=startDate
		self.magnetURL=magnetURL
		self.success = False

