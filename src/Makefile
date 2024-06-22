# Define the build destination variable (relative to the top-level directory)
INSTALL_DIR ?=usr/bin 

# Get the list of subdirectories
SUBDIRS := $(shell find . -maxdepth 1 -mindepth 1 -type d -exec test -e {}/Makefile \; -print)

.PHONY: all $(SUBDIRS)

# Default target
all: $(SUBDIRS)

# Target for each subdirectory
$(SUBDIRS):
	$(MAKE) -C $@ INSTALL_DIR=$(abspath $(INSTALL_DIR))

print-subdirs:
	@echo $(SUBDIRS)
