# marathon-python

This is a Python library for interfacing with [Marathon](https://github.com/mesosphere/marathon) servers via Marathon's [REST API](https://github.com/mesosphere/marathon/blob/master/REST.md).

#### Compatibility

* marathon-python is currently developed against Marathon 0.7.0-RC3 (see [Marathon docs](https://mesosphere.github.io/marathon/docs/rest-api.html))

## Installation

#### From PyPi (recommended)
```bash
pip install marathon
```

#### From GitHub
```bash
pip install -e git+git@github.com:thefactory/marathon-python.git#egg=marathon
```

#### From source
```bash
git clone git@github.com:thefactory/marathon-python
python marathon-python/setup.py install
```

## Documentation

API documentation is [here](http://thefactory.github.io/marathon-python).

Or you can build the documentation yourself:
```bash
pip install sphinx
pip install sphinx_rtd_theme
cd docs/
make html
```

The documentation will be in `<project-root>/gh-pages/html`:
```bash
open gh-pages/html/index.html
```

## Basic Usage

Create a `MarathonClient()` instance pointing at your Marathon server:
```python
>>> from marathon import MarathonClient
>>> c = MarathonClient("http://localhost:8080")
```

Then try calling some methods:
```python
>>> c.list_apps()
[MarathonApp::myapp1, MarathonApp::myapp2]
```

```python
>>> from marathon.models import MarathonApp
>>> c.create_app('myapp3', MarathonApp(cmd='sleep 100', mem=16, cpus=1))
MarathonApp::myapp3
```

```python
>>> app = c.get_app('myapp3')
>>> app.ports
[19671]
>>> app.mem = 32
>>> c.update_app('myapp3', app)
{'deploymentId': '83b215a6-4e26-4e44-9333-5c385eda6438', 'version': '2014-08-26T07:37:50.462Z'}
>>> c.get_app('myapp3').mem
32.0
```

```python
>>> c.get_app('myapp3').instances
1
>>> c.scale_app('myapp3', 2)
{'deploymentId': '611b89e3-99f2-4d8a-afe1-ec0b83fdbb88', 'version': '2014-08-26T07:40:20.121Z'}
>>> c.get_app('myapp3').instances
3
>>> c.scale_app('myapp3', delta=-1)
{'deploymentId': '1081a99c-55e8-4404-907b-4a3697059848', 'version': '2014-08-26T07:43:30.232Z'}
>>> c.get_app('myapp3').instances
2
```

```python
>>> c.list_tasks('myapp1')
[MarathonTask:myapp1-1398201790254]
>>> c.kill_tasks('myapp1', scale=True)
[MarathonTask:myapp1-1398201790254]
>>> c.list_tasks('myapp1')
[]
```

## License

Open source under the MIT License. See [LICENSE](LICENSE).
