# DiscoverUni

[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/dev/dev-wagtail-cms?branchName=develop&label=Dev%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=9&branchName=develop)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/pre-prod/pp-wagtail-cms?label=Pre%20prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=11)
[![Build Status](https://dev.azure.com/ofsbeta/discoverUni/_apis/build/status/prod/prod-wagtail-cms?branchName=master&label=Prod%20build%20status)](https://dev.azure.com/ofsbeta/discoverUni/_build/latest?definitionId=12&branchName=master)

# Table of Contents

...

## Tech stack

This application is based on the Wagtail CMS.
It utilises:
- Wagtail CMS
- Python/Django framework
- jQuery
- SASS

## Rollout

### LIVE

The following command will need to be run to make the codebase work in LIVE:

```
$ cp docker-compose.yml.example docker-compose.yml
```

## Environment variables

| Variable                          | Default              | Description                                 |
| --------------------------------- | -------------------- | ------------------------------------------- |
| DBHOST                            | host.docker.internal | DB host url/string                          |
| DBPORT                            | 5432                 | DB connection port                          |
| DBNAME                            | discoveruni          | DB name to use                              |
| DBUSER                            | <username>           | DB user                                     |
| DBPASSWORD                        | <password>           | DB password                                 |
| SEARCHAPIHOST                     | <searchapihost>      | The url endpoint for the search api         |
| DATASETAPIHOST                    | <datasetapihost>     | The url endpoint for the dataset api        |
| WIDGETAPIKEY                      | <widgetaccesskey>    | The access key for the api for the widget   |
| DATASETAPIKEY                     | <datasetaccesskey>   | The access key for the api for the site     |
| FEEDBACK_API_HOST                 | <feedbackapihost>    | The url endpoint for the feedback api       |
| AZURE_ACCOUNT_NAME                | <azureaccountname>   | The name of the account for image storage   |
| AZURE_ACCOUNT_KEY                 | <azureaccountkey>    | The access key to account for image storage |
| AZURE_ACCOUNT                     | <azureaccount>       | The account for image storage               |
| JSONFILES_STORAGE_CONTAINER       | <azurecontainer>     | The container URI for the json files        |
| SENDGRID_API_KEY                  | <sendgridapikey>     | The API key for the e-mail notifications    |
| SENDGRID_FROM_EMAIL               | <sendgridfromemail>  | The e-mail address used for notifications   |
| LOCAL                             | False                | Tells the site to use external API or mocks |

# Getting Started

## First time here?

The docker image for this branch is created differently from the other branches (`python manage.py runserver 0.0.0.0` is now run inside the image, not as a command on the image in the `docker-compose.yml`). This means that the old containers and images for other branches need to be deleted so the new one can be built.

```
$ docker ps --all
CONTAINER ID     IMAGE               COMMAND                  CREATED        STATUS                  PORTS       NAMES
<container_id>   wagtail-cms_web     "python manage.py ru…"   3 days ago     Exited (0) 3 days ago               wagtail-cms_web_1
............     .....               "...................."   ..........     .............           27017/tcp   .................
$ docker rmi -f <container_id>
$ docker images
REPOSITORY                            TAG          IMAGE ID       CREATED         SIZE
wagtail-cms_web                       latest       <image_id>     11 days ago     1.07GB
...............                       latest       ............   3 weeks ago     ......
$ docker rm <image_id>
...
```

This now means when you run `docker-compose up` docker will rebuild the image using the new commands in the `Dcokerfile`, and then build a new container from that

> *REMEMBER:* To run the commands above when switching back to the other branches on the project

## Configure

### Defaults

```
$ cp docker-compose.yml.example docker-compose.yml
$ vim docker-compose.yml
...
DBHOST:               "db"
DBNAME:               "django"
DBUSER:               "docker"
DBPASSWORD:           "docker"
...
DATASETAPIHOST:       "..."
DATASETAPIKEY:        "..."
...
AZURECOSMOSDBURI:     "..."
AZURECOSMOSDBKEY:     "..."
...
MONGODB_HOST:         "mongo"
MONGODB_USERNAME:     "mongodb"
MONGODB_PASSWORD:     "mongodb"
...
# docker-compose up
```

### Secret Key

```
$ python
>>> import random, string
>>> ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)])
'<secret_key>'
>>> exit()
$ vim docker-compose.yml
...
SECRET_KEY: "<secret_key>"
...
```

## Docker

You need to have [Docker](https://docs.docker.com/install/) installed to be able to see changes in the code, run tests and update local data.

```
$ docker-compose up
```

> Make sure to run this command in a separate window so you have somewhere to run other commands from

> This command will download all the required images (Python, PostgreSQL, CosmosDB) and start them for you all preconfigured

## Database (PostgreSQL)

### Creating

```
$ docker container exec -it wagtail-cms_web_1 python manage.py migrate
```

### Populating

```
$ docker container exec -it wagtail-cms_web_1 python manage.py populate_cms --db_host ... --db_name ... --db_user ... --db_password ... --db_port ...
```

> Use the creds for the remote PostgreSQL in the above statement

Want to delete the command from your command history so people can see passwords on your machine?

```
$ history | tail -n 5
100 ...
101 ...
102 ...  # <- You want to delete this one
103 ...
104 ...
$ history -d 103
```

## MongoDB

### Populating

```
$ docker container exec -it wagtail-cms_web_1 python manage.py populate_institutions
$ docker container exec -it wagtail-cms_web_1 python manage.py populate_courses
```

> `populate_courses` will get the courses in `settings.TEST_COURSES` from CosmosDB and put them in MongoDB **(as well as populate the file found in `courses/fixtures/courses.json`)**

### Adding More courses

```
$ vim docker-compose.yml
...
TEST_COURSES = 'U18-LAWLLB,AB35,...'
...
$ vim docker-compose.yml.example
...
TEST_COURSES = 'U18-LAWLLB,AB35,...'
...
$ docker container exec -it wagtail-cms_web_1 python manage.py populate_courses
...
$ git add docker-compose.yml.example
$ git add courses/fixtures/courses.json
$ git commit -m '...'
...
```

## Viewable URLs

You can view the following URLs in the browser

```
$ wget http://localhost:8000/institution-details/<any_institution>/
$ wget http://localhost:8000/admin/  # <- All wagtail pages
$ wget http://localhost:8000/course-details/10007804/U18-LAWLLB/Full-time/
$ wget http://localhost:8000/course-details/10000055/AB35/Full-time/
$ wget http://localhost:8000/course-details/10001850/PBSFND-D_FT/Full-time/
$ wget http://localhost:8000/course-details/10007165/U09FUECW/Full-time/
$ wget http://localhost:8000/course-details/10007767/UMDAHFY/Full-time/
```

# Useful Commands

## Docker

### List images

```
$ docker images
```

From this list you can find the docker images you no longer need. Copy their `IMAGE ID`

### Deleting Images

```
$ docker rm <IMAGE_ID>
```

### Listing Containers

Container are based of images. This is what runs your code

```
$ docker ps --all
```

The `NAME`s you can see in the commands above. The `STATUS` tells you whether ac container is being used. If you no longer need a container copy the `CONTAINER ID`

### Deleting Containers

```
$ docker rmi -f <CONTAINER_ID>
```

### Get into a Container

```
$ docker container exec -it wagtail-cms_web_1 bash
$ docker container exec -it wagtail-cms_db_1 bash
```

### Using the Django Shell

```
$ docker container exec -it wagtail-cms_web_1 python manage.py shell
```

##### Adding new dependencies

```
$ docker container exec -it wagtail-cms_web_1 pip install ...
$ docker container exec -it wagtail-cms_web_1 pip freeze > requirements.txt
```

# Other Stuff

## Adding Environment Variables

If you add environment variable to `docker-compose.yml` don't forget to also add it to `CMS/settings/base.py`

## Continuous Integration and Deployment Pipeline

The continuous integration and deployment pipeline for this project is implemented using Azure DevOps pipelines.

### Continuous Integration

The continuous integration pipeline for the project is defined in yml files in the root of the project, all starting with 'azure-pipelines'.

There are 4 pipelines defined in the project.

#### CI test
_Defined in 'azure-pipelines.yml'_

This pipeline should run on every push to Github from feature, bug and refactor branches. All this pipeline does is run the tests to regression check the new code.

#### Development build
_Defined in 'dev-azure-pipelines.yml'_

This pipeline should run on every push to Github on the develop branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the dev container registry.

#### Pre prod build
_Defined in 'pre-prod-azure-pipelines.yml'_

This pipeline should run on every push to Github from a release branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the pre-prod container registry.

#### Production build

_Defined in 'prod-azure-pipelines.yml'_

This pipeline should run on every push to Github on the master branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the prod container registry.

### Continuous Deployment

The continuous deployment pipeline is defined through the Azure DevOps pipeline UI.

There are 3 pipelines setup for the project.

#### Development deploy

The pipeline runs when the Development CI pipeline passes, it pulls the container generated by the CI build on to the WebApp server and starts the container.

#### Pre prod deploy

The pipeline runs when the a new container is pushed to the pre-prod container registry, it pulls the container on to the WebApp server and starts the container.

#### Production deploy

The pipeline runs when the a new container is pushed to the prod container registry, it pulls the container on to the WebApp server and starts the container.

### Releases

Releases of the code are following the major/minor/patch pattern for release numbering.

#### Creating a release

New releases can be generated manually or by using the 'release' command in the bin directory.

##### Manual release process

- update the version number with in the version.txt file
- create a new branch named in the pattern 'release/v`version number`' (e.g. release/v0.0.1)
- push the branch to Github

##### Automated release process

- ensure there are no uncommitted changes in your local repository
- call the 'release' command in the bin directory, passing as a parameter either major/minor/patch.

#### Finishing a release

Once a release has been signed off and deployed to production, you need to:

- merge the release branch into master and to development.
- tag master with the release number at the point it was merged in.
- delete the release branch

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

## License

See [LICENSE](LICENSE.md) for details.
