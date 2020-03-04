# VeraCrack v1.0
  Brute Force Veracrypt Container Password Guesser
  [![Python 3.8.2](https://img.shields.io/badge/Python-3.8.2-blue.svg
      )](https://www.python.org/downloads/release/python-382/)

  Tested on Windows 10 with [Veracrypt-64.exe 1.24-Update4
  ](https://www.veracrypt.fr/en/Downloads.html)


## Description
  A brute force password guesser for decrypting Veracrypt encrypted volumes
  that use a HMAC-SHA-512 hash. **Requires
  [Veracrypt](https://www.veracrypt.fr/en/Downloads.html) to be installed**.

  Given a list of passwords in a single column list, and a compatible encrypted
  Veracrypt volume, attempts each password until volume is decrypted and
  mounted or list is exhausted.

  **WARNING:** Once attempted, passwords are not secret; they are used in
  command line arguments and thus may remain in OS logs.


## Usage
  _If veracrack_config.txt has not been generated, see **First time use
  tutorial**_

  Run with an elevated command prompt (run command line as administrator).

  `python veracrack.py <targetFilePath> <passwords.csv>`

  * targetFilePath - path to target encrypted Veracrypt container.
  * passwords.csv - path to list of potential passwords.

### First time use tutorial

  1. Clone repository

  2. Open the command line and navigate to veracrack directory

  3. Generate sample config using `python veracrack.py --configGen`

  4. Set **veracryptexepath** in config file as path to where Veracrypt-64.exe
  is installed on your system. [Install Veracrypt](
      https://www.veracrypt.fr/en/Downloads.html)

  5. Navigate to veracrack directory in the **elevated command prompt**
  (run as administrator) and run program using Python with required arguments.
  Included example:

  `python veracrack.py VeraCrack_10 potentialPasswords.csv`

### Configuration

  Default filename: veracrack_config.txt

  * veracryptExePath
    * Set the path to your installed Veracrypt-x64.exe. (Required)
  * driveLetter
    * Which drive letter to mount target volume (must not already be in use)
  * verboseMode
    * Set debugging level


## Performance Notes
  Mean seconds per password attempt when decrypting VeraCrack_100 (not included)
  on a consistent system, with 5 trials.

  VeraCrack  | Seconds per Password Attempt
  -----------|-----------------------------------
   v1.0      |  2.073236 ± 0.013


## Changelog

### v1.0
  Created initial application and documentation.
