
upload-schemas:
	env IVCAP_URL=$(shell ivcap context get url) \
		IVCAP_JWT=$(shell ivcap context get access-token --refresh-token) \
		IVCAP_ACCOUNT_ID=$(shell ivcap context get account-id) \
	python common_schemas.py
