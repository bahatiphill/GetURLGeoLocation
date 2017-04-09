

#! /usr/bin/python

import sys
import socket
import urllib
import gzip
import os


try:
	import pygeoip

except importError:
	print "[!] Failed to import pygeoip"

	try:
		choice = raw_input('[*] Attempt to auto-install pygeoip? [y/n]')

	except KeyboardInterrupt:
		print '\n [!] User interrupted choice'
		sys.exit(1)

	if choice.strip().lower()[0] == 'y':
		print "[*] Attempting to install pygeoip..."
		sys.stdout.flush()
		try:
			import pip
			pip.main(['install', '-q', 'pygeoip' ])
			import pygeoip
			print "[DONE]"

		except Exception:
			print "[FAIL]"
			sys.exit(1)

	elif choice.strip().lower()[0] == 'n':
		print'[*] User Denied auto-install'
		sys.exit(1)

	else:
		print '[*] Invalid Decision'
		sys.exit(1)





class Locator(object):
	
	def __init__(self, url=False, ip=False, datfile=False):
		self.url = url
		self.ip = ip
		self.datfile = datfile
		self.target = ''




	def check_database(self):
		if not self.datfile:
			self.datfile = '/usr/share/GeoIP/GeoLiteCity.dat'

		else:
			if not os.path.isfile(self.datfile):
				print "[!] Failed to Detect specified Database"
				sys.exit(1)	

			else:
				return

		if not os.path.isfile(self.datfile):
			print '[-] Default Database Detection Failed'

			try:
				choice = raw_input('[*] Attempt to auto-install Database? [y/n]')

			except KeyboardInterrupt:
				print '\n [*] User interrupted choice'
				sys.exit(1)

			if choice.strip().lower()[0] == 'y':
				print '[*] Attempting to auto-install Database...'
				sys.stdout.flush()

				if not os.path.isdir('/usr/share/GeoIP'):
					os.makedirs('/usr/share/GeoIP')

					try:
						urllib.urlretrieve('http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz', '/usr/share/GeoIP/GeoLiteCity.dat.gz')

					except:
						print '[FAIL]'
						print '[!] Failed to download Database'
						sys.exit(1)


				try:
					with gzip.open('/usr/share/GeoIP/GeoLiteCity.dat.gz', 'rb') as compressed_dat:
						with open('/usr/share/GeoIP/GeoLiteCity.dat', 'wb') as new_dat:
							new_dat.write(compressed_dat.read())

				except IOError:
					print '[FAIL]'
					print '[!] Failed to Decompress Database'
					sys.exit(1)
				os.remove('/usr/share/GeoIP/GeoLiteCity.dat.gz')
				print'[DONE]'


			elif choice.strip().lower()[0]='n':
				print '[!] user Denied auto-install'
				sys.exit(1)

			else:
				print '[!] Invalid choice'
				sys.exit(1)







		
		