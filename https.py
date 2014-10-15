#!/usr/bin/python
from xml.dom.minidom import parseString
import logging
import subprocess
import ConfigParser

def usage():
    print "ehealthclient.py -p [port] -h [host]"


document = """\
<slideshow>
<title>Demo slideshow</title>
<slide><title>Slide title</title>
<point>This is a demo</point>
<point>Of a program for processing slides</point>
</slide>

<slide><title>Another demo slide</title>
<point>It is important</point>
<point>To have more than</point>
<point>one slide</point>
</slide>
</slideshow>
"""
output_toparse="/Users/iridium/Jobs/testManager/testManager/XMLRepository/nmap.txt"
with open(output_toparse,'r') as f:
				#result=result+ev_code+"$"+f.read()+"\n"
				xml_message=f.read()
dom = parseString(xml_message)
host=dom.getElementsByTagName("nmaprun")[0].getElementsByTagName("host")[0];
print "HOSTNAME: "+host.getElementsByTagName("hostname")[0].getAttribute("name")
port=host.getElementsByTagName("ports")[0].getElementsByTagName("port")[0]
print "PORT: "+port.getAttribute("portid")
print "PORT STATE: "+port.getElementsByTagName("state")[0].getAttribute("state")
print "SERVICE RUNNING: "+port.getElementsByTagName("service")[0].getAttribute("name")
ssl_scripts=port.getElementsByTagName("script")
for script in ssl_scripts:
	if script.getAttribute("id")=="ssl-cert":
		ssl_cert=script
	if script.getAttribute("id")=="ssl-enum-ciphers":
		ssl_cipher=script

table=ssl_cert.getElementsByTagName("table")
for info in table:
	if info.getAttribute("key")=="validity":
		values=info.getElementsByTagName("elem")	
		for value in values:
			if value.getAttribute("key")=="notBefore":
			
				print "NOT VALID BEFORE: "+value.childNodes[0].nodeValue
			if value.getAttribute("key")=="notAfter":
				
				print "NOT VALID AFTER: "+value.childNodes[0].nodeValue


table=ssl_cipher.getElementsByTagName("elem")
for info in table:
		
	if info.getAttribute("key")=="least strength":
		print "KEY STRENGTH:"+info.childNodes[0].nodeValue	
		

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def handleSlideshow(slideshow):
    handleSlideshowTitle(slideshow.getElementsByTagName("namprun")[0])
    slides = slideshow.getElementsByTagName("slide")
    handleToc(slides)
    handleSlides(slides)
    print "</html>"

def handleSlides(slides):
    for slide in slides:
        handleSlide(slide)

def handleSlide(slide):
    handleSlideTitle(slide.getElementsByTagName("title")[0])
    handlePoints(slide.getElementsByTagName("point"))

def handleSlideshowTitle(title):
    print "<title>%s</title>" % getText(title.childNodes)

def handleSlideTitle(title):
    print "<h2>%s</h2>" % getText(title.childNodes)

def handlePoints(points):
    print "<ul>"
    for point in points:
        handlePoint(point)
    print "</ul>"

def handlePoint(point):
    print "<li>%s</li>" % getText(point.childNodes)

def handleToc(slides):
    for slide in slides:
        title = slide.getElementsByTagName("title")[0]
        print "<p>%s</p>" % getText(title.childNodes)

#handleSlideshow(dom)
#try:     
#	opts, args = getopt.getopt(sys.argv[1:], "h:i:o:", ["host=","init=","output=","help"]) 
#except getopt.GetoptError:           
#        usage()                          
#        sys.exit(2)  
#
#for o, a in opts:
#			host=a
#		elif o in  ("-o","--output"):
#			output_folder = a+".log"
#		elif o in  ("-i","--init"):
#			config_file = a
#		else:
#			assert False, "unhandled option"


#sample_config=config_file
##print sample_config
#parser =  ConfigParser.RawConfigParser()
#with open(sample_config, 'r') as g:
#	parser.readfp(g)


#host=parser.get("1", "host")
#port=port.get("1","port")	
#output_toparse=+output_folder+".nmap.log"

#pathexecutor = "nmap -oX "+output_toparse+" -p "+port+" -script ssl-cert,ssl-enum-ciphers"+ host
#proc = subprocess.Popen([pathexecutor], stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()




#ports=dom.getElementsByTagName('ports')
#print ports.getElementsByTagName('service').item(0).item(0).getAttribute("name")
#for port in ports:
#port=collector.getAttribute('id')	
##get TestCases			
#testCases=collector.getElementsByTagName('TestCases').item(0).toxml()
#tot=collector.getAttribute("tot")
#app_coll=DoCollector(testCases,tot,dep_folder+"/"+collector_id,rep_folder)
#colls.append([collector_id,app_coll])