# test_invoke_http.py
from invokes import invoke_http

# invoke shipping_record microservice to get all shipping_records
results = invoke_http("http://localhost:5000/shippingrecord", method='GET')

print( type(results) )
print()
print( results )
