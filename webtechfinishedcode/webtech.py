'''
Web Tech Mini Project

Topic : Dom based web information extraction

Authors : Abhishek R S(12IT02) , Nikhil V(12IT46) ,Pradhynesh J(12IT ) , Shashank S(12IT58) ,

Extra Modules to be downloaded
mechanize
lxml

Please use the following command on Unix
sudo apt-get install python-mechanize
sudo apt-get install python-lxml

'''

#!/usr/bin/env python
import urllib					#library to make network requests
from lxml import html				#library to use xpath api
import re					#library used for handling regular expressions
import mechanize				#library which helps to open links in browser
import urlparse
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")


'''------------------------------------------------------------------------------------'''


url="http://www.indiatoday.intoday.in"
numberOfSteps=1					
finalUrls=[]					
myfile = open("foo.txt","w")

br=mechanize.Browser()				
br.set_handle_robots(False)			
br.addheaders = [('User-agent','Firefox')]	

lxmltree = etree.parse('myData.xml')
root = lxmltree.getroot()
head = lxmltree.find('News')
if head==None :
	element = etree.Element('News')
	root.append(element); 
head = lxmltree.find('News')


'''------------------------------------------------------------------------------------'''

def takelink(link):

	htmlfile = urllib.urlopen(link)
	htmltext = htmlfile.read()
	tree=html.fromstring(htmltext)

	paragraphs = tree.xpath('/html/body//div [ @class ="mediumcontent"]//p//text()')
	title = tree.xpath("//title/text()")
	category = tree.xpath('//span [ @itemprop = "title"]//text()')
	date = tree.xpath('/html/body//div [@class ="strstrap"]//text()')
		
	if paragraphs:
		count =0
		for item in category:
			print item
			count+=1
		print "Count :: ",count,"\n"

		topic = head.find( category[0])
		if topic==None :
			element = etree.Element(category[0])
			head.append(element);

		topic = head.find(category[0])
		mstr =""
		for item in title:
			mstr+=item
		element = etree.Element('Title',{'text' : mstr })
		topic.append(element);

		mstr=""
		for item in paragraphs:
			mstr+=item
		element = etree.Element('Body',{'text' : mstr })
		topic.append(element);

		lxmltree.write('myData.xml')


def scrapeThisStep(root):
	resultedUrls=[]	

	for url2 in root:
		try:
			br.open(url2)			
			#simulation of opening the link in the browser
			
			for newUrl in br.links():
				newLink = urlparse.urljoin(newUrl.base_url,newUrl.url)					
				resultedUrls.append(newLink)
				#add the newly founded link to the list containing the links of previous pages
		except:
			print("There was an error getting the Links")
	
	return resultedUrls

def scraper(root,steps):
	urls=[root]
	visited=[root]
	counter=0

	while counter<steps:
		thisStepUrl=scrapeThisStep(urls)
		urls=[]
		for u in thisStepUrl:
			if u not in visited:
				urls.append(u)
				visited.append(u)
		counter+=1
	
	return visited		
	 
finalUrls=scraper(url,numberOfSteps)
for lnk in finalUrls:
	takelink(lnk) 
myfile.close()