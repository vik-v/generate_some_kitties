# gensk
#### Script to generate kitties  😺
## Features
- Generate kitties in JSON format
- Check server status
- Deploy to server via `POST` method using API
- Clean database via `DELETE` method using API

gensk is a script to help you full database with learning purposes.

## Requirements
gensk tested with next requiremetns, and it works

| Pakage | Version |
| ------ | ------ |
| requests | 2.28.2 |
| webcolors | 1.12 |

## Installing
### For linux system or WSL
Get source
```sh
git clone git@github.com:vik-v/generate_some_kitties.git
```
Make virtual environment
```sh
cd generate_some_kitties
python3 -m venv venv
source venv/bin/activate
```
Install pip and dependencies
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### For MacOS
...
### For Windows
...

## Usage
### Help
Please, fill free to use [`-h` | `--help`]
```sh
usage: python3 gensk.py [-h] [-v [VERBOSITY]] [-s {http,https}] [-a [ADDRESS]] [-p [PORT]] [-r [RESOURCE]] [-u [URL]] [-g] [-l [{0,1,2,3}]] [-n [NUMBER_OF_CATS]] [-c | -d | -e]

Script for generate and deploy kitties data via API

options:
  -h, --help            show this help message and exit
  -v [VERBOSITY], --verbosity [VERBOSITY]
                        Set verbosity level for logging (default: 1)

URL configuration:
  -s {http,https}, --schema {http,https}
                        Select schema to use. (default: http)
  -a [ADDRESS], --address [ADDRESS]
                        Specify address. (default: 127.0.0.1)
  -p [PORT], --port [PORT]
                        Specify port number. (default: 8000)
  -r [RESOURCE], --resource [RESOURCE]
                        Specify API resource of endpoint. (default: cats/)
  -u [URL], --url [URL]
                        Fully specified URL to API. (default: )

Generating kitties:
  -g, --generate        Generate kitties and print in stdout. (default: False)
  -l [{0,1,2,3}], --lesson-number [{0,1,2,3}]
                        0: `Урок 5/15` 1: `Урок 9/15`2: `Урок 10/15` 3: `Урок 12/15`. (default: 0)
  -n [NUMBER_OF_CATS], --number-of-cats [NUMBER_OF_CATS]
                        Number of kitties to generate. (default: 10)

API actions:
  -c, --check-server    Basic check for endpoint availability. (default: False)
  -d, --deploy          Deploy generated data via `POST` method. (default: False)
  -e, --cleanup-db      Delete all entries in database via `DELETE` method. (default: False)
```

### Generating
To generate kitties you may use [`-g` | `--generate`]
```sh
python3 gensk.py -g
```
By default it's generate 10 entries:
```json
[
    {
        "name": "Инки",
        "color": "Black",
        "birth_year": 2018
    },
    ...
    {
        "name": "Бруно",
        "color": "Gray",
        "birth_year": 2011
    },
    {
        "name": "Дилан",
        "color": "Black",
        "birth_year": 2019
    },
]
```
Also, you can specify number of kitties to generate by using [`-n` |  `--number-of-cats`]
```sh
python3 gensk.py -g -n 1000
```
It will generate one thousand of kitties. What a pretty result!

#### Check server response
Checking url availability [`-c` |  `--check-server`]
```sh
python3 gensk.py -c
```
By default it check: http://127.0.0.1:8000/cats/

### Deploy data
To deploy data use [`-d` | `--deploy`], as for generator you can specify number of kitties by using [`-n` |  `--number-of-cats`]
```sh
python3 gensk.py -d -n 5
```
It will generate five kitties and rocket launch them to server.

### Cleanup database
From the bottom of my heart i’ll had to say, that if you decide to genocide fluffy kitties, you may use [`-x` | `--cleanup-db`]
```sh
python3 gensk.py -x
```
It will totaly remove all kitties from you server. Burn in Hell, scratchy basters!!

### Specifying custom URL or URL part
For [`-c` | `--check-server`], [`-d` | `--deploy`], [`-x` | `--cleanup-db`] you may specify:
| Option | Default value |
| ------ | ------ |
|[`-s` \| `--schema`]|`http`|
|[`-a` \| `--address`]| `127.0.0.1`|
|[`-p` \| `--port`]| `8000`|
|[`-r` \| `--resource`]|`cats/`|
```sh
python3 gensk.py -d -n 5 -p 8080 -r api/v1/cats/
python3 gensk.py -c -p 8080
python3 gensk.py -x -a localhost
```
To specify fully URL, use [`-u` | `--url`]
```sh
python3 gensk.py -d -n 5 -u http://scratchy-baster9000.pythonanywhere.com/cats/
```
## License

MIT
**Free Software, Hell Yeah!**
