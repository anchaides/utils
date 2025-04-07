DIRNAME := $(shell basename $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))

.phony: all clean 
all: input_forwarder 

$(INSTALL_DIR)/usr/bin/input_forwarder: input_forwarder.py   
	mkdir -p $(INSTALL_DIR)/usr/bin
	mkdir -p $(INSTALL_DIR)/usr/lib/systemd/user/ 
	cp input-forwarder.service $(INSTALL_DIR)/usr/lib/systemd/user/
	cp $< $@ 

clean: 
	rm -rf $(INSTALL_SUBDIR)/$(DIRNAME) 

