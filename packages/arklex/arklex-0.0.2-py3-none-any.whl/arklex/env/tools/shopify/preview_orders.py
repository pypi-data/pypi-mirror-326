import json
from typing import Any, Dict

import shopify

from arklex.env.tools.tools import register_tool
from arklex.env.tools.shopify.utils import SHOPIFY_AUTH_ERROR

description = "Get the status and details of an order."
slots = [
    {
        "name": "order_ids",
        "type": "array",
        "items": {"type": "string"},
        "description": "The order id, such as gid://shopify/Order/1289503851427. If there is only 1 order, return in list with single item. If there are multiple order ids, please return all of them in a list.",
        "prompt": "Please provide the order id to get the details of the order.",
        "required": True,
    },
    {
        "name": "limit",
        "type": "int",
        "description": "Maximum number of products to show.",
        "prompt": "",
        "required": False
    }
]
outputs = [
    {
        "name": "order_details",
        "type": "dict",
        "description": "The order details of the order. such as '{\"id\": \"gid://shopify/Order/1289503851427\", \"name\": \"#1001\", \"totalPriceSet\": {\"presentmentMoney\": {\"amount\": \"10.00\"}}, \"lineItems\": {\"nodes\": [{\"id\": \"gid://shopify/LineItem/1289503851427\", \"title\": \"Product 1\", \"quantity\": 1, \"variant\": {\"id\": \"gid://shopify/ProductVariant/1289503851427\", \"product\": {\"id\": \"gid:////shopify/Product/1289503851427\"}}}]}}'.",
    }
]
ORDERS_NOT_FOUND = "error: order not found"
errors = [
    SHOPIFY_AUTH_ERROR,
    ORDERS_NOT_FOUND
]

@register_tool(description, slots, outputs, lambda x: x not in errors)
def preview_orders(order_ids: list, limit=10, **kwargs) -> str:
    limit = limit or 10
    
    shop_url = kwargs.get("shop_url")
    api_version = kwargs.get("api_version")
    token = kwargs.get("token")

    if not shop_url or not api_version or not token:
        return SHOPIFY_AUTH_ERROR
    
    try:
        ids = ' OR '.join(f'id:{oid.split("/")[-1]}' for oid in order_ids)
        with shopify.Session.temp(shop_url, api_version, token):
            response = shopify.GraphQL().execute(f"""
                {{
                    orders (query:"{ids}" first: {len(order_ids)}) {{
                        nodes {{
                            id
                            name
                            totalPriceSet {{
                                presentmentMoney {{
                                    amount
                                }}
                            }}
                            lineItems(first: {limit}) {{
                                nodes {{
                                    id
                                    title
                                    quantity
                                    variant {{
                                        id
                                        title
                                        quantity
                                        variant {{
                                            id
                                            product {{
                                                id
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            """)
        results = json.loads(response)["data"]["orders"]['nodes']
        return results
    except Exception as e:
        return ORDERS_NOT_FOUND
