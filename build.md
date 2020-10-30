Build instructions
=================

# windows
Build the msi distribution file

   set base=c:\\dev\\py
   cd %base%\\ihe-tf-sync
   .\Scripts\activate
   pip install -r requirements.txt
   python setup.py bdist_msi
