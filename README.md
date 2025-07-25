# Archaeal_lipid_MS2_library
This program is designed to create an in silico MS2 library for lipidomic analysis. 

You can find our ArchLips MS2 library (.msp format) in: https://doi.org/10.5281/zenodo.16040382

To use this library, you can cite: 

ArchLips: A comprehensive in silico database for high-throughput identification of archaeal lipids

https://doi.org/10.1101/2025.05.05.652033

## 1. Prepare your data as the template file shows: Diether-template.xlsm/Tetraether-template.xlsm
- **Statistic Sheet**: 
Save the additional information of the molecules: eg., Formula, inchi, Smile, references. This information will not affect the exportation result.
<div align=center>
<img src="./Figs/fig1.png" style="width: 80%; max-width: 100%;">
</div>

- **Export Controller Sheet**:
This sheet decides which sheets will be exported. The sheet number of the MS2 sheet is recorded in column A (the sheet name can be recorded in column B for clarity). The exportation program reads the maximum and minimum values in column A, and the data sheets in between will be exported.
<div align=center>
<img src="./Figs/fig2.png" style="width: 80%; max-width: 100%;">
</div>

- **Data Sheets**:
### Each lipid class should be stored in a unique datasheet. The format should follow these rules:
- The first 5 rows record the general information of this molecule and the sheet. and the 6th row records the title of the column
- Start from the 7th row, each row records an individual molecule to be exported.
- The first 28 columns (A to AB) represent the general information of the molecules and the structural information to be exported.
- The peak information (X peaks) of the molecules’ MS2 is saved in the following peak columns. Columns from 29 to 28+X record the m/z value of the peak, and columns from 29+X to 28+2*X record the peak height. In one datasheet, all molecules should have the same peak columns. A 0 value can be used and will be ignored during the exportation.
<div align=center>
<img src="./Figs/fig3.png" style="width: 90%; max-width: 100%;">
</div>

## 2. Install package dependencies
- This program is up-to-date to work with Python 3.12
- tqdm (https://github.com/tqdm/tqdm）
- openpyxl (https://openpyxl.readthedocs.io/)
```
pip install tqdm
pip install openpyxl
```
## 3. Export the library
Save your data file in the folder: **Files_for_construction**.
Then you can export the library by running the **PoolExport.py** script with the default setting. The exported .msp library files can be found in **Exported_msp** folder.
```
python PoolExport.py
```
### Parameters for **PoolExport.py**

- **--folder_path**: Specify the directory of the .xlsm data files.
- **--include_path**: "1" only read the datafile in folder_path. "2" also read the datafile in the subfolders of the folder_path (default: 2).
- **--export_path**: Specify the directory of the exportated files.
- **--standardization**: "True": Standardize the MS2 in the MSP library, unify the maximum peak, remove replicate peaks, and remove low peaks. "False": Do not standardize the MS2.
- **--max_peak**: Maximum peak height after standardization (default: 1000).
- **--min_peak**: Peak height below will be filtered (default: 0.1).
- **--merge_at_end**: "True": Combine all exported .msp files into one .msp file. "False": Do not combine files (default: False).
- **--merge_while_processing** (More efficient than **merge_at_end** method, but the result file will not in the original order): True: Combine files while exporting files (default: True). 
- **--delete_intermediate**: "True": Delete intermediate files (default: False).
- **--threads**: Threads number used in this exportation. Use "0" for the maximum threads (default: 0).

## The following scripts can be modified for specific purpose:

### **SingleExport.py** controls the exportation of a single data file.
- **import_adduct()**: Specify the adduct ion of the library to be exported.
<div align=center>
<img src="./Figs/fig5.png" style="width: 90%; max-width: 100%;">
</div>

- **single_msp_export()**: Lines 49-62 specify the structural information in the data file to be exported.
<div align=center>
<img src="./Figs/fig6.png" style="width: 90%; max-width: 100%;">
</div>

## Citation and acknowledgement:
This program is inspired and modified from Lipidblast. https://fiehnlab.ucdavis.edu/projects/LipidBlast

