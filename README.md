EditData
==============

Getting Started
---------------

- Activate the Climmob environment.
```
$ . ./path/to/ClimmobEnv/bin/activate
```

- Change directory into your newly created plugin.
```
$ cd EditData
```

- Build the plugin
```
$ python setup.py develop
```

- Add the plugin to the climmob list of plugins by editing the following line in development.ini or production.ini
```
    #climmob.plugins = examplePlugin
    climmob.plugins = EditData
```

- Run Climmob again
