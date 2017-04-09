

#! /usr/bin/python

import sys
import socket
import urllib
import gzip
import os


try:
	import pygeoip

except ImportError:
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


			elif choice.strip().lower()[0]=='n':
				print '[!] user Denied auto-install'
				sys.exit(1)

			else:
				print '[!] Invalid choice'
				sys.exit(1)



	def query(self):
		if not self.url:
			print '[*] Translating %s: ' %(self.url)
			sys.stdout.flush()

			try:
				self.target += socket.gethostbyname(self.url)
				print self.target

			except Exception:
				print '\n [!] Failed to Resolve URL'
				return

			else:
				self.target += self.ip

			try:
				print '[*] Querying for records of %s ...\n' %(self.target)
				query_obj = pygeoip.GeoIP(self.datfile)
				for key, val in query_obj.record_by_addr(self.target).items():
					print '%s: %s' %(key, val)

				print '[*] Query Complete!'
			except Exception:
				print '\n[!] Failed To Retrieve Records'
				return




if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description = 'IP Geolocation Tool')
	parser.add_argument('--url', help='locate a IP based on URL', action='store', Default='False', dest='url')
	parser.add_argument('-t', '--target', help='locate the specified IP ', action='store', Default='False', dest='ip')
	parser.add_argument('--dat', help='Custom Database filepath', action='store', Default='False', dest='datfile')
	args = parser.parse_args() 



if ((not not args.url) and (not not args.ip) or (not args.url) and (not args.ip)):
	parser.error('Invalid target specification')

try:
	Locator_object = Locator(url=args.url, ip=args.ip, datfile=args.datfile)
	Locator_object.check_database()
	Locator_object.query()

except Exception:
	print '\n\n [!] UNKNOWN ERROR OCCURED'

except KeyboardInterrupt:
	print '\n\n [!] UNEXPECTED USER interrupt'
	sys.exit(1)