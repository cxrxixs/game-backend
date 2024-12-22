from django.http import HttpRequest, HttpResponse
from django.template import Context, Template


def home_page(request: HttpRequest):
    template = Template(
        """
        <!DOCTYPE html>
        <html lang='en'>
        <head>
        <meta charset='utf-8'>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
        <title>{% block title %} {{ title }} {% endblock %}</title>
        </head>
        <body>
        <div class="container">
        <h1 class="text-center"><i><color=blue>Hello</color></i> Smartnonsense</h1>
        </div>
        </body>
        """
    )
    context = Context({
        "title": "home page",
    })

    response_content = template.render(context)

    return HttpResponse(
        content=response_content.encode("utf-8"),
        content_type="text/html",
    )
