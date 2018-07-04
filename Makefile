# makefile

PROJECT = antlexa
VIRTUAL_ENV = env
FUNCTION_NAME = alexaskill
FUNCTION_HANDLER = lambda_handler
AWS_REGION = us-east-1
LAMBDA_ROLE = "arn"

install: virtual
build: clean_package build_package_tmp copy_python remove_unused zip

virtual:
	@echo "setup and activate virtualenv"
	if test ! -d "$(VIRTUAL_ENV)"; then \
		pip install virtualenv; \
		virtualenv $(VIRTUAL_ENV); \
	fi 
	@echo ""

clean_package:
	rm -rf ./package/*

build_package_tmp:
	mkdir -p ./package/tmp/lib
	cp -a ./$(PROJECT)/. ./package/tmp/   	
 
copy_python:
	if test -d $(VIRTUAL_ENV)/lib; then \
		cp -a $(VIRTUAL_ENV)/lib/python2.7/site-packages/. ./package/tmp/; \
	fi 
	# 64 bit
	if test -d $(VIRTUAL_ENV)/lib64; then \
		cp -a $(VIRTUAL_ENV)/lib64/python2.7/site-packages/. ./package/tmp/; \
	fi

remove_unused:
	rm -rf ./package/tmp/wheel*
	rm -rf ./package/tmp/easy-install*
	
zip:
	cd ./package/tmp && zip -r ../$(PROJECT).zip .


 




























