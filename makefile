# Makefile for the tickerscrape project
HOSTNAME=$(shell hostname)
PYTHON=python
ISCC=iscc
VERSION=$(shell python version.py)

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

ifeq ($(HOSTNAME),Darias-Air)
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

all: installer

installer: exe

upload: installer 
	chmod 755 build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe
	scp build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe bitdrib1@bitdribble.com:www/tickerscrape/downloads/tickerscrape-$(VERSION)-$(TARGET)-$(CPU)-setup.exe

ifeq ($(TARGET),windows)
installer: build/$(CPU_BUILD_DIR)/build/installer/mysetup$(EXE_SUFFIX)
else
installer:
endif

exe: build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX)

build/$(CPU_BUILD_DIR)/TickerScrape$(EXE_SUFFIX):
	$(PYTHON) setup.py build

build/$(CPU_BUILD_DIR)/build/installer/mysetup$(EXE_SUFFIX): exe TickerScrape.iss
	$(ISCC) build/$(CPU_BUILD_DIR)/TickerScrape.iss

clean:
	rm -rf build/$(CPU_BUILD_DIR)

debug-dump:
	@echo HOSTNAME=$(HOSTNAME)
	@echo PYTHON=$(PYTHON)
	@echo CPU_BUILD_DIR=$(CPU_BUILD_DIR)
	@echo VERSION=$(VERSION)
