# Makefile for the tickerscrape project
HOSTNAME=$(shell hostname)
PYTHON=python
ISCC=iscc
VERSION=$(shell python src/version.py)

# Host-specific settings
ifeq ($(HOSTNAME),andrei-HP)
  PYTHON=/cygdrive/c/Users/andrei/AppData/Local/Programs/Python/Python36/python.exe
  TARGET=windows
  CPU=x86_64
  CPU_BUILD_DIR=exe.win-amd64-3.6
endif

ifeq ($(HOSTNAME),LAPTOP-2SD4UBV0)
  PYTHON=/cygdrive/c/Users/daria/AppData/Local/Programs/Python/Python36-32/python.exe
  TARGET=windows
  CPU=x86
  CPU_BUILD_DIR=exe.win32-3.6
endif

ifeq ($(HOSTNAME),Darias-MacBook-Air.local)
  PYTHON=python3
  TARGET=mac-osx
  CPU=x86_64
  CPU_BUILD_DIR=exe.macosx-10.13-x86_64-3.6
endif

ifeq ($(HOSTNAME),thinkcentre)
  PYTHON=python
  TARGET=linux
  CPU=x86_64
  CPU_BUILD_DIR=exe.linux-x86_64-3.6
endif

EXE_SUFFIX=
ifeq ($(TARGET),windows)
  EXE_SUFFIX=.exe
endif

UPDATE_TGT=tickerscrape-update-$(VERSION).tgz

all: installer update

installer: exe

# upload-installer is target specific. upload-update is target independent.
upload: upload-installer upload-update

ifeq ($(TARGET),windows)
  installer: build/$(CPU_BUILD_DIR)/build/installer/mysetup$(EXE_SUFFIX)

  build/$(CPU_BUILD_DIR)/build/installer/mysetup$(EXE_SUFFIX): build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX) TickerScrape.iss
	$(ISCC) build/$(CPU_BUILD_DIR)/TickerScrape.iss

  upload-installer: installer
	chmod 755 build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe
	scp build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe bitdrib1@bitdribble.com:www/tickerscrape/downloads/tickerscrape-install-$(VERSION)-$(TARGET)-$(CPU)-setup.exe
endif

ifeq ($(TARGET),linux)
  installer: build/$(CPU_BUILD_DIR)/build/installer/tickerscrape.tgz

  build/$(CPU_BUILD_DIR)/build/installer/tickerscrape.tgz: build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX)
	@if [ ! -d build/$(CPU_BUILD_DIR)/build/installer ]; then mkdir -p build/$(CPU_BUILD_DIR)/build/installer; fi
	cd build/$(CPU_BUILD_DIR); tar cvfz tickerscrape.tgz bitmaps data libpython* README.md views bmp_source Format.py Main.py scrape widgets cursors lib TickerScrape; mv tickerscrape.tgz build/installer

  upload-installer: installer
	scp build/$(CPU_BUILD_DIR)/build/installer/tickerscrape.tgz bitdrib1@bitdribble.com:www/tickerscrape/downloads/tickerscrape-install-$(VERSION)-$(TARGET)-$(CPU).tgz
endif

exe: build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX)

build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX): *.py */*.py
	$(PYTHON) setup-cx-freeze.py build
	touch $@

update: build/update/$(UPDATE_TGT)

build/update/$(UPDATE_TGT): *.py */*.py
	rm -rf build/update/*
	@if [ ! -d build/update/tmp ]; then mkdir -p build/update/tmp; fi
	cp -a agw bitmaps bmp_source cursors data LICENSE README.md scrape snippets src TickerScrape.py views widgets build/update/tmp
	@find build/update/tmp -name __pycache__ -exec rm -rf {} \; 2>/dev/null || exit 0
	cd build/update/tmp; tar cvfz ../$(UPDATE_TGT) .

upload-update: update
	scp build/update/$(UPDATE_TGT) bitdrib1@bitdribble.com:www/tickerscrape/downloads/

clean:
	rm -rf build/$(CPU_BUILD_DIR) build/update

help:
	@echo Targets: 
	@echo "  all - all targets except upload"
	@echo "  installer - platform specific installer"
	@echo "  update - platform specific update pakage"
	@echo "  upload, upload-installer, upload-update - do the web site uploads"

debug-dump:
	@echo HOSTNAME=$(HOSTNAME)
	@echo PYTHON=$(PYTHON)
	@echo CPU_BUILD_DIR=$(CPU_BUILD_DIR)
	@echo VERSION=$(VERSION)

.SUFFIXES:
