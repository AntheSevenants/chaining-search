

echo Install the Python package manager

python -m pip install -U pip



echo Create the virtual environment

pip install --user virtualenv

virtualenv env



echo Activate the virtual environment

call .\env\Scripts\activate.bat


echo Install dependencies

pip install ipykernel
ipython kernel install --user --name=env
pip install -r requirements.txt
pip uninstall -y tornado
pip install tornado==5.1.1
jupyter contrib nbextension install --sys-prefix
jupyter nbextensions_configurator enable --sys-prefix
jupyter nbextension enable collapsible_headings/main
python -m ipykernel install --user --name env


rem fix for temporary issue:
rem https://github.com/jupyter/notebook/issues/4467
pip uninstall notebook
pip install notebook==5.7.5


echo Compile documentation

call .\doc\make html


echo Done. Type 'run' to start your jupyter notebook
