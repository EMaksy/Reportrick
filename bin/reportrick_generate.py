from fileinput import filename
import jinja2
import os
import weasyprint


PATH_TEMPLATE = "./template"
TEMPLATE_NAME = "layout_workreport.html"
PATH_CREATED_HTML = "work_report/jinja_workreport.html"
PATH_CREATED_PDF = "work_report/jinja_workreport.pdf"
CREATED_PDF_NAME = "test-jinja.pdf"
CREATED_HTML_NAME = "test-jinja.html"


def generate_html_and_pdf(meeting_list, green_list, amber_list, red_list, team_data, user_data, time_data):
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(PATH_TEMPLATE))

    jinja2_var = {
        'title': 'WORKREPORT',
        'red_entries': red_list,
        'amber_entries': amber_list,
        'green_entries': green_list,
        'meeting_entries': meeting_list,
        'user_data': user_data,
        'team_data': team_data,
        'time_data': time_data
    }

    template = jinja2_env.get_template(TEMPLATE_NAME)

    # creates html file
    myfile = open(
        PATH_CREATED_HTML, "w")
    myfile.write(template.render(jinja2_var))
    myfile.close()
    # create pdf
    weasyprint.HTML(PATH_CREATED_HTML).write_pdf(PATH_CREATED_PDF)
    print(
        f"File created at:\nHTML: {PATH_CREATED_HTML}\nPDF:  {PATH_CREATED_PDF}\n")


def generate_html(meeting_list, green_list, amber_list, red_list, team_data, user_data, time_data):
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(PATH_TEMPLATE))

    jinja2_var = {
        'title': 'WORKREPORT',
        'red_entries': red_list,
        'amber_entries': amber_list,
        'green_entries': green_list,
        'meeting_entries': meeting_list,
        'user_data': user_data,
        'team_data': team_data,
        'time_data': time_data
    }

    template = jinja2_env.get_template(TEMPLATE_NAME)
    myfile = open(
        PATH_CREATED_HTML, "w")
    myfile.write(template.render(jinja2_var))
    myfile.close()
    print(f"File created at:\nHTML: {PATH_CREATED_HTML}")


def generate_pdf(meeting_list, green_list, amber_list, red_list, team_data, user_data, time_data):
    jinja2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(PATH_TEMPLATE))

    jinja2_var = {
        'title': 'WORKREPORT',
        'red_entries': red_list,
        'amber_entries': amber_list,
        'green_entries': green_list,
        'meeting_entries': meeting_list,
        'user_data': user_data,
        'team_data': team_data,
        'time_data': time_data
    }

    template = jinja2_env.get_template(TEMPLATE_NAME)
    # creates file
    myfile = open(
        PATH_CREATED_HTML, "w")
    myfile.write(template.render(jinja2_var))
    myfile.close()

    weasyprint.HTML(
        PATH_CREATED_HTML).write_pdf(PATH_CREATED_PDF)
    os.remove(PATH_CREATED_HTML)
    print(f"File created at:\nPDF:  {PATH_CREATED_PDF}")


#user_data = ""
#time_data = ""
# red_list, amber_list, green_list, meeting_list = [
#    "Testen", "WESTEN", "Fisten", "ewgjowe"]
# generade_html_and_pdf(red_list, amber_list, green_list, meeting_list)
# generate_pdf(red_list, amber_list, green_list,
#             meeting_list, user_data, time_data)

# generate_html(red_list, amber_list, green_list,
 #             meeting_list, user_data, time_data)
