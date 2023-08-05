Pick Peak
=======================

Scan Alignment is a PyQtGraph-based graphical user interface. It allows for horizontal line alignment of images
collected in the TwinMic beamline through Scanning transmission x-ray microscopy (STXM) imaging technique.


----

README
""""""""""""""""" 

**Introduction**
 
The file should use UTF-8 encoding and be written using `reStructuredText
<http://docutils.sourceforge.net/rst.html>`_. It
will be used to generate the project webpage on PyPI and will be displayed as
the project homepage on common code-hosting services, and should be written for
that purpose.

**Installation**

For standard Python installations, install pickpeak using pip:

.. code:: bash

    pip install -U pip setuptools
    pip install pickpeak

**Usage**

.. code:: python
	
	from pickpeak.pickpeak import PickPeak as pp
	peaks = pp(spectrum) #spectrum shoud be type numpy.ndarray
	peaks.gui_design() #calls the GUI 
	list_of_peaks = peaks.peak_list #returns the current list of peaks collected through the GUI

**Requirements**

* `Python 2.7 <https://www.python.org/downloads/>`_.
* `Setuptools <https://setuptools.readthedocs.io/en/latest/>`_.
* `Tifffile <https://github.com/blink1073/tifffile>`_.
* `H5Py <http://www.h5py.org/>`_.
* `Matplotlib <https://matplotlib.org/>`_.
* `NumPy <http://www.numpy.org/>`_.
* `PyQtGraph <http://www.pyqtgraph.org/>`_.

    
