import urllib2,requests,re,os,sys

file_list_of_ids=str(sys.argv[1])
if len(sys.argv) > 2:
	if_mp=str(sys.argv[2])
	num_of_cores=int(sys.argv[3])
	import multiprocessing as mp

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
	with open(doi + '.pdf', 'wb') as fw:
		fw.write(response.content)

	print 'Completed'
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
