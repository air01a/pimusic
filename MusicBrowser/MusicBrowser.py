# -*- coding:utf-8 -*-
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from sqlalchemy import or_
from webapp import db,models
import magic
import os
from hsaudiotag import auto

class MusicBrowser:
	def __init__(self,path):
		self._path=path
		self._musiqExtension=['.MP3','.WAV','.WMA','.MP4','.OGG','.FLAC','.AIFF']

	def _getInDb(self,path):
		mp3=models.Mp3_library.query.filter_by(fullpath=path).first()
		return mp3

	def getFileFromId(self,id):
		mp3=models.Mp3_library.query.get(id)
		return mp3

	def _setInDb(self,path):
		toUpdate=False
		ctime=os.stat(path).st_mtime
		
		current=self._getInDb(path)
		if current==None:
			toUpdate=True
		elif current.ctime!=ctime:
			db.session.delete(current)
			db.session.commit()
			toUpdate=True

		if toUpdate==True:
			print "DB Updating for %s" % (path)
			audioFile=auto.File(path)
			directory=os.path.dirname(path)
			filename=os.path.basename(path)
			mp3 = models.Mp3_library(path=directory, filename=filename, artist=audioFile.artist, album=audioFile.album, title=audioFile.title, fullpath=path, ctime=ctime)
			db.session.add(mp3)
			db.session.commit()

	def updateDB(self):
		for root, dirs, files in os.walk(self._path):
			for name in files :
				try:
					path = os.path.join(root, name).decode('utf8')
					if name.upper().endswith(tuple(self._musiqExtension)):
						self._setInDb(path)
				except:
					print "Error with file %s" %(name)

	def searchByAlbum(self,album):
		data=models.Mp3_library.query.filter(models.Mp3_library.album.like('%'+album+'%')).all()
		p =   [d.toDict() for d in data]
		return p

	def searchByArtist(self,artist):
                data=models.Mp3_library.query.filter(models.Mp3_library.artist.like('%'+artist+'%')).all()
                p =   [d.toDict() for d in data]
                return p

        def searchByTitle(self,title):
                data=models.Mp3_library.query.filter(models.Mp3_library.title.like('%'+title+'%')).all()
                p =   [d.toDict() for d in data]
                return p

	def search(self,search):
		data=models.Mp3_library.query.filter(or_(models.Mp3_library.album.like('%'+search+'%'),models.Mp3_library.artist.like('%'+search+'%'),models.Mp3_library.title.like('%'+search+'%'),models.Mp3_library.fullpath.like('%'+search+'%'))).all()
		p =   [d.toDict() for d in data]
                return p
		
