PROJECT = changemonitor
FUNCTION?= $(PROJECT)
REGION = us-east-1
PAYLOAD?='{"key1":"value1", "key2":"value2", "key3":"value3"}'
ROLE=$(shell aws iam get-role --role-name $(PROJECT) --query 'Role.Arn' | tr -d '"')
all: build
build: clean
	mkdir build
	pip install -t build/ .
	pip install -t build/ -r requirements.txt 
	cd build; zip -r ../$(FUNCTION).zip .; cd ..
clean:
	rm -rf build/
destroy:
	aws lambda delete-function --function-name $(FUNCTION)
deploy: build
	aws lambda create-function \
    --region $(REGION) \
    --function-name $(FUNCTION) \
    --zip-file fileb://$(FUNCTION).zip \
    --role $(ROLE) \
    --handler "$(PROJECT)"_lambda.handler \
    --runtime python2.7 \
    --timeout 15 \
    --memory-size 128
create_role:
	aws iam create-role --role-name $(PROJECT) --assume-role-policy-document file://role_trust.json
	aws iam put-role-policy --role-name $(PROJECT) --policy-name $(PROJECT)-permissions --policy-document file://role_permissions.json
update_role:
	aws iam put-role-policy --role-name $(PROJECT) --policy-name $(PROJECT)-permissions --policy-document file://role_permissions.json
invoke:
	aws lambda invoke \
    --invocation-type RequestResponse \
    --function-name $(FUNCTION) \
    --region $(REGION) \
    --log-type Tail \
    --payload $(PAYLOAD) outputfile.txt
