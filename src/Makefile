# Define the build destination variable (relative to the top-level directory)
INSTALL_DIR ?= ../bin 

# Get the list of subdirectories
SUBDIRS := $(wildcard */)

.PHONY: all $(SUBDIRS)

# Default target
all: $(SUBDIRS)

# Target for each subdirectory
$(SUBDIRS):
	$(MAKE) -C $@ INSTALL_DIR=$(abspath $(INSTALL_DIR))

