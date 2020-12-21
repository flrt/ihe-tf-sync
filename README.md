Synchronize IHE documents
=========================

This basic tool allows you to be the up-to-date with the IHE TF documents, available on the [IHE.net website](https://www.ihe.net/resources/technical_frameworks/).

![IHE intl.](https://www.ihe.net/wp-content/uploads/2018/02/ihe-logo.svg)

These tool *do not replace* anything from IHE communication, it's only a way to keep locally all the documents in sync.

The documents are downloaded and stored locally thanks to their names.

You can use either the GUI app or the [command line](commandline.md)

# GUI Application

The application is avalaible for windows, linux and macos.
Simply launch the executable, select domains you want to synchronize and let it downnload files.

The main window looks like :

### on linux

![Linux app](/doc/main_linux.png)

### on mac OS

![MacOS app](/doc/main_macos.png)

### on windows

![Windows app](/doc/main_windows.png)




# Command Line overview 

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

More details [here](commandline.md).


# Keep up-to-date
Once you ran the program, each new execution will download only the newer documents (since last run).

Remember to be informed by IHE mechanisms:

- [twitter](https://twitter.com/IHEIntl) 
- [Monthly Newsletters](https://www.ihe.net/monthly-newsletters/)
- [mail from IHE about Technical Publications](https://www.ihe.net/monthly-newsletters/technical-publications/)
- [Linkedin](https://www.linkedin.com/company/iheintl/)

# License 

[MIT](LICENSE) 
