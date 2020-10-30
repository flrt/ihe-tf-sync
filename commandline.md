Synchronize IHE documents - Command Line
========================================

The starting point is the root directory (`documents` by default).
Then subdirectories will be created to store documents by domains.

Domains can be specified, with the `--domain` argument.

To get all documents from two domains: ITI and CARD, simplify run

    python sync.py --domain ITI,CARD


The directory will updated to be something like this: 


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

By default, only documents from the technical framework are searched. But it's possible to extended the search to the documents in public comment. In that case, just add the `--comment` in the command line.

[*Example*](#example-comment) : synchronize documents from `PHARMACY` domain. Then add the documents available for public comments (Can be done in a single step, obviously)

1.Synchronize documents in final state:



    $ python sync.py --output /home/fred/doc/ihe-docs --confdir /home/fred/doc/ihe-conf --domain PHARMACY
    Get information about documents
    .........
    235 documents found in IHE website : technical_frameworks

    Available documents :
    TF: 8 documents
    PAT: 3 documents
    CARD: 17 documents
    DENT: 1 documents
    ENDO: 3 documents
    EYECARE: 7 documents
    ITI: 42 documents
    SUPPL: 3 documents
    LAB: 2 documents
    PALM: 9 documents
    PCC: 39 documents
    PHDSC: 2 documents
    PCD: 16 documents
    PHARMACY: 11 documents
    QRPH: 28 documents
    QUALITY: 1 documents
    RO: 7 documents
    RAD: 36 documents

    Clean documents not in sync...

    Syncing PHARMACY domain...
    Newer document IHE_Pharmacy_Suppl_Common.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_DIS.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_CMA.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_PML.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_CMPD.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_MTP.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_PADV.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_PRE.pdf found: download it...
    Newer document IHE_Pharmacy_Suppl_HMW.pdf found: download it...
    Newer document IHE_Pharm_Suppl_MMA.pdf found: download it...
    Newer document IHE_Pharm_Suppl_UBP.pdf found: download it...
    

2.Add documents in public comments:



    $ python sync.py --output /home/fred/doc/ihe-docs --confdir /home/fred/doc/ihe-conf --comment --domain PHARMACY
    Get information about documents
    .........
    235 documents found in IHE website : technical_frameworks
    Get information about documents

    10 documents found in IHE website : public_comment

    Available documents :
    TF: 8 documents
    PAT: 3 documents
    CARD: 18 documents
    DENT: 1 documents
    ENDO: 3 documents
    EYECARE: 7 documents
    ITI: 42 documents
    SUPPL: 3 documents
    LAB: 2 documents
    PALM: 10 documents
    PCC: 40 documents
    PHDSC: 2 documents
    PCD: 17 documents
    PHARMACY: 12 documents
    QRPH: 31 documents
    QUALITY: 1 documents
    RO: 9 documents
    RAD: 36 documents

    Clean documents not in sync...

    Syncing PHARMACY domain...
    Newer document IHE_Pharm_Suppl_MMA.pdf found: download it...
    Newer document IHE_Pharm_Suppl_UBP.pdf found: download it...
    Newer document IHE_PHARM_WP_Supply_Rev1-0_PC_2019-11-18.pdf found: download it...

# Run without docker
Clone this repo and run the `sync.py` program.


    # git clone https://github.com/flrt/ihe-tf-sync.git
    # cd ihe-tf-sync
    # python sync.py --help
    
    usage: sync.py [-h] [--output OUTPUT] [--domain DOMAIN]
    
    optional arguments:
      -h, --help       show this help message and exit
      --output OUTPUT  output directory in wich the documents will be downloaded
      --confdir CONFDIR  directory containing the meta data about the documents
      --comment          get documents in public comments
      --domain DOMAIN    specify domain(s)


# Run with docker

Just one line to get your documents. Mount your local directory and call the program.

Mount the local directory with the `-v` parameter `${PWD}` for the current directory to `/opt/data`.

Call `python sync.py` with or without parameters. See `sync.sh` for syntax.

## Build your own container

    # docker build -t name ihe-tf-sync:1.0 .

Then use it :
    
    # mkdir ihe_docs
    # cd ihe_docs
    # docker run -ti --rm -v ${PWD}:/opt/data ihe-tf-sync:1.0 python sync.py --domain PHDSC

## Use the container in docker Hub
Nothing to build, just reference the [flrt/ihe-tf-sync](https://hub.docker.com/r/flrt/ihe-tf-sync/) container.

    # mkdir ihe_docs
    # cd ihe_docs
    # docker run -ti --rm -v ${PWD}:/opt/data flrt/ihe-tf-sync python sync.py --domain PHDSC


As a result, documents are downloaded:

    # tree
    .
    ├── conf
    │   └── docs.json
    └── documents
        └── PHDSC
            ├── IHE-PHDSC_Public_Health_White_Paper_2008-07-29.pdf
            └── IHE_PHDSC_Public_Health_White_Paper_2007_10_11.pdf

    3 directories, 3 files

## Even simplier
If you don't want to deal with docker explicitly, 2 shells can provide help:

- sync.sh for *nix environment
- sync.bat for windows environment

**Required**: docker has to been installed before

Then you can simply
 
### *nix environment 

    $ curl -O https://raw.githubusercontent.com/flrt/ihe-tf-sync/master/sync.sh
    $ sh sync.sh ITI,RAD

### windows environment

    $ Invoke-WebRequest -Uri https://raw.githubusercontent.com/flrt/ihe-tf-sync/master/sync.ps1 -OutFile sync.ps1 
    $ sync.ps1 ITI,RAD   

# Example
Look at [exec samples](exec.md) for more details.

# License 

[MIT](LICENSE) 
