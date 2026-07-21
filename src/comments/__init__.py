def __init__(self, *args, user=None, **kwargs):
    super().__init__(*args, **kwargs)

    if user and user.is_authenticated:
        self.fields.pop("name")
        self.fields.pop("email")