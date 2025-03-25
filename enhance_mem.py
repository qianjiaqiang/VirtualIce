import mrcfile
import numpy as np
import sys

def run(mem_pro :str, t2: float, t1: float = 0.01 ):
    print(mem_pro)
    origin_protein = mrcfile.open(mem_pro, permissive=True)
    assert len(origin_protein.data.shape) == 3

    data = np.copy(origin_protein.data)
    origin_protein.close()

    membrane_mask = np.where((data > t1) & (data< t2), True, False)
    protein_mask = np.where( data> t2, True ,False)

    membrane = membrane_mask * data
    protein = protein_mask * data

    enhance = np.copy(membrane)

    membrane_mean = membrane[np.nonzero(membrane)].mean()
    protein_mean = protein[np.nonzero(protein)].mean()

    print(membrane_mean)
    print(protein_mean)

    # enhance[np.nonzero(membrane)]+=  (protein_mean + membrane_mean)/2
    enhance[np.nonzero(membrane)]+=  np.sqrt(protein_mean * membrane_mean)
    enhance += protein
    # enhance_pro = mrcfile.new(f"{mem_pro.split('.mrc')[0]}_enhance.mrc")
    enhance_pro = mrcfile.new("emd_enhance.mrc")
    enhance_pro.set_data(enhance)
    enhance_pro.close()

    return 0

if __name__ == "__main__":
    # input normalized mrc (mean = 0.0, std=1.0)
    input_mrc = sys.argv[1]
    # include membrane
    threshold_membrane = float(sys.argv[2])
    # include protein only
    threshold_protein = float(sys.argv[3])
    print(input_mrc, threshold_membrane, threshold_protein)
    run(input_mrc, threshold_protein, threshold_membrane)
