from django.forms.widgets import Input


class CustomImageWidget(Input):
    template_name = "image_input.html"
    input_type = 'file'
    needs_multipart_form = True

    def format_value(self, value):
        return value

    def value_from_datadict(self, data, files, name):
        return files.get(name)

    def value_omitted_from_data(self, data, files, name):
        return name not in files

    def use_required_attribute(self, initial):
        return super().use_required_attribute(initial) and not initial
    