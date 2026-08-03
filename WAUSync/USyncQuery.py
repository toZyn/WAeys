"""Port of src/WAUSync/USyncQuery.ts."""

from __future__ import annotations

from ..WABinary.generic_utils import get_binary_node_child
from ..WABinary.types import BinaryNode
from .Protocols import (
    USyncBotProfileProtocol,
    USyncContactProtocol,
    USyncDeviceProtocol,
    USyncDisappearingModeProtocol,
    USyncLIDProtocol,
    USyncStatusProtocol,
    USyncUsernameProtocol,
)


class USyncQuery:
    def __init__(self):
        self.protocols = []
        self.users = []
        self.context = 'interactive'
        self.mode = 'query'

    def with_mode(self, mode):
        self.mode = mode
        return self

    def with_context(self, context):
        self.context = context
        return self

    def with_user(self, user):
        self.users.append(user)
        return self

    def parse_usync_query_result(self, result):
        if not result or result.attrs.get('type') != 'result':
            return None

        protocol_map = {protocol.name: protocol.parser for protocol in self.protocols}

        query_result = {'list': [], 'sideList': []}

        usync_node = get_binary_node_child(result, 'usync')
        list_node = get_binary_node_child(usync_node, 'list') if usync_node else None

        if list_node and isinstance(list_node.content, list):
            items = []
            for node in list_node.content:
                jid = node.attrs.get('jid')
                if jid:
                    data = {}
                    if isinstance(node.content, list):
                        for content in node.content:
                            protocol = content.tag
                            parser = protocol_map.get(protocol)
                            if parser:
                                data[protocol] = parser(content)
                    items.append({**data, 'id': jid})
            query_result['list'] = items

        return query_result

    def with_device_protocol(self):
        self.protocols.append(USyncDeviceProtocol())
        return self

    def with_contact_protocol(self):
        self.protocols.append(USyncContactProtocol())
        return self

    def with_status_protocol(self):
        self.protocols.append(USyncStatusProtocol())
        return self

    def with_disappearing_mode_protocol(self):
        self.protocols.append(USyncDisappearingModeProtocol())
        return self

    def with_bot_profile_protocol(self):
        self.protocols.append(USyncBotProfileProtocol())
        return self

    def with_lid_protocol(self):
        self.protocols.append(USyncLIDProtocol())
        return self

    def with_username_protocol(self):
        self.protocols.append(USyncUsernameProtocol())
        return self
