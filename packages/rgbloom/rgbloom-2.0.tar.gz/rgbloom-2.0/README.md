# rgbloom

This Python code retrieves RGB magnitudes computed from low resolution
spectra published in *Gaia* DR3, following the methodology described in
[Carrasco et al. (2023)](#3).  These magnitudes are given in the standard
system defined by [Cardiel et al. (2021a)](#1).

The code presented here is an updated version of
[rgblues](https://github.com/guaix-ucm/rgblues), which originally provided RGB
magnitudes from *Gaia* EDR3 photometric data, as explained in [Cardiel et al.
(2021b)](#2).

The RGB magnitudes provided by [Carrasco et al. (2023)](#3) are considered more
reliable as they are directly computed from the source spectrum, without the
need for any approximate calibration or constraints on source colour or
extinction. Moreover, the number of sources with RGB estimates has
significantly increased from approximately 15 million to around 200 million
objects (referred to as the 200M sample).  However, it is important to note
that the sky coverage of the 200M sample is still limited in some high Galactic
latitudes. For this reason, `rgbloom` also provides RGB estimates for sources
that do not belong to the 200M sample making use of the polynomial calibrations
of [Cardiel et al. (2021b)](#2), which can be useful for users requiring
calibrated RGB sources at those particular sky regions.

The code `rgbloom` performs a cone search defined by right ascension and
declination coordinates on the sky, along with a specified search radius.  This
cone search is performed making use of the Astroquery coordinated package of
astropy. 

Please note that a live internet connection is required for the code to
function properly.

## Installing the code

In order to keep your current Python installation clean, it is highly 
recommended to first build Python 3 *virtual environment*.

### Creating and activating the Python virtual environment

```shell
$ python3 -m venv venv_rgb
$ . venv_rgb/bin/activate
(venv_rgb) $
```

### Installing the package

We recommend installing the latest stable version, which is available via
the [PyPI respository](https://pypi.org/project/rgbloom/):

```shell
(venv_rgb) $ pip install rgbloom
```

The latest development version is available through [GitHub](https://github.com/guaix-ucm/rgbloom):

```shell
(venv_rgb) $ pip install git+https://github.com/guaix-ucm/rgbloom.git@main#egg=rgbloom
```

## Executing the program

Just execute it from the command line. For example

```shell
(venv_rgb) $ rgbloom 56.66 24.10 1.0 12
```

The last instruction executes the program providing the 
four positional arguments: right ascension, declination, search radius and 
limiting *Gaia* G magnitude. *Note that the coordinates and search radius 
must be given in decimal degrees*.

Whenever the code is executed, it will download certain auxiliary files to your
computer if they haven't been downloaded in a previous run. These files are
stored in a cache directory, and the location of this directory will be
displayed in the terminal output. You don't need to be concerned about the
specific location unless you want to delete these files to free up disk space.

The execution of this example should led to the following output in the
terminal (except for the absolute path where the auxiliary downloaded files 
are stored):

```
        Welcome to rgbloom version 1.9
        ==============================

Downloading data from 'https://guaix.fis.ucm.es/~ncl/rgbphot/gaiaDR3/reference_healpix8.csv' to file '/Users/cardiel/Library/Caches/pooch/635cd722cf61b23bd8eee20635e4d580-reference_healpix8.csv'.
<STEP1> Starting cone search in Gaia DR3... (please wait)
  INFO: Query finished. [astroquery.utils.tap.core]
        --> 310 objects found
        --> 23 objects classified as VARIABLE
<STEP2> Estimating RGB magnitudes in DR3 query using C21 polynomials OK!
<STEP3> Retrieving objects from the 200M sample in the enclosing HEALPIx level-8 tables
Downloading data from 'https://guaix.fis.ucm.es/~ncl/rgbphot/gaiaDR3/RGBsynthetic_NOVARIABLES/sortida_XpContinuousMeanSpectrum_006602-007952_RGB_NOVARIABLES_final.csv.gz' to file '/Users/cardiel/Library/Caches/pooch/2d94d5acfcb380d6dff1eaa207caa086-sortida_XpContinuousMeanSpectrum_006602-007952_RGB_NOVARIABLES_final.csv.gz'.
        * Required file: /Users/cardiel/Library/Caches/pooch/2d94d5acfcb380d6dff1eaa207caa086-sortida_XpContinuousMeanSpectrum_006602-007952_RGB_NOVARIABLES_final.csv.gz
          md5:f9cf7ed0f84eecda13ef6a408d291b96
        --> Number of objects: 100553
        --> Total number of objects: 100553
<STEP4> Cross-matching DR3 with 200M sample
        --> Number of objects in the 200M subsample.............: 100553
        --> Number of objects in DR3 query......................: 310
        --> Number of DR3 objects within the 200M sample........: 248
        --> Number of DR3 objects not present in the 200M sample: 62
<STEP5> Saving output CSV files
        --> file rgbloom_200m.csv saved
        --> file rgbloom_no200m.csv saved
<STEP6> Generating PDF plot
End of program
```

The `rgbloom` script executes the following steps:

- **Step 1**: cone search in *Gaia* DR3, gathering the following parameters: 
  `source_id`, `ra`, `dec`, `phot_g_mean_mag`, `phot_bp_mean_mag`,
  `phot_rp_mean_mag` and `phot_variable_flag`

- **Step 2**: initial RGB magnitude estimation using the polynomial 
  transformations given in Eqs. (2)-(4) of [Cardiel et al. (2021b)](#2).
  These values are only provided for objects in the field of view 
  that do not belong to the 200M sample.
  
- **Step 3**: downloading of the RGB magnitude estimates corresponding to 
  the 200M sample objects within the HEALPIx level-8 tables enclosing 
  the region of the sky defined in the initial cone search.
  
- **Step 4**: cross-matching between the DR3 and 200M subsamples to identify objects
  with RGB estimates derived from the low resolution *Gaia* DR3 spectra.
  
- **Step 5**: generation of the output files. Two files (in CSV format) are 
  generated: 

    - `rgbloom_200m.csv`: objects belonging to the 200M sample 
      with RGB magnitudes computed as described in [Carrasco et al. (2023)](#3).
      This CSV file provides the following columns:
      - `number`: consecutive number of the object in the CSV file (used in the final plot)
      - `source_id`: identification in *Gaia* DR3
      - `ra`: right ascension (from *Gaia* DR3)
      - `dec`: declination (from *Gaia* DR3)
      - `RGB_B`: blue RGB magnitude estimate
      - `RGB_G`: green RGB magnitude estimate
      - `RGB_R`: red RGB magnitude estimate
      - `errRGB_B`: uncertainty in the blue RGB magnitude estimate
      - `errRGB_G`: uncertainty in the green RGB magnitude estimate
      - `errRGB_R`: uncertainty in the red RGB magnitude estimate
      - `objtype`: type of source, according to the classification provided by
        *Gaia* DR3 (see [description of
        `GAIA_SOURCE`](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html) table for details):
        - `1`: object flagged as `NON_SINGLE_STAR`
        - `2`: object flagged as `IN_QSO_CANDIDATES`
        - `3`: object flagged as `IN_GALAXY_CANDIDATES`
        - `0`: none of the above
      - `qlflag`: global quality flag:
        - `0`: reliable source
        - `1`: suspicious source (blending, contamination, non-stellar
          identification)

    - `rgbloom_no200m.csv`: objects not included in the 200M sample, which
      RGB magnitudes are estimated using the approximate polynomial
      calibrations of [Cardiel et al. (2021b)](#2).
      This CSV file contains the following columns:
      - `number`: consecutive number of the object in the CSV file (used in the final plot)
      - `source_id`: identification in *Gaia* DR3
      - `ra`: right ascension (from *Gaia* DR3)
      - `dec`: declination (from *Gaia* DR3)
      - `phot_variable_flag`: photometric variability flag (from *Gaia* DR3)
      - `bp_rp`: G_BP-G_RP colour (from *Gaia* DR3)
      - `RGB_B`: blue RGB magnitude estimate
      - `RGB_G`: green RGB magnitude estimate
      - `RGB_R`: red RGB magnitude estimate

  The list of objects in these two files is sorted by right ascension.

- **Step 6**: generation of a finding chart plot (in PDF format): `rgbloom.pdf`. 
  The execution of the previous example generates a cone search around the
  [Pleiades](https://en.wikipedia.org/wiki/Pleiades) star cluster: ![Pleiades
  plot](https://guaix.fis.ucm.es/~ncl/rgbphot/gaiaDR3/pleiades_v8.png) In this
  plot (see [PDF
  file](https://guaix.fis.ucm.es/~ncl/rgbphot/gaiaDR3/pleiades_v8.pdf)) the
  object symbol size is scaled based on the Gaia G magnitude, and are color
  coded based on the *Gaia* G_BP - G_RP colour. Objects brighter than a
  predefined threshold are represented by larger star symbols. To aid in object
  identification, the consecutive identification numbers from the two files
  `rgbloom_200m.csv` and `rgbloom_no200m.csv`, are displayed in red and black,
  respectively. As these files are sorted by right ascension, the
  identification numbers increase sequentially on the chart.

  In the case of less reliable sources in `rgbloom_20m.csv` (where `qlflag=1`),
  the corresponding identification numbers are enclosed within a rectangle with
  a light-gray border. It is worth noting that when the `--nonumbers` parameter
  is used in the command line, the identification numbers will not be
  displayed.

  Starting from version 1.5, it is now possible to label each object with its magnitude
  instead of the objetc number in the CSV files. This can be achieved using the 
  `--display_mag <magname>` option, where `<magname>` can be any of the following: `RGB_B`, `RGB_R`,
  `RGB_R`, `Gaia_G`, `Gaia_BP`, `Gaia_RP`, `Gaia_BP-RP`. When this option is used,
  the displayed RGB magnitudes for objects outside the 200M sample
  correspond to the estimates calculated using the polynomial calibrations derived 
  by [Cardiel et al. (2021b)](#2), and are shown between parenthesis.

  In the case of objects that do not belong to the 200M sample (i.e., those in
  `rgbloom_no200m.csv`), a blue square
  has been overplotted on the sources flagged as variable in *Gaia* DR3, and a
  grey diamond on objects outside the *Gaia* -0.5 < G_BP - G_RP < 2.0 colour
  interval.

Note that the three output files, consisting of one PDF file and two CSV files, 
share the same root name, which is by default `rgbloom`. However, you can easily
modify this by using the optional argument `--basename <newbasename>` in the 
command line. This allows you to specify a new base name for the output files 
according to your preference.


## Additional help

Some auxiliary optional arguments are also available. See description 
invoking the script help:

```shell
$ rgbloom --help
```
```
usage: rgbloom [-h] [--basename BASENAME] [--brightlimit BRIGHTLIMIT]
               [--symbsize SYMBSIZE] [--max_symbsize MAX_SYMBSIZE]
               [--min_symbsize MIN_SYMBSIZE] [--mag_power MAG_POWER]
               [--display_mag {None,RGB_B,RGB_G,RGB_R,Gaia_G,Gaia_BP,Gaia_RP,Gaia_BP_RP}]
               [--num_fontsize NUM_FONTSIZE] [--nonumbers] [--noplot]
               [--nocolor] [--verbose]
               ra_center dec_center search_radius g_limit

RGB predictions from Gaia DR3 spectrophotometry (version 1.6)

positional arguments:
  ra_center             right Ascension (decimal degrees)
  dec_center            declination (decimal degrees)
  search_radius         search radius (decimal degrees)
  g_limit               limiting Gaia G magnitude

optional arguments:
  -h, --help            show this help message and exit
  --basename BASENAME   file basename for output files
  --brightlimit BRIGHTLIMIT
                        objects brighter than this Gaia G limit are displayed
                        with star symbols (default=8.0)
  --symbsize SYMBSIZE   global multiplying factor for symbol size
                        (default=1.0)
  --max_symbsize MAX_SYMBSIZE
                        maximum symbol size in chart (default=1000)
  --min_symbsize MIN_SYMBSIZE
                        minimum symbol size in chart (default=10)
  --mag_power MAG_POWER
                        power to scale symbol sizes in chart (default=3)
  --display_mag {None,RGB_B,RGB_G,RGB_R,Gaia_G,Gaia_BP,Gaia_RP,Gaia_BP_RP}
                        display selected magnitude instead of object number
  --num_fontsize NUM_FONTSIZE
                        font size for numbers in chart (default=5)
  --nonumbers           do not display object identification number in PDF
                        chart
  --noplot              skip PDF chart generation
  --nocolor             do not use colors in PDF chart
  --verbose             increase program verbosity```
```

## Citation

If you find this Python package useful, 
please cite [Cardiel et al. (2021a)](#3)
(to quote the use of the standard RGB system)
and [Carrasco et al. (2023)](#3) (where the computation of the RGB magnitudes
from the low resolution spectra published in *Gaia* DR3 is explained).

## Related information

You can visit the [RGB Photometry](https://guaix.ucm.es/rgbphot) web page at
the Universidad Complutense de Madrid.

## Bibliography

<a id="1">Cardiel et al. (2021a)</a>, 
MNRAS, https://ui.adsabs.harvard.edu/abs/2021MNRAS.504.3730C/abstract

<a id="2">Cardiel et al. (2021b)</a>, 
MNRAS, https://ui.adsabs.harvard.edu/abs/2021MNRAS.507..318C/abstract

<a id="3">Carrasco et al. (2023)</a>, Remote Sensing, https://www.mdpi.com/2072-4292/15/7/1767
