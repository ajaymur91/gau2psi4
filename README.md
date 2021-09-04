conda create -n genome


conda activate genome


conda install -c conda-forge pymatgen


conda install -c psi4 -c conda-forge psi4

######
python calc_SP.py  (PCM cavity scaling set to 1.2 by default)

Total Energy =                       -228.6691155252857186
######

G16 ref value (PCM Cavity scaling = 1.1)

 SCF Done:  E(RPBE-PBE) =  -228.676514333


G16 ref value (PCM Cavity scaling = 1.2)

 SCF Done:  E(RPBE-PBE) =  -228.668943875
