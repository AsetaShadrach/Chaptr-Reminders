from CreateService import CreateService
import pandas as pd


class ChaptrSheets():
    spreadsheet_id = '1dFt6Anilzcss2noYdwZS2kES_qg9bw2LZY2cMl56c5s'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 

    def __init__(self, params):
        self.params = params

    def get_sheet_data(self):
        RANGE_NAMES = self.params['range_names']

        service = CreateService('ChaptrSheetsSecret.json',
                                'chaptr_sheet_token.json',
                                'sheets', 
                                'v4', 
                                self.SCOPES)

        service = service.CreateApiService()

        result = service.spreadsheets().values().batchGet(spreadsheetId=self.spreadsheet_id,
                                        ranges=RANGE_NAMES , majorDimension='COLUMNS').execute()
        # Retrun our values 
        # The values will be in a list of dictionaries
        self.ranges = result.get('valueRanges', [])
    
        return 


    def incomplete_assignments(self):
        self.get_sheet_data()
        
        # Create dataframes from the ranges
        # One to holed submission data
        # The other to hold student data
        student_details = {'Name' : self.ranges[3]['values'][0][1:],
                        'Email': self.ranges[4]['values'][0][1:]}
        submission_details = {'TimePosted': self.ranges[0]['values'][0][1:],
                            'ProjectName':self.ranges[1]['values'][0][1:],
                            'Email': self.ranges[2]['values'][0][1:]}

        student_df = pd.DataFrame(student_details)
        submission_df = pd.DataFrame(submission_details)

        # convert submission Timestamp to datetime
        submission_df['TimePosted'] = pd.to_datetime(submission_df['TimePosted'])

        date_to_check_from = self.params['date_to_check_from']
        project_name = self.params['project_name']

        submission_df["ProjectName"] = submission_df["ProjectName"].apply(lambda x:x.lower())
        # Get the dataframe os students who have not submitted
        completed_projects = submission_df [ (submission_df.TimePosted > date_to_check_from)
                                            & (submission_df.ProjectName == project_name)]
        incomplete_projects = student_df[~student_df.Email.isin(completed_projects.Email)]

        return incomplete_projects

        
