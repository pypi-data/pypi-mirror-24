pwv_kpno is a Python package for modeling the atmospheric transmission
function at Kitt Peak National Observatory. It is capable of providing
models in the optical and near-infrared (7000 to 11000 Angstroms) for years
2010 onward. Knowing the atmospheric transmission function is important when
correcting ground based astronomical observations for atmospheric effects.
Observed spectra are typically corrected using observations of a telluric
standard star. pwv_kpno provides an alternative method that does not require
dedicated observation time, and that can be run at the observers convenience.

When working in the optical and near-infrared, the atmospheric transmission
function is highly dependent on the amount of precipitable water vapor (PWV)
in the atmosphere. pwv_kpno models the atmospheric transmission using PWV
measurements provided by the SuomiNet Project. SuomiNet measures PWV values
by relating the delay in GPS signals to PWV levels in the atmosphere. This
package uses measurements taken by GPS receivers located at Kitt Peak AZ,
Amado AZ, Sahuarita AZ, Tucson AZ, and Tohono O'odham Community College.
For more details on the correlation between GPS signals and PWV levels see
Blake and Shaw, 2011. For more details on the SuomiNet project see
http://www.suominet.ucar.edu/overview.html.

