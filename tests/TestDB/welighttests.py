'''
@author: Patrizio Tufarolo <patrizio.tufarolo@studenti.unimi.it>
'''

from patlib import SSHClient
from requests import session
from BeautifulSoup import BeautifulSoup
import MySQLdb,json


class Tester(object):
	def __init__(self):
		'''self.hostname = hostname
		self.username = username
		self.keyfile = keyfile
		self.serverkeyfile = serverkeyfile
		self.ssh_port = ssh_port'''

	def loginAndGetCookies(ctx,baseUrl,loginUrl,username,password):

		loginData = {
			'username':username,
			'password':password
		}
		s = session()
		cookies = dict(s.cookies)

		s.headers.update({'referer': baseUrl})
		s.get(baseUrl,verify=False,cookies=cookies)

		csrftoken = s.cookies['csrftoken']
		s.headers.update({'X-CSRFToken':csrftoken})
		req = s.post(loginUrl,data=loginData,verify=False,cookies=cookies)
		#print req.text
		return s

	def getInputValues(ctx,s,url,ids):
		cookies = dict(s.cookies)
		req = s.get(url,verify=False,cookies=cookies)
		val = req.text
		val.encode('utf-8')
		parsed_html = BeautifulSoup(val)

		input_values = []
		for id in ids:
			input_value = parsed_html.body.find('input', attrs={'id':id})['value']
			input_values.append(input_value)
		return input_values
		#ip = parsed_html.body.find('input', attrs={'id':'id_ip'})['value']
		#pwd = parsed_html.body.find('input', attrs={'id':'id_password'})['value']

	def mysqlConnect (self,dbHost='127.0.0.1',dbPort=3306,dbUser='root',dbPassword='',dbName=''):
		db = MySQLdb.connect(host=dbHost,port=dbPort,db=dbName,user=dbUser,passwd=dbPassword)
		return db

	def mysqlGetFields(self,mysql,tableToCheck='',fieldUnique='',valueUnique='',fieldsToGet=[]):
		result = []
		cursor = False
		try:
			for fieldToGet in fieldsToGet:
				cursor = mysql.cursor()
				query = """SELECT %s FROM %s WHERE %s=%s""" % (fieldToGet, tableToCheck, fieldUnique, valueUnique)
				cursor.execute(query)
				query_result = cursor.fetchone()
				cursor.close()
				result.append(query_result)
		except Exception as e:
			try:
				if (cursor):
					cursor.close()
			except:
				pass
			raise Exception, str(e)
		return result