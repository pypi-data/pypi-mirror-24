# Systran Translation Client

[![pipeline status](https://gitlab.com/canarduck/systranio/badges/master/pipeline.svg)](https://gitlab.com/canarduck/systranio/commits/master) [![coverage report](https://gitlab.com/canarduck/systranio/badges/master/coverage.svg)](https://gitlab.com/canarduck/systranio/commits/master)

An unofficial python client to Systran.io APIs, [official libraries](https://github.com/SYSTRAN/translation-api-python-client) are also available.
I am *not* affiliated with Systran *at all*.

## Setup & Installation

*TODO*

```
pip install systranio
```

Register & get an API key on [systran.io](https://platform.systran.net)

## APIs

### Translation

*Status* : WIP
*Reference* : [Translation API](https://platform.systran.net/reference/translation)
*Calls* :

* [x] Translate text
* [ ] Translate file
* [ ] Get translation status
* [ ] Cancel translation
* [ ] Get translation result
* [ ] Create batch
* [ ] Get batch status
* [ ] Cancel batch
* [ ] Close batch
* [x] Supported languages
* [ ] Supported formats
* [x] Get API version
* [x] List profiles 

*Usage* :

```
import systranio

translation = systranio.Translation(API_KEY)
options = {'source': 'en' } 
result = translation.text('translation', 'fr', **options)
print(result)  # traduction
```

### Natural Language Processing

Status : _not implemented_

### Ressource Management

Status : _not implemented_

### Multimodal Text Extraction

Status : _not implemented_

## Development

### Requirements

```
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

### Workflow

[post-commit](post-commit) & [pre-commit](pre-commit) hooks are available to automate an update of the [CHANGELOG.md](CHANGELOG.md) after a commit.
`cp *-commit .git/hooks/` to activate them.

[bumpversion](https://github.com/peritus/bumpversion) automates the version number update in [setup.py](setup.py) and a git tag creation
Usage : `bumpversion major|minor|patch` (respectively increments version number x.y.z)

Tests are launched on a `git push` by gitlab-ci (see [.gitlab-ci.yml](.gitlab-ci.yml)), an environnemental variable called `SYSTRANIO_KEY` containing
your API key is required.

Successful tag builds are uploaded to [pypi](https://pypi.python.org/pypi/systranio) by gitlab-ci, 2 environnemental variables are required `PYPI_USER` & `PYPI_PASSWORD`

TODO:
* automate docs generation after a successful build
