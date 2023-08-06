Piccolo/Picalor Python API calling interface

What is it?
-----------
A python package enabling users to call a set of Picwin32.dll or Ganessa_SIM.dll API functions and subroutines within python scripts.

Installation
------------
:Windows only:

  pip install ganessa-x.y.z-cp27-cp27m-win32.whl

Requirements
------------

  #) python requirements: numpy 1.7 or above
  #) Piccolo or Picalor kernel library (picwin32.dll), starting from version 5 (141203)
  #) valid Piccolo or Picalor license

This tool requires Picwin32.dll to be in the PATH or in one of the following directories:
 [ C: or D: ] / ['Program Files' or 'Program Files (x86)' ]
			/ 'Gfi Progiciels' or 'Safege' or 'Adelior']
			/ ['Piccolo5_' or 'Piccolo6_' or 'Ganessa_'] ['fr' or 'uk' or 'esp' or 'eng']
			/ ['Picwin32.dll' or 'Ganessa_SIM.dll' or 'Ganessa_TH.dll' ]


Content
-------

The package provides:
 #) 'sim' package:
     - a few basic functions for reading or loading a model, running simulations
     - 'getter' functions for individual objects and attributes, for time series
     - iterators of links, nodes, tanks, and tables, or over Piccolo selections
 #) 'util' package: various functions
 #) 'OpenFileMMI' provides classes for opening dialog frame for a .dat/.bin model file, and output (result) file

Model object and parameters can be modified using Piccolo command language (see cmd, cmdfile and execute)

History of the document
-----------------------

Created 2013-07-04
Revised 2015-05-03: since 2014-12-04 Picwin32.dll is compatible with this API
Revised 2016-07-07: provided as .rst


