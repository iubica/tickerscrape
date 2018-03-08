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
  PYTHON=/cygdrive/c/Users/andrei/AppData/Local/Programs/Python/Python36/python.exe
  TARGET=windows
  CPU=x86
  CPU_BUILD_DIR=exe.win-amd64-3.6
endif

all: installer

upload: installer 
	scp build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe bitdrib1@bitdribble.com:www/tickerscrape/downloads/tickerscrape-$(VERSION)-$(TARGET)-$(CPU)-setup.exe

installer: build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe

build/$(CPU_BUILD_DIR)/build/installer/mysetup.exe: TickerScrape.py TickerScrape.iss
	$(PYTHON) setup.py build
	$(ISCC) build/$(CPU_BUILD_DIR)/TickerScrape.iss

clean:
	rm -rf build/$(CPU_BUILD_DIR)

debug-dump:
	@echo HOSTNAME=$(HOSTNAME)
	@echo PYTHON=$(PYTHON)
	@echo CPU_BUILD_DIR=$(CPU_BUILD_DIR)
	@echo VERSION=$(VERSION)
