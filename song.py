class Song(object):
	song_request = ""
	lyrics = ""

	def __init__(self, song_request, lyrics):
		self.song_request = song_request
		self.lyrics = lyrics

	def songlyrics(self):
		return self.lyrics

	def songname(self):
		return self.song_request





