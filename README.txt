To estimate the evidence/expected value of apoptosis/signal flux of models in this repository

  1. Install PySB and all dependencies, such as BioNetGen.
  2. Install MultiNest.
  3. Install pyMultiNest from the LoLab fork at https://github.com/LoLab-VU/PyMultiNest.
  4. Modify the write.py file to specify the PySB, BioNetGen, and output directories.
  5. Run write.py to produce pyMultiNest run files, one for each model.
  6. Run each of the model specific run files.
