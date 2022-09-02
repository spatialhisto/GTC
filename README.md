# GTC
Genes To Count

[![Python version](https://img.shields.io/badge/python-v3.8-brightgreen)](https://www.python.org/)
[![Python version](https://img.shields.io/badge/docs-pds-yellow)](https://github.com/spatialhisto/GTC/blob/main/_docs_/Documentation.pdf)
[![Python version](https://img.shields.io/badge/checks-passing-brightgreen)](https://github.com/spatialhisto/GTC/)

#### Description

<img src="https://github.com/spatialhisto/GTC/blob/main/_docs_/_etc_/gtc_logo.png?raw=true" width="150" title="GTC" alt="cellpose" align="right" vspace="50">

The program derives compartments for neoplastic and non-neplastic tissue based on the transcripts of selected *in situ* sequencing genes.
The compartments are then compared to the ones classified by a pathologist specialist in colorectal cancer.
Afterwards, the algorithm counts the number of transcripts for all genes in the various compartments and highlights the significant genes via a vulcano plot.

For a detailed description please refer to our [paper](https://github.com/spatialhisto/GTC/blob/main/_docs_/Documentation.pdf) and the provided [documentation](https://github.com/spatialhisto/GTC/blob/main/_docs_/Documentation.pdf) file.

#### Installation

```bash
git clone https://github.com/spatialhisto/GTC.git
```

#### Run analysis

```bash
python3 gtc_main.py
```

#### Example data

Two [example cases](https://github.com/spatialhisto/GTC/blob/main/data/) are provided to highlight the formatting of the data.
