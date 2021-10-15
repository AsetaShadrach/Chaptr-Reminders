from GMAIL import ChaptrGmail
from SHEETS import ChaptrSheets

# ---- ALTER THESE ----

course_sheet_name = 'Python Programming'
project_name = "PYTHON WEEK ONE PRACTICE"  
date_to_check_from = '9/18/2021'  # Month/Day/Year 

# -----  ----- ----- -----


# Make sure all sheets folow the same format for the following 2 lines to work
student_names_col = course_sheet_name+'!A:A'
student_emails_col = course_sheet_name+'!B:B'


sheets_params = {    
    'course_sheet_name' : course_sheet_name,
    'project_name' : project_name , 
    'date_to_check_from' : date_to_check_from , 
    
    'range_names'  : ['Project Submissions!A:A',
                      'Project Submissions!D:D',
                      'Project Submissions!G:G',
                      student_names_col,
                      student_emails_col            
                     ] 
    
        } 


gmail_params = {
    'sender_email': 'me',
    'assignment_name': 'PYTHON WEEK ONE PRACTICE',
    'link_to_assignment': 'https://tinyurl.com/yvfuew6v'
}


if __name__ == '__main__':
    sheet =  ChaptrSheets(sheets_params)
    gmail = ChaptrGmail(gmail_params)

    df = sheet.incomplete_assignments()
    gmail.gmail_main(df)


