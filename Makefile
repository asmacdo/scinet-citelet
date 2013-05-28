# Bundle JS files for bookmarklet and Chrome extension

all : seturl \
      js-src/_*.js \
      pytelet/static/js/citelet.min.js \
      pytelet/static/js/bookmarklet.js \
      ext/citelet.cat.js

# Minify src and contrib JS files and write to static/js
# Note: Order of JS files matters--must take _*.js files first, then 
# user-contributed files, then citelet.js
pytelet/static/js/citelet.min.js : js-src/_*.js js-contrib/*.js js-src/main.js
	python py-util/minify.py --wrap --minify --files $^ > pytelet/static/js/citelet.min.js

# Concatenate src and contrib JS files and write to ext
ext/citelet.cat.js : js-src/_*.js js-contrib/*.js
	python py-util/minify.py --files $^ > ext/citelet.cat.js 

# False dependency: Touch source files when utility files change
js-src/_*.js : py-util/minify.py js-util/wrapper.js
	touch js-src/_*.js

## Update URL in extension manifest
#ext/manifest.json : url
#	sed s/__url__/`sed s/:.*// url`/ ext/.manifest.json > ext/manifest.json
#
## Update URL in _citelet
#js-src/_citelet.js : url
#	sed s/__url__/`cat url`/ js-src/._citelet.js > js-src/_citelet.js
#
## Update URL in _citelet
#pytelet/static/js/bookmarklet.js : url
#	sed s/__url__/`cat url`/ pytelet/static/js/.bookmarklet.js \
#        > pytelet/static/js/bookmarklet.js

seturl : FORCE
	sed s/__url__/`echo $$CITELET_BASE_URL`/ js-src/._citelet.js > ./js-src/_citelet.js
	sed s/__url__/`echo $$CITELET_BASE_URL`/ pytelet/static/js/.bookmarklet.js \
        > ./pytelet/static/js/bookmarklet.js
	sed s/__url__/`echo $$CITELET_BASE_URL | sed s/:.*//`/ ext/.manifest.json \
        > ./ext/manifest.json
FORCE:
