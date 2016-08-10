# -*- coding: utf-8 -*-  
import os
import sys
import commands
import json
import time
import pika
import urllib2
import basemodules as mo
import traceback
import socket
socket.setdefaulttimeout(60)
urllib2.socket.setdefaulttimeout(60) 

class RMQ_Manager:
	def __init__(self):
		self.initconn()
	def initconn(self):
		try:
			credentials = pika.PlainCredentials('***', '***')
			connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.12.200', credentials=credentials))
			self.channel = connection.channel() 
			self.declare()		
		except:
			mo.logger.error( "initconn failed: "%(str(sys.exc_info()) + "; " + str(traceback.format_exc())) )
	def declare(self):
		self.channel.exchange_declare(exchange='app_collect',type='topic',durable=True)
		self.channel.queue_declare(queue='video_collect', durable=True, exclusive=False, auto_delete=False, arguments={"x-max-priority":10})
		self.channel.queue_bind(exchange='app_collect', queue='video_collect', routing_key="video_collect")
	def send(self, msg):
		self.channel.basic_publish(exchange='app_collect',routing_key='video_collect',body=msg,
			properties=pika.BasicProperties(
			delivery_mode=2,priority=5, # make message persistent
		))
	def dispatch(self):
		pass



class VideosProcessor(RMQ_Manager):
	def __init__(self):
		RMQ_Manager.__init__(self)
	def dispatch(self):
		queues_old = []
		qobjs = {}
		while 1: #blocked reactor
			cont = None
			try:
				self.declare()
				r = self.channel.basic_get(queue="video_collect", no_ack=False) #0
				if r[0] != None:
					self.channel.basic_nack(delivery_tag=r[0].delivery_tag, multiple=False, requeue=False)
					#print "send sms:  ",r[-1]#, r[0].delivery_tag
					#process m3u8, get mp4 and download
					cont = r[-1]
					if not on_download(cont) and "url_backup=" in cont:
						mo.logger.warning("try to use url_backup: %s"%cont)
						cont = cont.replace("url=","url_over=").replace("url_backup=","url=")
						on_download(cont)
			except:
				mo.logger.error( str(sys.exc_info()) + "; " + str(traceback.format_exc()) )
				self.initconn()
				if cont != None:
					mo.logger.warning("Put back queue: %s"%cont)
					self.send(cont)
			time.sleep(1)


class download_type:
		MP4 = "video"
		AUDIO = "audio"

str_format_down_source = "%s_%s_%s.mp4"
str_format_down_target = "%s_%s.mp4"

def download_pkg(itemid,ptype,dtype,pkgurl):
		errinfo = ""
		for i in xrange(6):
			try:
					f = urllib2.urlopen(pkgurl)
					buf = f.read()
					f = open(str_format_down_source%(itemid,ptype,dtype), "wb+")
					f.write(buf)
					f.close()
					return True
			except:
					errinfo = "%s %s %s"%(itemid,str(sys.exc_info()),str(traceback.format_exc())) 
					time.sleep(i)
		mo.logger.error( errinfo )
		return False

def deco_m3ua(func):
		def _deco(argstr):
				#P34432555_default.m3u8 get child.m3ua
				if argstr.find("itemid=")!=-1 and argstr.find("type=")!=-1 and not argstr.endswith(".m3u8"):
						mo.logger.error("error arg: %s"%argstr)
						return False #ex.
				tmps = argstr.split("&", 4)
				if len(tmps) != 5:
						mo.logger.error("error arg: %s"%argstr)
						return False #ex.
				itemid = tmps[0].split("itemid=")[1]
				ptype = tmps[1].split("type=")[1]
				fname = tmps[2].split("name=")[1]
				fpath = tmps[3].split("path=")[1]
				url = tmps[4].split("url=")[1]
				if "&url_backup=" in url:
					url = url.split("&url_backup=")[0]
				mo.logger.info("Args: %s %s %s %s %s (%s)"%(itemid,ptype,fname,url,fpath,argstr))

				#parent.m3u8
				fobj = None
				for i in range(3):
					try:
						fobj = urllib2.urlopen(url)
						break
					except:pass
				lines = fobj.readlines() #if fobj None, throw excpt
				url_audio = None
				tmpdic = {} #BANDWIDTH:url
				##EXT-X-STREAM-INF:AVG_BANDWIDTH=564652,BANDWIDTH=726473,CLOSED-CAPTIONS=NONE,CODECS="avc1.64001f,mp4a.40.5",AUDIO="audio-64",RESOLUTION=306x544 http://apptrailers.itunes.apple.com/apple-assets-us-std-000001/PurpleVideo3/v4/05/70/94/05709479-9b5b-a2b9-c992-466ca834b8b1/P34430557_A558823262_en_video_gr7.m3u8
				index = -1
				for line in lines:
					index = index+1
					if "EXT-X-MEDIA" in line and url_audio==None:
						url_audio = line.split("URI=\"")[1][:-2]
						continue
					if not "EXT-X-STREAM-INF" in line:
						continue
					#print lines[index]
					#print lines[index+1]
					tmpdic[ int(line.split("BANDWIDTH=")[1].split(",",1)[0]) ] = lines[index+1]
					rets = sorted(tmpdic.keys())[:5] #[1,2,3...]

				#child.m3u8
				url_mp4 = None
				for ret in rets:
					#mo.logger.info("child.m3u8: %s. "%tmpdic[ret])
					fobj = None
					for i in range(6):
						try:
							fobj = urllib2.urlopen(tmpdic[ret])
							break
						except:pass
					if fobj == None:
						continue
					for line in fobj.readlines():
						if line.endswith(".mp4\n"):
							url_mp4 = tmpdic[ret].rsplit("/",1)[0]+"/"+line
							break
					if url_mp4 != None:
						#print url_mp4
						break
				if url_mp4 == None:
					mo.logger.error("%s can not fetch mp4 url. "%itemid)
					return False
				#audio
				fobj = None
				for i in range(6):
					try:
						fobj = urllib2.urlopen(url_audio)
						break
					except:pass
				if fobj != None:
					for line in fobj.readlines():
						if line.endswith(".mp4\n"):
							url_audio = url_audio.rsplit("/",1)[0]+"/"+line
							break
				if url_audio != None:
					#print url_audio
					pass
				else:
					mo.logger.warning("%s can not fetch audio url, only use video ! "%itemid)
					download_pkg(itemid,ptype,download_type.MP4,url_mp4)
					os.rename(str_format_down_source%(itemid,ptype,download_type.MP4), fname)
					upload_file(fname, fpath)
					mo.logger.info("%s ftp(%s) fin." % (itemid,url_mp4))
					return False
				
				return func( itemid,ptype,url_mp4.strip("\n"),url_audio.strip("\n"),fname,fpath )
		return _deco

def upload_file(target,fpath):
	ret,output = None,None
	for i in xrange(3):
		try:
			ret,output = mo.ftp_up(target,"192.168.102.201",'21',"video","***",fpath)
			if ret: break 
		except:
			continue
	return ret,output

@deco_m3ua
def on_download(*args):
		itemid,ptype,url_mp4,url_audio,fname,fpath = args
		mo.logger.info("%s downloading(%s)" % (itemid,url_mp4) )
		start = time.time()
		if not download_pkg(itemid,ptype,download_type.MP4,url_mp4):
			return False
		if not download_pkg(itemid,ptype,download_type.AUDIO,url_audio):
			return False
		mo.logger.info("%s downloaded(%s) %.03fs fin." % (itemid,url_mp4,time.time()-start))
		start = time.time()

		#merge now.
		source1 = str_format_down_source%(itemid,ptype,download_type.MP4)
		source2 = str_format_down_source%(itemid,ptype,download_type.AUDIO)
		target = fname #str_format_down_target%(itemid,ptype)
		os.system( "rm -f %s"%target )
		ret = os.system( "ffmpeg -i %s -i %s %s 1>.ffoutput 2>.fferror"%(source1,source2,target) )
		mo.logger.info("%s ffmpeg(%s) %.03fs fin." % (itemid,url_mp4,time.time()-start))
		start = time.time()

		retval = False
		#ftp upload.
		ret,output = upload_file(target,fpath)
		if not ret:	
			mo.logger.error( "%s %s"%(itemid,output) )
		else:
			retval = True
			mo.logger.info("%s ftp(%s) %.03fs fin." % (itemid,url_mp4,time.time()-start))
			start = time.time()

		#delete files local.
		try: 
			os.remove(source1) 
		except: pass
		try: 
			os.remove(source2) 
		except: pass
		try: 
			os.remove(target) 
		except: pass
		return retval


g_rmq_mgr = VideosProcessor()
g_rmq_mgr.dispatch()


#queue item: itemid=558823262&type=iphone5s&url=http://apptrailers.itunes.apple.com/apple-assets-us-std-000001/PurpleVideo5/v4/f8/7d/88/f87d887c-711a-29b7-1523-fc4af2d1ffe2/P34432555_default.m3u8
#on_download("itemid=558823262&type=iphone5s&url=http://apptrailers.itunes.apple.com/apple-assets-us-std-000001/PurpleVideo5/v4/f8/7d/88/f87d887c-711a-29b7-1523-fc4af2d1ffe2/P34432555_default.m3u8")

