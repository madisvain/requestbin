[![CircleCI](https://circleci.com/gh/madisvain/requestbin.svg?style=svg)](https://circleci.com/gh/madisvain/requestbin)

# RequestBin
RequestBin is a free service for inspecting HTTP Requests.

RequestBin gives you a URL that will collect requests made to it and let you inspect them in a human-friendly way.
You can use RequestBin to see what your HTTP client is sending or to inspect and debug webhook requests.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/madisvain/requestbin)

## Stack
RequestBin is built upon Sanic to achieve high throughput. The current setup can asyncronously handle thousands of requests per second.

#### Libraries used
* [Sanic](https://github.com/channelcat/sanic)
* [asyncpg](https://github.com/MagicStack/asyncpg)
* [uvloop](https://github.com/MagicStack/uvloop)
* [ultraJSON](https://github.com/esnme/ultrajson)
* [React.js](https://reactjs.org/)
* [antD](https://ant.design/)

## API documentation
...

## Development
#### Virtualenv
```shell
pipenv shell
```
#### Install packages
```shell
pipenv install
```
#### Run development server
```shell
gunicorn requestbin.app:app --worker-class sanic.worker.GunicornWorker --reload
```

## Contributing
Thanks for your interest in the project! All pull requests are welcome from developers of all skill levels. To get started, simply fork the master branch on GitHub to your personal account and then clone the fork into your development environment.

Jeff Lindsay (progrium on Github, Twitter) is the original creator of the RequestBin framework.
Madis Väin (madisvain on Github, Twitter) is the creator of this RequestBin framework and service.

## License
MIT