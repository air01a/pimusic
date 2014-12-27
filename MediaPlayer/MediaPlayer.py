from mplayer import Player
import threading 
from time import sleep
import os
import random

class MediaPlayer:
	def getTimeLength(self):
		return self._mPlayer.length

	def getTimePos(self):
		return self._mPlayer.time_pos

	def getFileName(self):
		return self._mPlayer.filename

	def getPlayingInfo(self):
		filename = self._mPlayer.filename
		time_pos = self._mPlayer.time_pos
		length   = self._mPlayer.length
		
		return { 'filename':filename, 'time_pos':time_pos, 'length':length }

	def next(self):
		if not self._added:
			self._addFile()
		self._mPlayer.pt_step(1)
		
	def previous(self):
		back=self._playList.previous()
		if back!=None:
			self._mPlayer.loadfile(back,1)

	def _mediaPlayerThread(self):
		self._added=False
		while self._threadContinue:
			sleep(1)
			time_pos=self._mPlayer.time_pos
			if time_pos != None:
				if self._added and self._mPlayer.time_pos<3:
					self._added=False
				if (self._mPlayer.time_pos>self._mPlayer.length-1) and not self._added:
					self._addFile()
					self._added=True
				print "%s %i / %i" %(self._mPlayer.filename ,self.getTimePos(),self.getTimeLength())

	def seek(self,time):
		if time<self._mPlayer.length and time>=0:
			self._mPlayer.time_pos=time

	def stop(self):
		self._threadContinue=False
		self._thread._Thread__stop()
		self._mPlayer.quit()
		self._mPlayer = None
		self._thread = None

	def start(self):
                self._mPlayer = Player(("-ao alsa:device=bluetooth"))
                self._threadContinue = True
                self._thread = threading.Thread(None, self._mediaPlayerThread, None, (), {})
                self._thread.start()

	def _addFile(self):
		next=self._playList.next()
		if next!=None:
			self._mPlayer.loadfile(next,1)

	def pause(self):
		self._mPlayer.pause()
		self._playing = not self._playing

	def play(self):
		if _self._mPlayer == None:
			self.start()

		if not self._playing:
			if self._playingIndex == -1:
				self._addFile()
			else:
				self._mPlayer.pause()
			self._playing = True

	def setVolume(self,volume):
		if volume>=0 and volume<=100:
			self._mPlayer.volume=volume
		return self.getVolume()

	def increaseVolume(self):
		volume=self._mPlayer.volume
                volume+=10
		if volume>100:
			volume=100
		self._mPlayer.volume=volume
                return self._mPlayer.volume

	def decreaseVolume(self):
		volume=self._mPlayer.volume
		volume-=10
		if volume<0:
			volume=0

		self._mPlayer.volume=volume
		return self._mPlayer.volume

	def getVolume(self):
		return self._mPlayer.volume

	def __init__(self,playList):
		self._playing = False
		self._playList = playList
		self._playingIndex = -1
		self._mPlayer = None
		self._threadContinue = False
