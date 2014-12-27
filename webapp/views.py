from flask import render_template, flash, redirect, Response, request, abort
from webapp import webapp
from config import PATH, PLAYLISTPATH
from PlaylistManager import PlaylistManager
from MusicBrowser import MusicBrowser
from MediaPlayer import MediaPlayer
import json
import os

musicBrowser = MusicBrowser.MusicBrowser(PATH)
playList     = PlaylistManager.PlaylistManager()
mediaPlayer  = MediaPlayer.MediaPlayer(playList)

@webapp.route('/')
@webapp.route('/index')
def index():
    return render_template('index.html',
                           title='Home')

@webapp.route('/api/v1/searchbyalbum',methods=['GET'])
def searchByAlbum():
	if 'q' in request.args:
		return Response(json.dumps(musicBrowser.searchByAlbum(request.args.get('q'))))
	abort(404)

@webapp.route('/api/v1/searchbyartist',methods=['GET'])
def searchByArtist():
        if 'q' in request.args:
                return Response(json.dumps(musicBrowser.searchByArtist(request.args.get('q'))))
        abort(404)

@webapp.route('/api/v1/searchbytitle',methods=['GET'])
def searchByTitle():
        if 'q' in request.args:
                return Response(json.dumps(musicBrowser.searchByTitle(request.args.get('q'))))
        abort(404)

@webapp.route('/api/v1/search',methods=['GET'])
def search():
        if 'q' in request.args:
                return Response(json.dumps(musicBrowser.search(request.args.get('q'))))
        abort(404)

@webapp.route('/api/v1/play',methods=['GET'])
def play():
	mediaPlayer.play()
	return Response(json.dumps({'error':0}))

@webapp.route('/api/v1/stop',methods=['PUT','POST'])
def stop():
	mediaPlayer.stop()
	return Response(json.dumps({'error':0}))

@webapp.route('/api/v1/pause',methods=['GET'])
def pause():
        mediaPlayer.pause()
	return Response(json.dumps({'error':0}))

@webapp.route('/api/v1/next',methods=['GET'])
def next():
        mediaPlayer.next()
	return Response(json.dumps({'error':0}))

@webapp.route('/api/v1/previous',methods=['GET'])
def previous():
        mediaPlayer.previous()
	return Response(json.dumps({'error':0}))

@webapp.route('/api/v1/saveplaylist',methods=['POST','PUT'])
def savePlayList():
	if 'name' in request.form:
		name=os.path.join(PLAYLISTPATH,os.path.basename(request.form.get('name')))
		if not playList.savePlayList(name):
			abort(500)
		return Response(json.dumps({'error':0}))
	abort(404)	
		
@webapp.route('/api/v1/addtoplaylist',methods=['POST','PUT'])
def addToPlayList():
	if 'id' in request.form:
		id=int(request.form['id'])
		music=musicBrowser.getFileFromId(id)
		if music==None:
			abort(500)
		playList.addFile(music.fullpath)
		return Response(json.dumps({'error':0}))
	abort(404)

@webapp.route('/api/v1/getplaylist',methods=['GET'])
def getPlayList():
	return Response(json.dumps(playList.getPlayList()))

@webapp.route('/api/v1/listplaylist',methods=['GET'])
def listPlayList():
	return Response(json.dumps(playList.listPlayList(PLAYLISTPATH)))

@webapp.route('/api/v1/loadplaylist',methods=['POST','PUT'])
def loadPlayList():
	if 'name' in request.form:
                name=os.path.join(PLAYLISTPATH,os.path.basename(request.form.get('name')))
		if not playList.loadPlayList(name):
                        abort(500)
		return Response(json.dumps(playList.getPlayList()))
	abort(404)

@webapp.route('/api/v1/increasevolume',methods=['POST','PUT'])
def increaseVolume():
	return Response(json.dumps(mediaPlayer.increaseVolume()))


@webapp.route('/api/v1/decreasevolume',methods=['POST','PUT'])
def decreaseVolume():
        return Response(json.dumps(mediaPlayer.decreaseVolume()))

@webapp.route('/api/v1/setvolume',methods=['POST','PUT'])
def setVolume():
	if 'volume' in request.form:
		try: 
			volume=int(request.form.get('volume'))
		except:
			abort(500)
		
	        return Response(json.dumps(mediaPlayer.setVolume(volume)))
	abort(404)

@webapp.route('/api/v1/getvolume',methods=['GET'])
def getVolume():
	return Response(json.dumps(mediaPlayer.getVolume()))


@webapp.route('/api/v1/getplayerinfo',methods=['GET'])
def playerInfo():
	return Response(json.dumps(mediaPlayer.getPlayingInfo()))

@webapp.route('/api/v1/goto', methods=['PUT','POST'])
def goTo():
	if 'position' in request.form:
		try:
                        position=int(request.form.get('position'))
			mediaPlayer.seek(position)
		except:
                        abort(500)
	return playerInfo()

