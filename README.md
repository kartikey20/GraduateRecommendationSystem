# U11 Graduate University Recommendation System

U11 is a recommendation system for Graduate Schools, targetted towards international students applying to colleges in the United States. The application is a HTML site, with a Flask python backend system. 

**Work by:** Anirban Chatterjee, Ravish Chawla, Tanmay Rajpurohit, Yanchao Feng, Yannick Schröcker

### Codebase Structure
The codebase is structured as follows:
* data/
  * maindata.tsv - main dataset used for classification/training
  * trained_models - trained models built by SVM learner
* raw-data/ - raw data from scraper
* scraper/ - scraper and cleaning python scripts
  * scraper.py - scraper for website 1point3acres.com
  * cleaning/
    * json_to.tsv.py - convert json data to a tsv file
    * transform_scores.py - split GRE/TOEFEL grades based on distribution
    * merge_scores.py - fill GPA scores for missing records by user
    * split_university.py - split rows with multiple universities
    * fix_unicode.py - fix unicode values lost by openrefine
* site/ - main website
  * index.html - main HTML website
  * script.js - JS script to control site
  * styles.css - CSS stylings for site
  * app.py - FLASK api
  * create_list.py - classifies data onto training models
  * training/ - model building/training
    * classification.py - script that builds training models
* images/ - images of the application

### Application Dependencies
The following python libraries are required for the application to run properly:
* Python (version 3)
  * flask
  * flask-cors
  * pandas
  * numpy
  * scipy
  * sklearn

All of these can be installed using `pip`. 

### Setup Instructions
The application runs with a Backend and the Frontend. Having the above dependencies installed, start the backend service as follows:

    cd site/
    python app.py

This will start the python API server on `http://localhost:5000`

Start a new service (while keeping the above service running):

    cd site/
    python -m http.server

The application can be viewed in a browser window, on `http://localhost:8000`
