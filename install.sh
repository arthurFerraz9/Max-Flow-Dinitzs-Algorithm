conda remove --name Dinitzs --all

conda env create -f requirements.yml

conda install -c anaconda ipykernel
python -m ipykernel install --user --name=Dinitzs

conda activate Dinitzs
