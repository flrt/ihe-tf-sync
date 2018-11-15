Synchronize IHE documents
=========================

This basic tool allows you to keep all the up-to-date documents, available on the IHE.net website
The documents are downloaded and stored locally thanks to there name.

The starting point is the root directory (`documents` by default).
Then subdirectories will be created to store documents by domains.

The domains can be specified, with the `--domain` argument.

To get all documents from two domains : ITI and CARD, simplify run

'''
python sync.py --domain ITI,CARD
'''

The directory will updated to be something like this : 

'''
documents
├── CARD
│   ├── IHE_CARD_Suppl_CIRC_Rev1-1_TI-2011-07-01.pdf
│   ├── IHE_CARD_Suppl_CRC.pdf
│   ├── .../...
│   └── IHE_Card_Suppl_CPN.pdf
└── ITI
    ├── IHE_ITI_Handbook_De-Identification_Rev1.1_2014-06-06.pdf
    ├── IHE_ITI_Handbook_Metadata.pdf
    ├── .../...
    ├── IHE_ITI_Suppl_NPFSm.pdf
    ├── IHE_ITI_Suppl_PDQm.pdf
    ├── IHE_ITI_Suppl_PIXm.pdf
    ├── .../...
    ├── IHE_ITI_TF_Vol1.pdf
    ├── IHE_ITI_TF_Vol2a.pdf
    ├── IHE_ITI_TF_Vol2b.pdf
    ├── IHE_ITI_TF_Vol2x.pdf
    ├── IHE_ITI_TF_Vol3.pdf
    ├── IHE_ITI_TF_Vol4.pdf
    ├── .../...
    └── IHE_ITI_Whitepaper_Security_Cookbook_2008-11-10.pdf

2 directories, 58 files
'''

# Run without docker
Clone these repo and run the `sync.py` program.

'''
# python sync.py --help

usage: sync.py [-h] [--output OUTPUT] [--domain DOMAIN]

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  output directory in wich the documents will be downloaded
  --domain DOMAIN  specify domain(s)

'''

# Run with docker
Just one line to get your documents. Mount your local directory et call the program.
Mount the local directory with the `-v` paramater : `$PWD` for the current directory to `/opt/data`.
Call `python sync.py` with or without parameters.

'''
# mkdir ihe_docs
# cd ihe_docs
# docker run -ti --rm -v $PWD:/opt/data ihe-tf-sync:1.0 python sync.py --domain PHDSC
'''

As a result, documents are downloaded :

'''
# tree
.
├── conf
│   └── docs.json
└── documents
    └── PHDSC
        ├── IHE-PHDSC_Public_Health_White_Paper_2008-07-29.pdf
        └── IHE_PHDSC_Public_Health_White_Paper_2007_10_11.pdf

3 directories, 3 files
'''


