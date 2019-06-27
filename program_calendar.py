#!/usr/bin/python
# coding: latin-1

from flask import Flask, redirect, url_for,request, render_template
import json
import requests
import time 

gmt_time = time.strftime("%Y-%m-%d %I:%M:%S", time.gmtime()).replace(' ','T')

local_time = time.strftime("%Y-%m-%d %I:%M:%S").replace(' ','T')

app = Flask(__name__)

def get_contests(resource_id,gmt):
	
	start_time = local_time
	if gmt==1:
		start_time = gmt_time	

	headers = {
		"charset": "utf-8",
		"content-type": "application/json"
	}

	p = { 
		"username": "af",
		"api_key": "55f76864bb0e15222562c22b40b63986987434cf",
		"resource__id": resource_id,
		"start__gt": start_time,
		"order_by": "start", 
		"limit": 10
	}

	r = requests.get('https://clist.by:443/api/v1/contest/', params=p, headers=headers)
	print r.status_code
	print type(r.status_code)
	if r.status_code==200:
		content = json.loads(r.content)
		contests = content['objects']
		contest_lists = []
		for contest in contests:
			start =  str(contest['start']).split('T')
			end = str(contest['start']).split('T')
			contest_lists.append([contest['event'],contest['href'],start[0],start[1],end[0],end[1]])
		return contest_lists
	else:
		return []
		

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/codeforces')
def codeforces():
	resource_id = 1
	contests = get_contests(resource_id,gmt=1)
	return render_template('contests.html', res='codeforces', contests=contests)

@app.route('/codechef')
def codechef():
	resource_id = 2
	contests = get_contests(resource_id,gmt=0)
	return render_template('contests.html', res='codechef', contests=contests)

@app.route('/topcoder')
def topcoder():
	resource_id = 12
	contests = get_contests(resource_id,gmt=0)
	return render_template('contests.html', res='topcoder', contests=contests)

@app.route('/hackerearth')
def hackerearth():
	resource_id = 73
	contests = get_contests(resource_id,gmt=0)
	return render_template('contests.html', res='hackerearth', contests=contests)

@app.route('/hackerrank')
def hackerrank():
	resource_id = 63
	contests = get_contests(resource_id,gmt=0)
	return render_template('contests.html', res='hackerrank', contests=contests)




if __name__ == '__main__':
	app.run(host='192.168.43.7',port=5000)


