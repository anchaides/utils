DIRNAME := $(shell basename $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))

.phony: all clean 
all: $(INSTALL_DIR)/$(DIRNAME) 

$(INSTALL_DIR)/$(DIRNAME): $(DIRNAME)   
	cp $< $@ 

clean: 
	rm -rf $(INSTALL_DIR)/$(DIRNAME) 

