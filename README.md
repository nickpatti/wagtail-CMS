# uniSimple

<!-- vim-markdown-toc GitLab -->

* [Purpose of this app](#purpose-of-this-app)
* [About this application](#about-this-application)
* [Getting Started](#getting-started)
  * [Running the development server](#running-the-development-server)
  * [Adding new dependencies](#adding-new-dependencies)

<!-- vim-markdown-toc -->


## Purpose of this app


The purpose of this app is to provide a user interface for admin users to maintain the 'uniSimple' site.


## About this application


This application is based on the Wagtail CMS.

## Getting Started


### Running the site

As a prerequisite to running the site you need to have Python (3.6.8) and PIP installed. There are multiple ways to install Python, either download from the official [Python site](https://www.python.org/downloads/) or use the package manager [Homebrew](https://brew.sh/). PIP comes installed with Python 3.4(or greater) by default

You have two options to run the development server:

**1.** In a virtual environment of your choice run the following from the root directory of the project:

```
source ./env.sh
pip install -r requirements.txt
./manage.py runserver

```

**2.** from the root directory run:

This options requires you to have [Docker](https://docs.docker.com/v17.12/docker-for-mac/install/) installed in order to run the site in a Docker container

```
docker build -t wagtailcms .
docker run -p 8000:8000 wagtailcms

```

For either option:

The first command builds the docker image.
The second command starts the docker container, running on port 8000.


### Adding new dependencies

Adding a new dependency requires rebuilding docker image for Django app if you are working with Docker. After installing dependency with `pip install <dependency>` run following to update requirements.txt

```
pip freeze > requirements.txt
```

Stop docker container

```
docker stop [CONTAINER]
```

Rebuild Docker image

```
docker build -t wagtailcms .
```

Start server again

```
docker run -p 8000:8000 wagtailcms

```

## Environment variables

| Variable        | Default       | Description                       |
| --------------- | :-----------: | --------------------------        |    
| DBHOST         | unistatsdb.postgres.database.azure.com            | DB host url/string                |
| DBPORT         | 5432          | DB connection port                |
| DBNAME         | unistatsdevdb        | db name to use                    |
| DBUSER         | unistatsmanager@unistatsdb           | DB user                           |
| DBPASSWORD     | 8f555f62-6009-4a77-a1aa-75658ac2bc1a              | DB password                       |


### Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

### License

See [LICENSE](LICENSE.md) for details.
