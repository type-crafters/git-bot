from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('msg'),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

def use_markdown(filename, **context):
    template = env.get_or_select_template(filename)
    return template.render(**context)