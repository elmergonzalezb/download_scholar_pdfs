# download_scholar_pdfs
This repository hosts a simple, short script that allows batch .PDF downloading from a list of DOIs and/or titles. PDF files are retrieved/downloaded from libgen scholar archives.

The batch_download.py script can be used from command line, as such:

$python batch_download.py list_of_dois_or_titles.txt

The script will detect if the 'multiprocessing' module is installed, and will ask you for the number of cores you may want to put into use (just to speed up the http request / .PDF downloading process). If you want to avoid multiprocessing, enter 1.
