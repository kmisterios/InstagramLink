# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect
from firstapp import app
from firstapp.forms import LinkForm
from firstapp.model_stuff.checking_string import do_things
from firstapp.comments_parser import parseinst
import json

import crochet
crochet.setup() 
from firstapp.instspider.spiders.comment_spider import QuotesSpider
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

ind = 0
output_data = []
crawl_runner = CrawlerRunner()

@app.route('/')
def home():
	return redirect('/links')
	
#def scrape():
    # run crawler in twisted reactor synchronously
    #scrape_with_crochet()
    #print(output_data)
    #return json.dumps([item for item in output_data])


@app.route('/links', methods=['GET', 'POST'])
def link():
	form = LinkForm()
	if form.validate_on_submit():
		scrape_with_crochet(form.link.data)
		if (len(output_data) == ind) and (output_data[len(output_data)-1] != 'error'):
			flash('Плохих комментариев {}'.format(do_things(parseinst(output_data[len(output_data)-1]['idstr']))))
			return redirect('/index')
		else:
			flash('Incorrect input!')
			return redirect('/links')
	return render_template('links.html', title='Enter your link', form=form)

@crochet.wait_for(timeout=60.0)
def scrape_with_crochet(link):
    # signal fires when single item is processed
    # and calls _crawler_result to append that item
    global ind
    ind = len(output_data) + 1
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(QuotesSpider, link = link)#'https://www.instagram.com/p/B3rxYQ6IBWL/')
    return eventual  # returns a twisted.internet.defer.Deferred
    
def _crawler_result(item, response, spider):
	#output_data = []
	if len(dict(item)) == 0:
		output_data.append('error')
	else:
		output_data.append(dict(item))
	
@app.route('/index')
def index():
	user = {'username': 'Лёха'}
	posts = [
		{
			'author': {'username': 'Миша'},
			'body': 'Я сделаль! :)'
		}
	]
	return render_template('index.html', title='Results', user=user, posts=posts)
