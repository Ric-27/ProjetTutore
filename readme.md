# Projet Tutoré

Ric Branch. Homography Solution
Inside references are the codes used to create the final product

Inside final product is the tested, final and proved method.

## Usage
Tested with: Python 3.6.9

Run inside the final product folder.
```command
python3 configure.py # run configuration with default path to reference image
python3 configure.py -img "Debug/reference_t.jpg" -qd True # this to rerun the configuration and add planes if needed (use execute without .txt)

python3 execute.py -img "Debug/reference_t.jpg" -txt True #this to include graphical solution only using the warp perspective and not different planes
python3 execute.py #this to use the data.npz file and have only command result with different z planes if created
```

## Equipe
Iad Abdul
Ricardo RICO
David Velasquez
Kai Zhang
## License
[MIT](https://choosealicense.com/licenses/mit/)