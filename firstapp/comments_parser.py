from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import numpy as np
from igramscraper.instagram import Instagram
import json
import firstapp.instspider
import pickle

def parseinst(idstr):
	ind = idstr.index('=') + 1
	idstr = idstr[ind:]
		
	instagram = Instagram()
	instagram.with_credentials('grouchysalmon', 'ulofob37', '')
	instagram.login()
	
	comments = instagram.get_media_comments_by_id(idstr, 10000)
	k = 0
	comments_list = []
	for comment in comments['comments']:
		k +=1
		comments_list.append(comment.text)
		#print(comment.owner)
	print(k)
	return comments_list
    #with open('comments.txt', 'wb') as f:
        #pickle.dump(comments_list,f)

#parseinst('https://www.instagram.com/p/B503dRlAGf7/')
