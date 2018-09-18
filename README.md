ISAexplorer
===========

This site has been developed to provide a visualization of ISATab files and it can be used to host a lightweight ISATab repository.
It runs on a Node.js environment and relies on python to load the datasets.

Dependencies

 * [Node.js](http://nodejs.org/) 6+
 * Python 3.5+

Libraries used:

 * FontAwesome 4.3.0
 * lunr.js - fast full text search within the browser
 * [React.js](https://reactjs.org/) (v0.15)


## Installation

Simply clone the repository, or download it as a zip file.

We recommend running the python scripts using a virtual environment.

1. If not already installed in your system, first install the virtual environment via `pip`:

   `pip install virtualenv`

2. Create a virtual environament:

   `virtualenv venv`
   
3. Then, activate the virtual environment:

  `source venv/bin/activate`if you are using the bash shell or `. venv/bin/activate` if you are using `/bin/sh`
  
  
4. Install the requirements:

  `pip install -r requirements.txt`
 
 or
  
  `pip install --upgrade -r requirements.txt`
  
  if you want to upgrade the requirements already installed.

To download Springer Nature Scientific Data files, run the sdata_crossref_download.py script:

```
python scripts/sdata_crossref_download.py
```

Or to use your own data, place your ISA-Tab files in the Data directory (can also be symlinks).

To build a new index over the files, run the build_index.py script, which will build an initial metadata repository JSON file that is used by lunr.js to search, and by the web application to present the initial file list.:

```
python scripts/build_index.py data
``` 

This will create a file called isatab-index.json which will be read by the application to generate the search interface.

To generate the json-ld with schema.org representation, use:
```
python scripts/schemaorg_conversion.py

```


### For React-based version

To install dependencies:

```
npm install
```

To build the assets locally:

```
npm run build:local
```

(check other builds in package.json)

To run the web server:
```
node server.js
```
