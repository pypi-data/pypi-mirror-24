# AWS Gateway Client
===================

# Overview


# Installation

With pip

```
pip install apigateway_client
```

GitHub

```
git clone git@github.com:iamjohnnym/apigateway_client.git
```

# Usage

```
from apigateway_client import Client

api_client = Client(
    api_gateway_id="gateway_id",
    region="us-east-1",
    stage='develop',
    endpoint_key='pets',
    account_id='acccount-id',
    role='role_name',
    role_session_name='unittest'
    )

response = api_cliet.get(endpoint_meta='pet')
```