conda create -n genome
conda activate genome
conda install -c conda-forge pymatgen
conda install -c psi4 -c conda-forge psi4

python calc_SP.py
