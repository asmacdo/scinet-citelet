# Citelet

## Organization:

* js-src: Base modules for extracting article meta-data
* js-contrib: User-contributed modules for extracting article meta-data
* js-util: Miscellaneous JS utility functions
* py-util: Miscellaneous Python utility functions
* app/: Flask app
* chrome-ext/: Code for Chrome extension

## How to run Citelet from localhost:

* Start a mongod instance
    * mongod
* Start a Flask server:
    * python app/main.py
* Browse to the bookmarklet page
    * http://localhost:5000/bookmarklet
* Drag the bookmarklet to your bookmarks bar
* Browse to an article
* Click the bookmarklet
