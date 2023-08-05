# Notes for vulnmine developers

This article gives some quick notes for people interested in customizing /
developing Vulnmine.

## Plugins

### Overview

There are two sample plugins provided in the  _vulnmine/plugins_ directory:

* _plugin1.py_: Shows how complementary information can be used to augment the
SCCM host record.
* _plugin2.py_: Shows how to produce customized statistics and output files.

The plugins use the [python yapsy framework](http://yapsy.sourceforge.net/)

Plugins are defined using the _*.yapsy-plugin_ files (also in the _plugins_ directory.)

In Vulnmine, plugins are loaded by _util.py_'s _load_plugins()_ function. The plugin
manager object is initialized there.

The mainline vulnmine.py calls the plugins (in the _rd_sccm_hosts()_ and
_output_stats()_ functions.)

### Plugin Interaction with Vulnmine class objects

Plugins can access the main Vulnmine class objects:

* The object instance is passed to the plugin as an I/P parameter. The safest
approach is for the plugin to load the pickled version of the class object, then
call the object's "get()" method. This provides a copy of the object's pandas
dataframe to the plugin.

* The plugin code can modify the object contents. This includes adding new
custom columns to the object's dataframe. The sample plugin1.py provided
has examples of this.

* The custom fields added to the SccmHost object's dataframe pass through the
processing and show up in the final consolidated dataframe. The sample
plugin2.py then uses these custom fields to produce site-specific statistics.

### Plugin Input / Output

Plugin code can also read input data sets and print output.

For simplicity, python "print()" is used.

## The test data

Realistic test data is provided with the released code. This section
gives a basic description of this data

### The organization "mycorp.com"

The "mycorp.com" company has 4 sites: **North, South, East, West**

There are two regions:  **A** (sites North, West) and **B** (sites South, East).

 In the organization's Active Directory:

 * VIP people's desktops / laptops are in the AD group **"VIP"**.
 
 * **Desktops, laptops, and servers** are grouped each in their own OUs. This is
reflected in the host's Distinguished Name.

In general, older vulnerable software was used to build the test data. However
the NIST NVD data was the most recent available at the time. This ensured that
lots of vulnerabilities would be found.

### The input data sets

The corresponding input data flat files are all found in _data/csv_:

* __v_R_System_.csv__:  The CSV version of the corresponding SCCM view.
* __v_GS_ADD_REMOVE_PROGRAMS / _64__: Idem

* __ps-ad-vip.csv__: A CSV flat file containing the contents of the AD host group
"VIP" which contains VIP PCs.
