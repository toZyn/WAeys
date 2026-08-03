"""Port of src/WAUSync/USyncUser.ts."""


class USyncUser:
    def __init__(self):
        self.id = None
        self.lid = None
        self.phone = None
        self.username = None
        self.usernameKey = None
        self.type = None
        self.personaId = None

    def with_id(self, id_):
        self.id = id_
        return self

    def with_lid(self, lid):
        self.lid = lid
        return self

    def with_phone(self, phone):
        self.phone = phone
        return self

    def with_username(self, username):
        self.username = username
        return self

    def with_username_key(self, username_key):
        self.usernameKey = username_key
        return self

    def with_type(self, type_):
        self.type = type_
        return self

    def with_persona_id(self, persona_id):
        self.personaId = persona_id
        return self
