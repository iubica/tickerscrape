- Check out the wxPortfolio sandbox

- cd to wxPortfolio, check out the tickerscrape sandbox. The location
of tickerscrape should end up being wxPortfolio/tickerscrape.

- Python3 is required; use 'pip install' for all missing packages.
  - On Windows, install Python3 from python.org. Both the 32 bit and 64 bit versions are supported. Set the python3 executable in the PATH.
  - On Linux, follow distribution-specific steps to install Python3. On Centos 7, for example, install the python36u rpm package: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7
  - On Mac OSX, install XCode, Homebrew, then install Python3 using Homebrew: http://docs.python-guide.org/en/latest/starting/install3/osx/ 
  
- Execute 'wxPortfolio.py' (if python3 is in the PATH) or 'python wxPortfolio to start the application directly from the sandbox. On Windows, 'python3' is aliased to 'python'. On OSX, you must invoke python as 'python3', to distinguish it from the system 'python', which is version 2.
  
- Execute 'python setup.py build' to build an executable package, which can be
found under the 'build/<cpu-target>' folder.


