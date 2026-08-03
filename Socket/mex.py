"""Port of src/Socket/mex.ts — executeWMexQuery (GraphQL over WAM binary)."""

from __future__ import annotations

import asyncio
import json

from ..WABinary.generic_utils import get_binary_node_child
from ..WABinary.jid_utils import S_WHATSAPP_NET
from ..WABinary.types import BinaryNode
from ..Utils.generics import Boom


def w_mex_query(variables: dict, query_id: str, query, generate_message_tag):
    return query(BinaryNode(tag='iq', attrs={
        'id': generate_message_tag(),
        'type': 'get',
        'to': S_WHATSAPP_NET,
        'xmlns': 'w:mex',
    }, content=[
        BinaryNode(tag='query', attrs={'query_id': query_id},
                   content=json.dumps({'variables': variables}).encode('utf-8')),
    ]))


async def execute_wmex_query(variables: dict, query_id: str, data_path: str, query, generate_message_tag):
    result = w_mex_query(variables, query_id, query, generate_message_tag)
    if asyncio.iscoroutine(result):
        result = await result
    child = get_binary_node_child(result, 'result')
    if child is not None and child.content is not None:
        content = child.content
        data = json.loads(content.decode('utf-8') if isinstance(content, bytes) else str(content))

        errors = data.get('errors') or []
        if errors:
            error_messages = ', '.join(err.get('message') or 'Unknown error' for err in errors)
            first_error = errors[0]
            error_code = ((first_error.get('extensions') or {}).get('error_code')) or 400
            raise Boom(f'GraphQL server error: {error_messages}', status_code=error_code, data=first_error)

        response = data.get('data', {}).get(data_path) if data_path else data.get('data')
        if response is not None:
            return response

    action = data_path[5:].replace('_', ' ') if (data_path or '').startswith('xwa2_') else (data_path or '').replace('_', ' ')
    raise Boom(f'Failed to {action}, unexpected response structure.', status_code=400, data=result)
