#A script to automatically download torrents of my favorite show and hopefully invoke deluge to actually download them.
#Here goes nothing


import requests
import bs4
import re
import subprocess

import ConfigParser
import datetime
import os
from TVShow import TVShow

def download(proxy,downLoads):



	# for i in range(0,len(downLoads)):


	for i in range(0,len(downLoads)):
	 	startLink = proxy+'s/?q='+downLoads[i].name.replace(' ','+')+'&page=0&orderby=99'

	 	print 'Searching the web '+startLink
	 	response = requests.get(startLink)
	 	soup = bs4.BeautifulSoup(response.text,'lxml')
	 	# print downLoads[i].season
	 	# print downLoads[i].episode
	 	link=soup.find_all("a",href=re.compile('.*S'+downLoads[i].season+'E'+downLoads[i].episode+'\.\w*\.*HDTV\.(x264|xVID)\-\w*\\%5Bettv\%5D'))
	 	# link=soup.find_all("a",href=re.compile('.*S08E01\.\w*\.*HDTV\.(x264|xVID)\-\w*\\%5Bettv\%5D'))
	 	# print link[0]['href']

	 	print 'The Number of torrent links found '
	 	print len(link)
	 	if len(link) > 0 :

	 		response = requests.get(proxy+link[0]['href'])
	 		soup = bs4.BeautifulSoup(response.text,'lxml')
	 		link=soup.find_all("a",href=re.compile('magnet.*S'+downLoads[i].season+'E'+downLoads[i].episode+'\.\w*\.*HDTV\.(x264|xVID)\-\w*\\%5Bettv\%5D'))
	 		magnetUrl = link[0]['href']
	 		
	 		print 'Adding torrent with magnetURL '+magnetUrl 
	 		p=subprocess.Popen('deluge-console add '+magnetUrl,stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()
			print output
			downLoads[i].success = True

	 	else :
	 		print 'Torrents for the show '+downLoads[i].name+' Season '+downLoads[i].season+' Episode '+downLoads[i].episode+' Not available yet : ('
	 		downLoads[i].success = False

	return downLoads



#Driver, Pre&Post Processing code

if __name__ == '__main__':

	mydir = os.path.dirname(os.path.abspath(__file__))
	

	config = ConfigParser.ConfigParser()
	config.read(mydir+'/downloadTorrents.cfg')
	
	# determine day of week 
	now = datetime.datetime.now()
	today = now.strftime('%A')

#	today = 'Thursday'



	proxy = config.get('Proxy','name')

	numShows = len(config.get(today,'name').split(','))

	showNames = config.get(today,'name').split(',')

	seasonNumbers = config.get(today,'season').split(',')
	# premierDates = config.get(today,'season premiere date').split(',')
	episodeNumbers = config.get(today,'episode number').split(',')

	print 'Today is '+today+'. Shows slated for downloading are '+str(showNames)
	
	downLoads = [ TVShow("","","","","") for i in range(numShows)]

	for i in range(0,numShows):
		downLoads[i].name=showNames[i]
		downLoads[i].season=seasonNumbers[i]
		downLoads[i].episode=episodeNumbers[i]
		# downLoads[i].startDate=premierDates[i]
		downLoads[i].magnetURL=''


		
	# for i in range(0,numShows):
	# 	print downLoads[i].__dict__



	downLoads = download(proxy,downLoads)

	for i in range(0,numShows):
		if downLoads[i].success == True:
			print 'Torrent for '+downLoads[i].name +' got added successfully, so incrementing the cfg file to point to the next episode'
			ep=int(downLoads[i].episode)
			downLoads[i].episode = '%02d' %(ep+1) 

		
		episodeNumbers[i] = downLoads[i].episode

	
	
	updatedEpisodes = ",".join(episodeNumbers)

	

	config.set(today,'episode number',updatedEpisodes)	

	with open(mydir+'/downloadTorrents.cfg', 'w') as configfile:
		config.write(configfile)
    
		


