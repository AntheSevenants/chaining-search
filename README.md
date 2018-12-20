# Create virtual environment for chaining search, in which local copies of all Python dependencies will be installed
Install venv for python3, eg. on Ubuntu:
$ sudo apt install python3-venv
Create and activate virtual environment:
$ python3 -m venv cs_env
$ source cs_env/bin/activate
Install dependencies inside virtual environment
(venv) $ pip install ipykernel
(venv) $ ipython kernel install --user --name=cs_env
pip3 install -r requirements.txt
