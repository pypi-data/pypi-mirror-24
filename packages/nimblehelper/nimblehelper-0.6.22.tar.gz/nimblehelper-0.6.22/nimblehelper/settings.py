# Nimble Gateway Url to make requests to
SIEBEL_GATEWAY_URL = "http://authenticationservice:8000/siebel/siebelrequest/"
KONG_ADMIN_URL = "http://kong:8001/"

# Response Messages
SUCCESSFUL = "Operation successful"
INTERNAL_SERVER_ERROR = "An error has occured, please try again later"
INVALID_INPUT = "You have not specified all the inputs or the format of some of the input is wrong"
INVALID_AUTHORIZATION = "You do not have the permission to make this call"

# List of codes that Nimble Helper supports
CODE_LIST = [200, 201, 400, 401, 403, 500]
SUCCESS_CODES = [200, 201]

