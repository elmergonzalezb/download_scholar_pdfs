import urllib2,re,os,sys,imp

try:
	imp.find_module('requests')
	import requests
except ImportError:
	print 'You need to install \'requests\' module!'
	sys.exit()

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
	if len(doi)>259:
		doi=doi[:260]
	with open(doi + '.pdf', 'wb') as fw:
		fw.write(response.content)

	print 'Saved'
	print

def download_doi_pdf(doi):

	my_doi=doi

	doi=re.sub('[:]', '', doi)
	doi=re.sub(r'\s+', '+', doi)

	my_http='http://booksc.org/s/?q=' + doi + '&t=0'
	print my_http
	req = urllib2.Request(my_http)
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
			print 'Couldn\'t find the PDF link\n'
			return

		m=list(set(m))
		my_pdf='http' + m[0] + 'pdf'
		download_file(my_doi, my_pdf)

		with open('pdf_exists.txt', 'a+') as cf:
			print >>cf, my_doi

	else:
		print 'Couldn\'t find the PDF link'
		print

		return

def work(dois):

	for doi in dois:

		print '----------------------------------------'
		print

		if not os.path.isfile(doi+'.pdf'):
			print doi
			download_doi_pdf(doi)
		else:
			print doi + ' - Exists!'
			print 

file_list_of_ids=str(sys.argv[1])

with open(file_list_of_ids, 'r') as lf:
	dois = [line.rstrip() for line in lf]

saved_dois=[re.sub('_', '/', x.rstrip('.pdf')) for x in os.listdir('.') if x.endswith('pdf')]

if len(saved_dois)>0:

	print '\nThe PDF files for the below DOIs (N=' + str(len(saved_dois)) + ') are already downloaded/saved:\n'
	for i in saved_dois:
		print i

dois=[x for x in dois if x not in saved_dois]

try:
	imp.find_module('multiprocessing')
	num_of_cores = int(raw_input( '\n >> multiprocessing module was found.\n\n-Do you want to use multiple cores?\n\n-If yes, enter the number of cores(>1), else just type 1: '))
	import multiprocessing as mp
	if num_of_cores==1:
		work(dois)
	else:
		multi(dois,num_of_cores)
except ImportError:
	work(dois)
