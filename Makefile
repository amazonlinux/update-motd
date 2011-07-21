# -*- Makefile -*-
# Makefile for source package: update-motd
#
# Module created by 'ajorgens' on 2011-07-21

NAME	:= update-motd
VENDOR	:= GOBI

define find-makefile-common
$(firstword $(foreach d,. common ../common,$(if $(wildcard $(d)/Makefile.common),$(d)/Makefile.common)))
endef

include $(find-makefile-common)

ifeq ($(find-makefile-common),)
define get_common_url
$(shell git remote show -n origin | sed -re '/fetch\s+url/I!d;s,^.+\b(\w+://\S+)/[^/]+$$,\1/common.git,')
endef

common :
	git clone $(get_common_url) $@

sources :: common
	$(MAKE) $@
endif
