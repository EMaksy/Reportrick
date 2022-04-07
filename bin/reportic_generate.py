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


def generade_html_and_pdf(red_list, amber_list, green_list, meeting_list):
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(PATH_TEMPLATE))

    red_list, amber_list, green_list, meeting_list = ["Testen", "WESTEN", "Fisten"], [
        "Testen", "WESTEN", "Fisten"], [
        "Testen", "WESTEN", "Fisten"], [
        "Testen", "WESTEN", "Fisten"]
    jinja2_var = {
        'title': 'WORKREPORT',
        'red_entries': red_list,
        'amber_entries': amber_list,
        'green_entries': green_list,
        'meeting_entries': meeting_list,
        'user_data': ["Eugen", "Maksymenko", "Team"],
        'time_data': ["Date", "CALENDERWEEK"]
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


red_list, amber_list, green_list, meeting_list = [
    "Testen", "WESTEN", "Fisten", "ewgjowe"]
generade_html_and_pdf(red_list, amber_list, green_list, meeting_list)
