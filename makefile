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

UPDATE_TGT=tickerscrape-update-$(VERSION)-$(TARGET)-$(CPU).tgz

all: installer update

installer: exe

ifeq ($(TARGET),windows)
  installer: build/$(CPU_BUILD_DIR)/build/installer/mysetup$(EXE_SUFFIX)

  build/$(CPU_BUILD_DIR)/build/installer/mysetup$(EXE_SUFFIX): build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX) TickerScrape.iss
	$(ISCC) build/$(CPU_BUILD_DIR)/TickerScrape.iss

  upload: installer update
	chmod 755 build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe
	scp build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe bitdrib1@bitdribble.com:www/tickerscrape/downloads/tickerscrape-install-$(VERSION)-$(TARGET)-$(CPU)-setup.exe
	scp build/update/$(UPDATE_TGT) bitdrib1@bitdribble.com:www/tickerscrape/downloads/
endif

ifeq ($(TARGET),linux)
  installer: build/$(CPU_BUILD_DIR)/build/installer/tickerscrape.tgz

  build/$(CPU_BUILD_DIR)/build/installer/tickerscrape.tgz: build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX)
	@if [ ! -d build/$(CPU_BUILD_DIR)/build/installer ]; then mkdir -p build/$(CPU_BUILD_DIR)/build/installer; fi
	cd build/$(CPU_BUILD_DIR); tar cvfz tickerscrape.tgz bitmaps data libpython* README.md views bmp_source Format.py Main.py scrape widgets cursors lib TickerScrape; mv tickerscrape.tgz build/installer

  upload: installer update
	scp build/$(CPU_BUILD_DIR)/build/installer/tickerscrape.tgz bitdrib1@bitdribble.com:www/tickerscrape/downloads/tickerscrape-install-$(VERSION)-$(TARGET)-$(CPU).tgz
	scp build/update/$(UPDATE_TGT) bitdrib1@bitdribble.com:www/tickerscrape/downloads/
endif

exe: build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX)

build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX): *.py */*.py
	$(PYTHON) setup-cx-freeze.py build
	touch $@

update: build/update/tickerscrape-update-$(VERSION)-$(TARGET)-$(CPU).tgz

build/update/tickerscrape-update-$(VERSION)-$(TARGET)-$(CPU).tgz: *.py */*.py
	rm -rf build/update/*
	@if [ ! -d build/update/tmp ]; then mkdir -p build/update/tmp; fi
	cp -a agw bitmaps bmp_source cursors data LICENSE README.md scrape snippets src TickerScrape.py views widgets build/update/tmp
	@find build/update/tmp -name __pycache__ -exec rm -rf {} \; 2>/dev/null || exit 0
	cd build/update/tmp; tar cvfz ../tickerscrape-update-$(VERSION)-$(TARGET)-$(CPU).tgz .

clean:
	rm -rf build/$(CPU_BUILD_DIR) build/update

debug-dump:
	@echo HOSTNAME=$(HOSTNAME)
	@echo PYTHON=$(PYTHON)
	@echo CPU_BUILD_DIR=$(CPU_BUILD_DIR)
	@echo VERSION=$(VERSION)

.SUFFIXES:
