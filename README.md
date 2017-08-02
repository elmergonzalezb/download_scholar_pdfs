# download_scholar_pdfs
This repository hosts a simple, short script that allows batch .PDF downloading from a list of DOIs and/or titles. PDF files are retrieved/downloaded from libgen scholar archives.

The batch_download.py script can be used from command line, as such:

$python batch_download.py list_of_dois_or_titles.txt

If you have multiprocessing module installed and want to put it into use to speed up the http request / .PDF downloading process, use as such:

$python batch_download.py list_of_dois_or_titles.txt N

(where N is the number of cores you may want to utilize)
