from webapp import db

class Mp3_library(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	path = db.Column(db.String(500),index=True)
	filename = db.Column(db.String(255),index=True)
	artist = db.Column(db.String(255),index=True)
	album = db.Column(db.String(255),index=True)
	title = db.Column(db.String(255),index=True)
	fullpath = db.Column(db.String(500),index=True,unique=True)
	ctime = db.Column(db.Integer)

	def __repr__(self):
		print "< %i : %s %s %s %s %s %s %i>" % (self.id, self.path, self.filename, self.artist, self.album, self.title, self.fullpath, self.ctime)

	def toDict(self):
		return {'id':self.id,'path':self.path,'filename':self.filename,'artist':self.artist,'album':self.album,'title':self.title,'fullpath':self.fullpath,'ctime':self.ctime}


