# Analysis of connection matrices
- distribution of values
- cohort analysis
- dashboard


## Install
Set up a virtual environment and Jupyter kernel
```
conda create --name=brain python=3.10
conda activate brain
conda install -c anaconda pip

pip install ipykernel
ipython kernel install  --user --name "brain"
```

Install libraries
```
pip install -r requirements.txt
```


## Dataset
[Brain/MINDS Marmoset Brain MRI Dataset NA216 (In Vivo) and eNA91 (Ex Vivo)](https://dataportal.brainminds.jp/marmoset-mri-na216)

Download and extract files
```
bash setup_data.sh
```


## Dashboard
```
streamlit run app.py
```