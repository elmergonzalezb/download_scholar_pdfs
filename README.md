# Download Scholar PDFs from DOI files
This repository hosts a simple, short script that allows batch .PDF downloading from a list of DOIs and/or titles. PDF files are retrieved/downloaded from libgen scholar archives.

Recommended sqlite3 version : 2.6.0 

The downloader.py script can be used from command line, as such:

$python downloader.py list_of_dois_or_titles.txt false 1  /path/to/download/ > /path/to/log

If you already have a list of DOI files you want to import into the database you can use :

$python doi_import_to_sqlite.py list_of_dois_or_titles.txt

The script will detect if the 'multiprocessing' module is installed, and will ask you for the number of cores you may want to put into use (just to speed up the http request / .PDF downloading process). If you want to avoid multiprocessing, enter 1.

You can run the script multiple times, just keep then running in different directories as it will create a database to store the results in the script current directory. You can use the /path/to/download/ to redirect output of all scripts to a single folder.
