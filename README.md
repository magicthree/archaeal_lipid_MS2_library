# archaeal_lipid_MS2_library
## 1. Prepare your data as the template file shows: Diether-template.xlsm/Tetraether-template.xlsm
- **Statistic Sheet**: 
Save the additional information of the molecules: eg., Formula, inchi, Smile, references. This information will not affect the exportation result.
- **Export Controller Sheet**:
This sheet decides which sheets will be exported. In column A, the sheet number of the MS2 sheet is recorded (the sheet name can be recorded in column B for clarify). The exportation program reads the maximum and minimum value in column A, and the data sheets in between will be exported.
- **Data Sheets**:
### Each lipid class should be stored in a unique data sheet. The format should follow these rules:
- The first 5 rows record the general information of this molecule and the sheet. and the 6th row records the title of the column
- Start from the 7th row, each row records an individual molecule to be exported.
- The first 28 columns (A to AB) represent the general information of the molecules and the structural information to be exported.
- The peak information (X peaks) of the molecules’ MS2 is saved in the following peak columns. Columns from 29 to 28+X record the m/z value of the peak, and columns from 29+X to 28+2*X record the peak height of the peak. In one data sheet, all molecules should have the same number of the peak columns. A 0 value can be used and will be ignored during the exportation.
## 2. Install package dependencies

## 3. Export the library
Save your data file in the folder: **Files_for_construction**.
Then you can export the library by running the **PoolExport.py** script with the default setting. The exported .msp library files can be found in **Exported_msp** folder.
You can edit the following scripts to modify the parameters for exportation.
### **PoolExport.py** controls the overall parameters during the exportation.
- **folder_path**: Specify the directory of the .xlsm data files.
- **include_path**: "1" only read the datafile in folder_path. "2" also read the datafile in the subfolders of the folder_path.
- **export_path**: Specify the directory of the exportated files.
- **fix_file**: "True": Standardize the MS2 in MSP library, unify the maximum peak, remove replicate peaks, and remove low peaks. "False": Do not standardize the MS2.
- **merge_at_end**: "True": Combine all the exported files into one file. "False": Do not combine files.
- **merge_while_processing** (More efficient than **merge_at_end** method, but the result file will not in the original order): True: Combine files while exporting files. 
False: Do not combine files while exporting.
- **threads**: Threads number used in this exportation. Use "0" for the maximun threads.
### **SingleExport.py** controls the exportation of a single data file.
- **importadduct()**: Specify the the adduct ion of library to be exported.
- **single_msp_export()**: Line 49-62 specify the structural information in data file to be exported.
### **MSPfix.py** controls the standardization of the MS2 in MSP library.
- **peak_cal()**: all peaks will be linearly transformed, and the maximum peak abundance will be set as max_peak parameter. After the transformation, peak abundance lower than min_peak will be removed.


