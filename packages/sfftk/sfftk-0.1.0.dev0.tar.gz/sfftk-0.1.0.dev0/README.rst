================================================================
sfftk: EMDB-SFF Toolkit
================================================================

.. contents:: Table of Contents

----------------------------------------------------------------
About
----------------------------------------------------------------

sfftk
================================================================
The EMDB-SFF Toolkit (sfftk) is a set of utilities to generate, edit and display segmentation data contained in EMDB Segmentation File Format (SFF) files. 
EMDB-SFF is the result of a community effort to unify representation of segmentations derived from various segmentation tools.
The toolkit is designed as a set of subcommands that perform the various functions:

.. code:: bash

	pkorir@pkorir-tarakimu:trunk $ python sff -h
	usage: sff [-h] EMDB-SFF tools ...
	
	The EMDB-SFF Toolkit (sfftk)
	
	optional arguments:
	  -h, --help      show this help message and exit
	
	Tools:
	  The EMDB-SFF Toolkit (sfftk) provides the following tools:
	
	  EMDB-SFF tools
	    convert       converts from/to EMDB-SFF
	    updateschema  update schemas (emdb_sff.py or roi.py) using generateDS.py
	    list          list various entities
	    createroi     create ROIs and write to file
	    attachroi     attach ROIs to image
	    deleteroi     delete ROIs associated with image
	    config        manage configs
	    view          view file summary
	    view3d        render 3D model
	    tests         run unit tests

The various utilities are designed as packages for reusability.

EMDB-SFF
================================================================
The EMDB-SFF has two principal roles:

1. An open and flexible format for storing segmentations
2. A means to capture annotation of segmentations

The current version of the file format is 0.5.8 pending discussion and feedback from the EM community.

As a unifying representation, EMDB-SFF will facilitate display of segmentations alongside associated reconstructed volumes.
EMDB-SFF incorporates four generic segmentation representations:

- 3D volumes
- contours
- meshes (surfaces)
- shape primitives (ellipsoid, cuboid, cylinder, cone)

Funding
================================================================

TBD


----------------------------------------------------------------
Obtaining sfftk
----------------------------------------------------------------

TBD

----------------------------------------------------------------
Installing sfftk
----------------------------------------------------------------

TBD

----------------------------------------------------------------
Purpose
----------------------------------------------------------------

sfftk is designed to:

- convert application specific segmentation file formats (AS-SFF) into EMDB-SFF;
- convert EMDB-SFF files into AS-SFF (where possible);
- display segmentations contained in EMDB-SFF files for inspection;
- prepare OMERO ROIs from segmentations;
- attach generated OMERO ROIs to corresponding images hosted in OMERO;
- annotate segmentations using biological ontologies;
- view segmentation metadata;


----------------------------------------------------------------
Audience
----------------------------------------------------------------

sfftk is aimed at 3D electron microscopy (3DEM) practitioners.

----------------------------------------------------------------
Input Data
----------------------------------------------------------------

sfftk accepts the following data types:

- several AS-SFFs (see Supported Formats below for the up-to-date listing)
- ROI files: XML files formatted with the ROI schema (link);
- EMDB-SFF files: XML files formatted with the EMDB_SFF schema;  


----------------------------------------------------------------
Supported Formats
----------------------------------------------------------------

(extension in alphabetic order)

- Amira Mesh (.am)
- EMDB Map masks (.map)
- IMOD (.mod)
- ROI (.roi)*
- Segger (.seg)
- EMDB-SFF (.sff)
- Amira HxSurface (.surf)

*internal file

----------------------------------------------------------------
Dependencies
----------------------------------------------------------------

(alphabetic order of Python import name)

sfftk has the following dependencies:

- generateDS
- h5py
- matplotlib
- numpy
- omero
- scipy
- simpleparser
- skimage
- bitarray (?)

----------------------------------------------------------------
Features
----------------------------------------------------------------


Generic Options
================================================================
Some options work on most subcommands. Run `sff <subcommand> -h` to verify available options.

-v/--verbose
-h/--help

Converting Files to EMDB-SFF
================================================================
Supported AS-SFF files are converted to EMDB-SFF files using the `convert` subcommand:

.. code:: bash

	$ sff convert <file.ext>

where `ext` is a supported extension.  

Example:

.. code:: bash

	# verbosely convert an IMOD file into EMDB-SFF and write the output to file.sff
	$ python sff convert -v sff/test_data/test_data.mod -o file.sff
	Thu Jul 14 16:43:04 2016	Created XMLData object from schema <schema.emdb_sff.segmentation object at 0x102a4f610>
	Thu Jul 14 16:43:04 2016	Reading in IMOD file from sff/test_data/test_data.mod file
	Thu Jul 14 16:43:04 2016	Writing out XML to file file.sff

Viewing Segmentations
================================================================
Viewing raw data
----------------------------------------------------------------
The raw data can be viewed through the `view` subcommand:

.. code:: bash

	$ sff view <file.ext>
	
Example:

.. code:: bash

	# view metadata from an Amira Mesh file
	$ sff view sff/test_data/test_data.am

	*******************************************************************************
	Amira Mesh file
	Version:              2.1
	Format:               BINARY-LITTLE-ENDIAN
	*******************************************************************************
	Materials:  
	            
	Mitochondria_
	Id                    4
	Color                 [1.0, 1.0, 0.0]
	
	Inside      
	Id                    2
	Color                 [0.64, 0.0, 0.8]
	
	Mitochondria
	Id                    3
	Color                 [0.0, 1.0, 0.0]
	
	NE          
	Id                    6
	Color                 [1.0, 0.0, 0.0]
	
	mitochondria__
	Id                    5
	Color                 [0.0, 0.125, 1.0]
	
	Exterior    
	Id                    1
	
	            
	Mesh                  200 images each of 971 X 862 pixels (3 colors)
	            
	*******************************************************************************


Configurations (TBD)
================================================================
Most subcommands act transiently. However, subcommands which require persistent data must save configurations. 
For example, subcommands that require connections to an OMERO instance must at least store the host, port and username (not advisable to store passwords). 
Also, updating the schema needs a persistent record of the location and destination of the schema and schema API, respectively.

.. code:: bash

	$ sff config <config.name>=<config.value>

Example:

.. code:: bash

	$ sff config omero.host=localhost omero.port=4064 omero.user=test 


Listing Supported AS-SFFs
================================================================

TBD

Annotating Segmentations
================================================================

TBD

----------------------------------------------------------------
Using the sfftk API
----------------------------------------------------------------

sfftk provides an API to its functionality for reusability. 

1. Read EMDB-SFF files

.. code:: python
	:number-lines:
	
	from sfftk.readers.sffreader import get_data
	
	# get_data takes an EMDB-SFF file name
	descriptor, segments, colours, alphas = get_data(sff_fn)
	
	# descriptor is one of 'threeDVolume', 'contourList', 'meshList', 'shapePrimitive'
	# segments is a dictionary of contours/meshes
	# colours is a list with as many RGB float-triples as segments
	# alphas is a list with as many floats (in the range 0-1 inclusive) as segments
	
2. Convert supported AS-SFF files to EMDB-SFF

TBA

3. Convert EMDB-SFF to supported AS-SFF files

TBD

----------------------------------------------------------------
Extending sfftk
----------------------------------------------------------------

TBD

----------------------------------------------------------------
Developers
----------------------------------------------------------------

Paul K. Korir, PhD

----------------------------------------------------------------
Contact
----------------------------------------------------------------

For questions, comments and/or bug reports, please write to:

pkorir [THE @ SIGN] ebi [FIRST DOT] ac [ANOTHER DOT] uk
paul.korir [THE @ SIGN] gmail [ONLY ONE DOT] com
