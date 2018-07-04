# makefile

PROJECT = unique_identifier
VIRTUAL_ENV = env
FUNCTION_NAME = alexaskill
FUNCTION_HANDLER = lambda_handler
AWS_REGION = us-east-1
LAMBDA_ROLE = "arn"

install: virtual

virtual: 
 @echo "setup and activate virtual environment"
    if test ! -d "$(VIRTUAL_ENV)"; then \
        pip install virtualenv; \ 
	virtualenv $(VIRTUAL_ENV); \
    fi
    @echo ""

build_package_tmp:
    mkdir -p ./package/tmp/lib
    cp -a ./$(PROJECT)/. ./package/tmp/
    
copy_python:
 
