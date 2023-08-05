# SalesForce Session Library
============================

# Overview

A python wrapper for [simple-salesforce](https://github.com/simple-salesforce/simple-salesforce).  The general purpose is to help build queries without having to write raw SQL. 

# Installation

## Pip Installation

`pip install SalesForceSession`

# Usage

[Get Your Session Token](https://help.salesforce.com/articleView?id=user_security_token.htm)

### Setting environment variables

```
export SF_USERNAME='your.sf.email@domain.com' 
export SF_PASSWORD='yoUrSalesfoRc3P4sSWORd!' 
export SF_SECURITY_TOKEN='YourUsersSecurityToken'
export SF_CLIENT_ID='SalesForceIDENTIFICATION' 
```

### Python Code

```
from salesforce_session import SalesForceSession

salesforce = SalesForceSession()

records = salesforce.query(
                query_type='SELECT',
                fields=['Status','Priority'],
                sql_objects='Case',
                conditions="Status='New'",
                limit=1
                )
```

The above method constructs the following statement:

`SELECT Status, Priority FROM Case WHERE Status='New' LIMIT 1`

This then excutes the `simple_salesforce.query_all()` method, converts the results to json and returns that object.

# License

MIT License
