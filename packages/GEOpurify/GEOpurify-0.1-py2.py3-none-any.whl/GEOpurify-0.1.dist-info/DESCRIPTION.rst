* GEOpurify
/Atlas of tools making Gene Expression Omnibus data amicable to machine learning./

** Installation

#+BEGIN_SRC sh
pip install GEOpurify
#+END_SRC

** Example Usage

#+BEGIN_SRC python :results output org drawer
from GEOpurify import GEOpurifier
g = GEOpurifier()
gds_df = g.gdspurify("GDS4376")
#+END_SRC

** Methods

*** ~filepurify(filepath, separation="\t")~

Given a path to a standard table with GEO data, returns a dataframe
with gene expression and GSM ids in separate columns.

*** ~dirpurify(dirname)~

Given a path to a directory with standard tables of data from GEO,
applies ~filepurify~ and return a combined dataframe.

*** ~gdspurify(gds_id, load_extra_features=False)~

Given a GDS id, extracts data on a platform, platform organism,
platform techonolgy type and sample organism used. If
~load_extra_features~ is set to ~True~, extra features are fetched
from the GDS columns.

Saves already processed tables corresponding to the GDS in the
directory ~data/tmp~, while storing the raw GEO data in the directory
~data/raw~.

*** ~gdspolypurify(self, gds_list_path, load_extra_features=False)~

Given a path to a file listing GDS ids, each on a new line, applies
~gdspurify~ to each and combines all the data into one dataframe.


