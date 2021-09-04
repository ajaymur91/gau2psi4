import pymatgen.io.gaussian
gau=pymatgen.io.gaussian.GaussianInput.from_file('1.com')

#>>>gau.basis_set
#'DEF2TZVP'
#>>> gau.charge
#-1
#>>> gau.spin_multiplicity
#1
#>>> gau.functional
#'PBEPBE'

mol=pymatgen.core.Molecule(gau.molecule.species,gau.molecule.cart_coords)
import pymatgen.io.xyz
xyz=pymatgen.io.xyz.XYZ(mol)
xyz.write_file("gau.xyz")

#########################
# function to read xyz to psi4
def readXYZ(file):
    f = open(file, "r")
    lines = f.readlines()
    filelength = len(lines)
    progress = 0
    geomcount = 0
    geom = []
    while progress < filelength:
        tmpgeom = ""
        length = int(lines[progress])+2
        rangestart = progress
        rangeend = progress + length
        for i in range(rangestart, rangeend):
            tmpgeom = tmpgeom + lines[i]
        geom = geom + [tmpgeom]
        geomcount = geomcount + 1
        progress = progress + length
    f.close()
    return(''.join((geom)))
########################
import psi4
geom = readXYZ("gau.xyz")
psi4geom = psi4.geometry(geom)
psi4.set_memory('2048 MB')
psi4.set_num_threads(12)
psi4.set_options({'basis':'def2-TZVP'})
psi4.set_options({'pcm': 'true'})

pcm_string = """
       Units = Angstrom
       Medium {
       SolverType = IEFPCM
       Solvent = Water
       }
       Cavity {
       RadiiSet = UFF
       Type = GePol
       Scaling = TRUE
       Area = 0.3
       Mode = Implicit
       }
    """
psi4.pcm_helper(pcm_string)

psi4geom.set_molecular_charge(gau.charge)
psi4geom.set_multiplicity(gau.spin_multiplicity)
#>>> psi4geom.print_out()
#    Molecular point group: c1
#    Full point group: C1
#
#    Geometry (in Angstrom), charge = -1, multiplicity = 1:
#
#       Center              X                  Y                   Z               Mass       
#    ------------   -----------------  -----------------  -----------------  -----------------
#         O            2.124699950718     0.338999784934    -1.173084208680    15.994914619570
#         H            1.161303950718     0.373503784934    -0.675366208680     1.007825032230
#         H            2.024503950718    -0.481893215066    -1.745103208680     1.007825032230
#         O           -0.268357049282     0.393846784934    -0.203808208680    15.994914619570
#         H           -0.479650049282     1.286070784934    -0.275282208680     1.007825032230
#         H           -1.219183049282    -0.204284215066     0.663821791320     1.007825032230
#         O           -1.836537049282    -0.690838215066     1.420821791320    15.994914619570
#         H           -1.801308049282    -1.640100215066     1.334738791320     1.007825032230

psi4.set_options({'basis': 'def2-TZVP',
                   'scf_type': 'pk',
                   'pcm_scf_type': 'total',
                   'e_convergence': 1e-8,
                   'd_convergence': 1e-8})
e=psi4.energy('pbe')
print(e)
#################################
