================
Plugins
================

ClamAV
------
Allows malware scanning of submitted files via ClamAV.

Prerequisites
+++++++++++++

* Worker nodes running ClamAV daemon (http://www.clamav.net/)
* Python ClamD module (https://pypi.org/project/clamd/)

Installation
++++++++++++

* Install ClamAV from OS packages and configure as required
* Rename the clamav.py.plugin file in Nemesis plugin directory to clamav.py
* Reinstall Nemesis via setuptools
* Install Python ClamD module into your Nemesis virtual env
* Update your analysis_plugins list in your nemesis.conf file
* Once compelete restart the Nemsis worker service

::
	
	source /opt/nemesis/bin/activate
	cd ~/git/nemesis
	cp python_nemesis/plugins/clamav.py.plugin python_nemesis/plugins/clamav.py
	python setup.py install
	pip install clamd
	vi /etc/nemesis/nemesis.conf # Update analysis plugins list to include clamav
	service nemesis-worker restart

Sample Artifacts
++++++++++++++++

Malware Detected::
	
	{
		"success": true,
	 	"result": {"is_malware": true,
			   "malware_type": "EICAR-Test-File"},
		"message": null
	}

Malware Not Detected::
	
	{
		"success": true,
	 	"result": {"is_malware": false,
			   "malware_type": null},
		"message": null
	}

EXIF
----
Extracts EXIF data from compatible image files.

Prerequisites
+++++++++++++

* Python ExifRead module (https://pypi.org/project/ExifRead/)

Installation
++++++++++++

* Rename the exif.py.plugin file in Nemesis plugin directory to exif.py
* Reinstall Nemesis via setuptools
* Install Python ExifRead module into your Nemesis virtual env
* Update your analysis_plugins list in your nemesis.conf file
* Once compelete restart the Nemsis worker service

::
	
	source /opt/nemesis/bin/activate
	cd ~/git/nemesis
	cp python_nemesis/plugins/exif.py.plugin python_nemesis/plugins/exif.py
	python setup.py install
	pip install exifread
	vi /etc/nemesis/nemesis.conf # Update analysis plugins list to include exif
	service nemesis-worker restart

Sample Artifacts
++++++++++++++++

EXIF extracted::
	
	{
		"success": true,
	 	"result": {"exif_tags": [...]}
		"message": null
	}

Unable to extract EXIF data::
	
	{
		"success": false,
	 	"result": null,
		"message": "Unable to extract EXIF from EXE filetype, only able to extract EXIF from JPEG and TIFF file types."
	}
