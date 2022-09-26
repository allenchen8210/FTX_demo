# FTX_demo
FTX demo

run command $flask run

## command 1
```
export FLASK_APP=flask_request.py
flask run
```

## command 2
```
python3 flask_request.py
```
* This command need to specify the sys path and use `pip3 install` to install the relevent packages.
```
import sys
sys.path.append('/Users/bur/opt/anaconda3/lib/python3.9/site-packages')
```

## command 3 (Currently Used)
```
python3 flask_request.py --sys_path [path for python3.9 site-packages]
```
* example:
```
python3 flask_request.py --sys_path /Users/bur/opt/anaconda3/lib/python3.9/site-packages
```
* Use command args to input the path.