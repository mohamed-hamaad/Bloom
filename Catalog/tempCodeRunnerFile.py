def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields)
        for field_name, field in self.fields.items():
            print(field_name, field.widget.attrs)
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-dark/20 focus:outline-none focus:border-dark text-sm tracking-wide bg-cream'
            })
            print(field.widget.attrs)