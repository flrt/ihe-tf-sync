Synchronize IHE documents - User manuel
=========================

# Main tab

The main tab shows the different domains of IHE.

A standard process can be released in 3 steps (clicks).

## step 1 : select domains to synchronize

![Windows app](/doc/main_windows.png)

Each domain can be checked. If the domain is checked, all the available documents on the website will be downloaded. 
If a document is no longer present on the IHE website, it will be deleted locally (if previously downloaded).

![domain selection](/doc/detail_list_windows.png)

In this configuration, the document of the PALM and PAT will be synchronized. 
The result will be 10+3 documents present locally.

When documents have been downloaded, the folder icon allows the user to access directly to the local directory.

![local directory](/doc/step2-PALM.png)

When the cell is orange, a difference between what files should be present and what files are present exists. It will be fixed by the synchronize process.

![local diff](/doc/diff_local_macos.png)

## step 2 : verify the synchronization

Once the domains are selected, click the synchronize button. A window will show what will be done.

![confirm actions](/doc/confirm_sync_macos.png)

If it's what you want to do, then click the OK button.

## step 3 : synchronize process

![synchronize](/doc/download_windows.png)

The process will download the missing documents and suppress the obsolete ones.

# configuration tab

The configuration tab allows the user to set :

- the location of the configuration file (domains selected, etc.)
- the location of the documents, stored locally. 
- the level of the debugger
- the localtion of the debug file
- the IP and port address used to check if the internet connection is up

It's a classical configuration tab, nothing special.

![configuration - change directory](/doc/changedir_linux.png)