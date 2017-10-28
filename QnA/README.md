In order to run helloAlex NLU component 

1) Install conda

`wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh`

2) Create conda environment

`conda create --name helloalex --file requirement.txt`

3) Active the environment

`source activate helloalex`

4) Install spacy model

`python -m spacy download en`

5) Run

`python app.py`
