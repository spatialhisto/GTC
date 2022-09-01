# GTC
Genes To Count

The algorithm derives compartments for neoplastic and
non-neplastic tissue based on selected in situ sequencing 
genes and compares the results to the tissue compartments 
classified by a pathologist specialist in colorectal cancer.
Afterwards, the algorithm counts the number of transcripts
in the compartments and calculates a vulcano plot.

Python v3.8

Main used Python packages:
* matplotlib=3.4.3
* numpy=1.21.2
* opencv=4.0.1
* pandas=1.3.3


For a complete overview see file:
environment.yml


Project structure:
# -gtc
# -data
#  |-pathways.csv
#  |-SAMPLE_FOLDER_A/
#  | |-Gtc_Parameters_1A.txt
#  | |-Gtc_Parameters_2A.txt
#  | |-Data/
#  |-SAMPLE_FOLDER_B/
#  | |-Gtc_Parameters_1B.txt
#  | |-Gtc_Parameters_2B.txt
#  | |-Data/
#  |-etc.
#
