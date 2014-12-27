import os
import random

class PlaylistManager:
	def __init__(self):
		self._playList = []
		self._playingIndex = -1
		self._repeat = True

        def randomizePlayList(self):
                track=[self._playList[self._playingIndex]]
                del self._playList[self._playingIndex]
                random.shuffle(self._playList)
                self._playList = track+self._playList
                self._playingIndex=0

        def loadPlayList(self, path):
                if os.path.isfile(path):
                        plst = open(path+".plt", "rt")
                        self.playList=[]
                        for line in plst:
                                if os.path.isfile(line.rstrip()):
                                        self._playList.append(line.rstrip())
                        self.playingIndex=-1
			return True
		return False

	def listPlayList(self,path):
		playlist=[]
		for (dirpath, dirnames, filenames) in os.walk(path):
			for filename in filenames:
				if filename.split(".")[-1]=='plt':
					playlist.append(filename.split(".")[0])
		return playlist

	def savePlayList(self,path):
		try:
			plst = open(path+'.plt',"w")
			for line in self._playList:
				plst.write(line+"\n")
			plst.close()
			return True
		except:
			return False

        def addFile(self,path):
                self._playList.append(path)

        def getPlayList(self):
                return self._playList

	def next(self):
		if self._playingIndex < len(self._playList)-1:
			self._playingIndex+=1
			return self._playList[self._playingIndex]
		if self._repeat and len(self._playList)>0:
			self._playingIndex=0
			return self._playList[self._playingIndex]
		return None

	def previous(self):
		if self._playingIndex>0:
			self._playingIndex-=1
			return self._playList[self._playingIndex]

		if self._repeat and len(self._playList)>0:
			self._playingIndex=len(self._playList)-1
			return self._playList[-1]
		return None

if __name__=='__main__':
	pl=PlaylistManager()
	pl.addFile("/media/disk1/Multimedia/Musique/Tragedie - Hey Oh.mp3")
	pl.addFile("/media/disk1/Multimedia/Musique/Ben E King - Stand by me.mp3")
	pl.addFile("3.mp3")
	pl.addFile("4.mp3")
	print pl.next()
	print pl.next()
	print pl.getPlayList()
	pl.randomizePlayList()
	print pl.getPlayList()
