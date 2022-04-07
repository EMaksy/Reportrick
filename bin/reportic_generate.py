from fileinput import filename
import jinja2
import os
import weasyprint


PATH_TEMPLATE = "./template"
TEMPLATE_NAME = "layout_workreport.html"
PATH_CREATED_HTML = "workreport/jinja_workreport.html"
PATH__CREATED_PDF = "workreport/jinja_workreport.pdf"
CREATED_PDF_NAME = "test-jinja.pdf"
CREATED_HTML_NAME = "test-jinja.html"


jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(PATH_TEMPLATE))

jinja2_var = {
    'title': 'WORKREPORT'
}
template = jinja2_env.get_template(TEMPLATE_NAME)

# debug info
print(template.render(jinja2_var))


# creates file
myfile = open(
    PATH_CREATED_HTML, "w")
myfile.write(template.render(jinja2_var))
myfile.close()

print(oct(os.stat(PATH_CREATED_HTML).st_mode))
print(weasyprint.HTML(
    PATH_CREATED_HTML).write_pdf(PATH__CREATED_PDF))
doc_pdf = weasyprint.HTML(
    PATH_CREATED_HTML).write_pdf(PATH__CREATED_PDF)
