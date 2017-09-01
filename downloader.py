import urllib2,requests,re,os,sys,httplib,sqlite3

file_list_of_ids=str(sys.argv[1])

if len(sys.argv) > 2:
	if_mp=str(sys.argv[2])
	num_of_cores=int(sys.argv[3])
	import multiprocessing as mp

# Check to see if output directory exists.
if not os.path.isdir(sys.argv[4]):
	print 'Arg #4. ' + sys.argv[4] + ' does not exist'
	print
	sys.exit()
	
# Output directory must have trailing slash.
if not re.match(r'\/$', sys.argv[4]):
	sys.argv[4] = sys.argv[4] + '/'
	

# Open SQLite database and create table if it does not already exist. Failed column is for future use, if there is a need to skip DOIs that always fail.
conn = sqlite3.connect('doi_log.sqlite')
c = conn.cursor()
try:
	c.execute('''CREATE TABLE IF NOT EXISTS journals (doi TEXT PRIMARY KEY, downloaded INTEGER, failed INTEGER);''')
except sqlite3.IntegrityError:
	print 'Error creating SQLite table'
	sys.exit()

conn.commit()
	
def chunks(l, n):

	for i in range(0, len(l), n):
		yield l[i:i + n]

def multi(dois,num_of_cores):

	u=int(len(dois)/(num_of_cores*1.0))
	pool = mp.Pool(processes=num_of_cores)
	pool.map(func=work, iterable=chunks(dois,u))
	pool.close()
	pool.join()

def download_file(doi, download_url):
	response = requests.get(download_url)
	doi=re.sub('/', '_', doi)
	with open(sys.argv[4] + doi + '.pdf', 'wb') as fw:
		fw.write(response.content)

	print 'Completed'
	print

	# If PDF saved, add it to database table.
	try:
		# downloaded column = 1, failed column = 0
		c.execute("INSERT INTO journals (doi,downloaded,failed) VALUES (?,1,0)", (doi,))
		conn.commit()
	except sqlite3.IntegrityError:
		print 'Error creating SQLite table'
		sys.exit()

def download_doi_pdf(doi):

	my_doi=doi
	
	doi=re.sub('[:]', '', doi)
	doi=re.sub(r'\s+', '+', doi)

	my_http='http://booksc.org/s/?q=' + doi + '&t=0'
	print my_http
	req = urllib2.Request(my_http)
	# Catch exceptions for url request.
	try:
		response = urllib2.urlopen(req)
		the_page = response.read()

		if re.search(r'On your request nothing has been found',the_page):
			print 'No results found'
			print
			return

		m=re.findall(r'href="http(.*?)\ title',the_page)

		for i in m:
			if not re.search('xml',i):
				my_link='http' + i
				break

		if 'my_link' in locals():

			my_link=my_link[:-1]
			my_link=re.sub('\"', '', my_link)
			req = urllib2.Request(my_link)
			response = urllib2.urlopen(req)
			the_page = response.read()

			m=re.findall(r'source="http(.*?)pdf',the_page)
			if len(m)==0:
				print 'Couldn\'t find the PDF link'
				print
				with open('cdnt.txt', 'a+') as cf:
					print >>cf, my_doi
				return
			m=list(set(m))
			my_pdf='http' + m[0] + 'pdf'
			download_file(my_doi, my_pdf)

		else:
			print 'Couldn\'t find the PDF link'
			print
			with open('cdnt.txt', 'a+') as cf:
				print >>cf, my_doi
			return
	# Handle exceptions for URL request; without this the script terminates on a Network/HTTP error.
	except urllib2.HTTPError, e:
		print 'HTTP Error'
	except urllib2.URLError, e:
		print 'URL Error'
	except httplib.HTTPException, e:
		print 'HTTP Exception'
	except Exception:
		import traceback
		print 'generic exception: ' + traceback.format_exc()
	return


def work(dois):

	for doi in dois:

		print '----------------------------------------'
		print

		# Local file check, proceed to DB check if file is not stored locally.
		if not os.path.isfile(sys.argv[4] + doi+'.pdf'):
			# DB lookup if uploading DOIs after retrieval without interrupting script.
			# clean DOI by replacing slashes with underscores
			sanitized_doi=re.sub('/','_',doi)
			# Catch SQL Exceptions
			try:
				# Retrieve row from DB for this DOI; parameter query to avoid SQL injection. Only one row, DOI is unique. No need to scan entire table.
				c.execute("SELECT * FROM journals WHERE doi = ? LIMIT 1", (sanitized_doi,))
				# Extract the row returned.
				doi_row = c.fetchone()
				# if doi is in table
				if doi_row:
					# if DOI is downloaded
					if doi_row[1] == 1:
						# do nothing
						print doi + " - already downloaded per database record"
						print
				# doi is not in table, download it
				else:
					print doi
					download_doi_pdf(doi)
			# Handle SQl Exceptions	
			except sqlite3.IntegrityError:
				print "SQL Error"
				sys.exit()
		# File exists locally, skip.
		else:
			print doi + ' - Exists!'
			print 
		
		


os.system('cat cdnt.txt | sort | uniq > cdnt.txt')

with open(file_list_of_ids, 'r') as f:
	dois = [line.rstrip() for line in f]

with open('cdnt.txt', 'r') as f:
	not_dois = [line.rstrip() for line in f]

dois=[x for x in dois if x not in not_dois]

if if_mp=='True':
	multi(dois,num_of_cores)
else:
	work(dois)
