####### Datasets
1. BCRP dataset
The dataset containing 1238 compounds with IC50 values and structure information
2. Approved drugs
The dataset of approved drugs containing 4324 compounds derived from KEGG drug (https://www.genome.jp/kegg/drug/drug_ja.html)

####### Prediction for BCRP inhibition 
#Create the environment
conda env create -n pred_bcrp -f environment.yml

#How to get the predicted pIC50 in BCRP with the final simplified model
The column name of compound_id and smiles should be indicated as "name" and "smiles" at config.json
Execute like "python main.py {data} {config.json}"
Example: python /place/of/main.py /place/of/dataset.csv /place/of/config.json (Use absolute path)
The predicted pIC50 values are placed in the output folder.

#Test run with bcrp dataset
python /place/of/main.py /place/of/data_bcrp_part.csv /place/of/config_sample_bcrp_part.json
The output results for a verification is in the output_examples folder.

#Test run with external test set
python /place/of/main.py /place/of/data_externaltest.csv /place/of/config_sample_extest.json
The output results for a verification is in the output_examples folder.

####### Predicted results on approved drugs
Predicted_pIC50_Top100.csv
