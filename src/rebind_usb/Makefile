DIRNAME := $(shell basename $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))

INSTALL_SUBDIR ?= $(INSTALL_DIR)/usr/bin
.phony: all clean 
all: $(INSTALL_SUBDIR)/$(DIRNAME) 

$(INSTALL_SUBDIR)/$(DIRNAME): $(DIRNAME)   
	cp $< $@ 

clean: 
	rm -rf $(INSTALL_SUBDIR)/$(DIRNAME) 

