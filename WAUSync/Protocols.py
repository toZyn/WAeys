"""Port of src/WAUSync/Protocols/ — USync query protocols."""

from __future__ import annotations

from ..WABinary.generic_utils import assert_node_error_free, get_binary_node_child, get_binary_node_children, get_binary_node_child_string
from ..WABinary.types import BinaryNode


def _node(tag, attrs=None, content=None):
    return BinaryNode(tag=tag, attrs=attrs or {}, content=content)


class USyncContactProtocol:
    name = 'contact'

    def get_query_element(self):
        return _node('contact')

    def get_user_element(self, user):
        if user.phone:
            return _node('contact', content=user.phone)
        if user.username:
            attrs = {'username': user.username}
            if user.usernameKey:
                attrs['pin'] = user.usernameKey
            if user.lid:
                attrs['lid'] = user.lid
            return _node('contact', attrs)
        if user.type:
            return _node('contact', {'type': user.type})
        return _node('contact')

    def parser(self, node):
        if node.tag == 'contact':
            assert_node_error_free(node)
            return node.attrs.get('type') == 'in'
        return False


class USyncDeviceProtocol:
    name = 'devices'

    def get_query_element(self):
        return _node('devices', {'version': '2'})

    def get_user_element(self, user=None):
        return None

    def parser(self, node):
        device_list = []
        key_index = None

        if node.tag == 'devices':
            assert_node_error_free(node)
            device_list_node = get_binary_node_child(node, 'device-list')
            key_index_node = get_binary_node_child(node, 'key-index-list')

            if isinstance(device_list_node.content, list):
                for child in device_list_node.content:
                    if child.tag == 'device':
                        attrs = child.attrs
                        device_list.append({
                            'id': int(attrs.get('id')),
                            'keyIndex': int(attrs.get('key-index')),
                            'isHosted': bool(attrs.get('is_hosted') and attrs['is_hosted'] == 'true'),
                        })

            if key_index_node and key_index_node.tag == 'key-index-list':
                key_index = {
                    'timestamp': int(key_index_node.attrs.get('ts')),
                    'signedKeyIndex': key_index_node.content,
                    'expectedTimestamp': (
                        int(key_index_node.attrs['expected_ts'])
                        if key_index_node.attrs.get('expected_ts')
                        else None
                    ),
                }

        return {'deviceList': device_list, 'keyIndex': key_index}


class USyncStatusProtocol:
    name = 'status'

    def get_query_element(self):
        return _node('status')

    def get_user_element(self, user=None):
        return None

    def parser(self, node):
        if node.tag == 'status':
            assert_node_error_free(node)
            content = node.content
            status = content.decode('utf-8') if isinstance(content, bytes) else (content or None)
            set_at = None
            t = node.attrs.get('t')
            if t is not None:
                from datetime import datetime, timezone

                set_at = datetime.fromtimestamp(int(t), tz=timezone.utc)
            if status is None:
                code = node.attrs.get('code')
                if code and int(code) == 401:
                    status = ''
                else:
                    status = None
            elif isinstance(status, str) and len(status) == 0:
                status = None
            return {'status': status, 'setAt': set_at}
        return None


class USyncDisappearingModeProtocol:
    name = 'disappearing_mode'

    def get_query_element(self):
        return _node('disappearing_mode')

    def get_user_element(self, user=None):
        return None

    def parser(self, node):
        if node.tag == 'disappearing_mode':
            assert_node_error_free(node)
            duration = int(node.attrs.get('duration'))
            set_at = None
            t = node.attrs.get('t')
            if t is not None:
                from datetime import datetime, timezone

                set_at = datetime.fromtimestamp(int(t), tz=timezone.utc)
            return {'duration': duration, 'setAt': set_at}
        return None


class USyncUsernameProtocol:
    name = 'username'

    def get_query_element(self):
        return _node('username')

    def get_user_element(self, user=None):
        return None

    def parser(self, node):
        if node.tag == 'username':
            assert_node_error_free(node)
            return node.content if isinstance(node.content, str) else None
        return None


class USyncLIDProtocol:
    name = 'lid'

    def get_query_element(self):
        return _node('lid')

    def get_user_element(self, user):
        if user.lid:
            return _node('lid', {'jid': user.lid})
        return None

    def parser(self, node):
        if node.tag == 'lid':
            return node.attrs.get('val')
        return None


class USyncBotProfileProtocol:
    name = 'bot'

    def get_query_element(self):
        return _node('bot', content=[_node('profile', {'v': '1'})])

    def get_user_element(self, user):
        return _node('bot', content=[_node('profile', {'persona_id': user.personaId})])

    def parser(self, node):
        bot_node = get_binary_node_child(node, 'bot')
        profile = get_binary_node_child(bot_node, 'profile')

        commands_node = get_binary_node_child(profile, 'commands')
        prompts_node = get_binary_node_child(profile, 'prompts')

        commands = []
        prompts = []

        for command in get_binary_node_children(commands_node, 'command'):
            commands.append({
                'name': get_binary_node_child_string(command, 'name'),
                'description': get_binary_node_child_string(command, 'description'),
            })

        for prompt in get_binary_node_children(prompts_node, 'prompt'):
            prompts.append(f"{get_binary_node_child_string(prompt, 'emoji')} {get_binary_node_child_string(prompt, 'text')}")

        return {
            'isDefault': bool(get_binary_node_child(profile, 'default')),
            'jid': node.attrs.get('jid'),
            'name': get_binary_node_child_string(profile, 'name'),
            'attributes': get_binary_node_child_string(profile, 'attributes'),
            'description': get_binary_node_child_string(profile, 'description'),
            'category': get_binary_node_child_string(profile, 'category'),
            'personaId': profile.attrs.get('persona_id') if profile else None,
            'commandsDescription': get_binary_node_child_string(commands_node, 'description'),
            'commands': commands,
            'prompts': prompts,
        }
