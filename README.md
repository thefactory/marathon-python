# marathon-python

This is a Python library for interfacing with [Marathon](https://github.com/mesosphere/marathon) servers via Marathon's [REST API](https://github.com/mesosphere/marathon/blob/master/REST.md).

#### Compatibility

* marathon-python has been tested with Marathon 0.5.1 ([REST API version 2](https://github.com/mesosphere/marathon/blob/marathon-0.5.1/REST.md))

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
>>> c.create_app(id='myapp3', cmd='sleep 100', mem=16, cpus=1)
True
```

```python
>>> app = c.get_app('myapp3')
>>> app.ports
[19671]
>>> c.update_app('myapp3', app, mem=32)
True
>>> c.get_app('myapp3').mem
32.0
```

```python
>>> c.get_app('myapp3').instances
1
>>> c.scale_app('myapp3', 2)
True
>>> c.get_app('myapp3').instances
3
>>> c.scale_app('myapp3', delta=-1)
True
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

## License

Open source under the MIT License. See [LICENSE](LICENSE).
