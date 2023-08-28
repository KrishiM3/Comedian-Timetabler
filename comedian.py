import demographic

#Class for storing a comedian object, which tracks their name, and themes
#themes are a list of strings
#name is a string

class Comedian:

	def __init__(self,name="", themes=list()):
		self.name=name
		self.themes=themes

	
	def setName(self,name):
		self.name = name

	
	def setThemes(self,themes):
		self.themes = themes

	
	def addTheme(self,theme):
		self.themes.add(theme)

	def __str__(self):
		return str([self.name, self.themes])

	def __repr__(self):
		return str(self)
