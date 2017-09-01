import re,os,sys,sqlite3

file_list_of_ids=str(sys.argv[1])

# Open SQLite database and create table if it does not already exist. Failed column is for future use, if there is a need to skip DOIs that always fail.
conn = sqlite3.connect('doi_log.sqlite')
c = conn.cursor()
try:
	c.execute('''CREATE TABLE IF NOT EXISTS journals (doi TEXT PRIMARY KEY, downloaded INTEGER, failed INTEGER);''')
except sqlite3.IntegrityError:
	print 'Error creating SQLite table'
	sys.exit()

conn.commit()

def add_to_db(doi):

	# If PDF saved, add it to database table.
	try:
		# downloaded column = 1, failed column = 0; IGNORE if DOI already present in DB.
		c.execute("INSERT OR IGNORE INTO journals (doi,downloaded,failed) VALUES (?,1,0)", (doi,))
		conn.commit()
	except sqlite3.IntegrityError:
		print 'Error creating SQLite table'
		sys.exit()


with open(file_list_of_ids, 'r') as f:
	for line in f:
		line.rstrip() 
		if re.match(r'^10',line):
			if re.match(r'.+?already downloaded per database record$',line):
				print 'Already in DB'
				print
			else:
				print 'Adding DOI ' + line + ' to DB'
				print
				add_to_db(line)