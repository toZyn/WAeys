"""Port of src/Utils/offline-node-processor.ts — offline stanza node processing."""

from __future__ import annotations

import asyncio
from typing import Callable, Dict

from ..WABinary.types import BinaryNode

MessageType = str  # 'message' | 'call' | 'receipt' | 'notification'


def make_offline_node_processor(
    node_processor_map: Dict[str, Callable[[BinaryNode], object]],
    deps: dict,
    batch_size: int = 10,
) -> dict:
    """Creates a processor for offline stanza nodes that:
    - Queues nodes for sequential processing
    - Yields to the event loop periodically to avoid blocking
    - Catches handler errors to prevent the processing loop from crashing
    """
    nodes = []
    is_processing = False

    def enqueue(type_: MessageType, node: BinaryNode):
        nonlocal is_processing
        nodes.append({'type': type_, 'node': node})

        if is_processing:
            return

        is_processing = True

        async def run():
            nonlocal is_processing
            processed_in_batch = 0
            try:
                while len(nodes) and deps['isWsOpen']():
                    item = nodes.pop(0)
                    type_ = item['type']
                    node = item['node']

                    node_processor = node_processor_map.get(type_)

                    if node_processor is None:
                        deps['onUnexpectedError'](Exception(f'unknown offline node type: {type_}'), 'processing offline node')
                        continue

                    try:
                        result = node_processor(node)
                        if asyncio.iscoroutine(result):
                            await result
                    except Exception as err:
                        deps['onUnexpectedError'](err, f'processing offline {type_}')
                    processed_in_batch += 1

                    # Yield to event loop after processing a batch
                    # This prevents blocking the event loop for too long when there are many offline nodes
                    if processed_in_batch >= batch_size:
                        processed_in_batch = 0
                        await deps['yieldToEventLoop']()
            finally:
                is_processing = False

        asyncio.ensure_future(run()).add_done_callback(
            lambda fut: (
                None if not fut.exception() else deps['onUnexpectedError'](fut.exception(), 'processing offline nodes')
            )
        )

    return {'enqueue': enqueue}
