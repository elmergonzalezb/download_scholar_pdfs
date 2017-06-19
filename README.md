# download_scholar_pdfs
This is repository hosts a simple, short script that allows batch .PDF downloading from a list of DOIs and/or titles. PDF files are retrieved/download from libgen scholar archives.

The batch_download.py script can be used from command line, as such:

$python batch_download.py list_of_dois_or_titles.txt

If you have multiple CPU cores available and want to use multiprocessing architecture to speed up the http request / .PDF downloading process, use as such:

$python batch_download.py list_of_dois_or_titles.txt True 10

(where True is True for multiprocessing and next the number of available cores as an integer)
