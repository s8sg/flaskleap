# Flask RESTful Application Code Generator

## Overview

Generates Flask Service blueprint code from a Swagger Specification doc based on CDNetworks P3 project  specification

**This project is diecly modified on:** `github.com/guokr/swagger-py-codegen`  
  
**How its different:**  
  
Flask Code Gen is completly based on requirments for p3 services. It Automates:  
**1>** Module Creation (flask blueprint) and grouping of API's    
**2>** Abstract API views to support easier API changes  
**3>** Python Project setup (setuptools, tox, pycov, flake8, pydoc integration)  
**4>** Build, Test, Release automation Script  
**5>** Dockerfile with Cherrypi as a wsgi server  
**6>** Swagger UI and Definition creation  

## Install

```
pip install flask-codegen
```

## Usage

Create all:

```
flask-codegen --swagger-doc api.yml example
```

Command Options:

    -s, --swagger, --swagger-doc        Swagger doc file.  [required]
    -f, --force                         Force overwrite of all the Generated file.
    -g, --group-factor                  Group info a module based given no of occurance of same API path
    -t, --template-dir                  Path of your custom templates directory.
    --help                              Show this message and exit.

## Examples:

Generate example service from **api.yml**:

    $tree
	.
	|__ api.yml

    //  Group factor value 1 indicates that more than one same 
    //  api pattern will create a module
    $ flask-codegen -s api.yml -g 1 example
    $ tree
	.
	|__ api.yml
	|__ example
		├── Dockerfile
		├── MANIFEST.in
		├── Makefile
		├── README.md
		├── config
		│   └── config.py
		├── docker-entrypoint.sh
		├── example
		│   ├── __init__.py
		│   ├── __main__.py
		│   ├── app.py
		│   ├── blueprints.py (R)
		│   ├── common
		│   │   ├── __init__.py
		│   │   └── utils.py
		│   ├── config
		│   │   ├── __init__.py
		│   │   └── config.py
		│   ├── hello
		│   │   ├── __init__.py
		│   │   ├── models.py
		│   │   ├── resources.py (R)
		│   │   ├── routes.py (R)
		│   │   └── views.py
		│   ├── resources.py (R)
		│   ├── routes.py (R)
		│   ├── run.py
		│   ├── schemas.py (R)
		│   ├── swagger.json (R)
		│   └── views.py
		├── requirements.txt
		├── server.py
		├── setup.cfg
		├── setup.py
		├── swagger.yaml (R)(S)
		├── test
		│   ├── __init__.py
		│   └── test.py
		├── tox.ini
		└── wsgi.py
	    
    (R) File that would be Regenerated for changes in swagger
        For the best practice user should not change the Regenerated Files
    (S) Swagger definition file for the Service
        This file would be used by the CI/CD for the service definition


Install Example Service:

    $ cd example
    $ make install

Start Example Service:

    $ python server.py

Create and Run Docker image of Example Service:
  
    $ make install-docker
    $ docker run docker run -p 8080:8080 p3/example


Service Swagger Ui from apis.yml:

Then you can visit http://127.0.0.1:8080/apidocs in a browser.
