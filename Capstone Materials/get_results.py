import boto3
import xmltodict
import os.path
import io
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload

def check_code(workerId, num):
    #MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

    mturk = boto3.client('mturk', aws_access_key_id = "****",
            aws_secret_access_key = "****"
            region_name='us-east-1', 
           # endpoint_url = MTURK_SANDBOX
            )

    # Use the hit_id previously created
    hit_id = '3WA2XVDZFTW00A6LSGV0T36SFAZ6ET'

    worker_results = mturk.list_assignments_for_hit(HITId=hit_id)

#AssignmentStatuses=['Submitted']
    if worker_results['NumResults'] > 0:
        count_loop = 0
        for assignment in worker_results['Assignments']:
            
            #correct completion code
            correctCode = "snapQ$image$basket"

            #get worker id that is in turk
            result_worker_id = assignment['WorkerId']

            #check if worker id is accounted for (in google spreadsheet AND mturk)
            if(result_worker_id == workerId):
                xml_doc = xmltodict.parse(assignment['Answer'])
                
                print("Worker's answer was:")
                if type(xml_doc['QuestionFormAnswers']['Answer']) is list:

                    # Multiple fields in HIT layout
                    for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
                        print("For input field: " + answer_field['QuestionIdentifier'])
                        print("Submitted answer: " + answer_field['FreeText'])
                else:
                    
                    # One field found in HIT layout
                    #print("For input field: " + xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier'])
                  #  print("Worker %s Submitted answer: " + xml_doc['QuestionFormAnswers']['Answer']['FreeText'] %(workerId))
                    code = xml_doc['QuestionFormAnswers']['Answer']['FreeText']

                    #approve if worker id is counted for in mturk/google forms and correct completion code
                    if(code == correctCode):

                        #approve assignment with feedback
                       # response = mturk.approve_assignment(
                         #   AssignmentId= assignment['AssignmentId'],
                          ##  RequesterFeedback= 'Your HIT has been approved. Thank you! Watch out for more assignments!'
                          #  )
                       # print("WorkerId %s response approved." %(workerId))

                        #send bonus if worker did optional third image upload
                        if(num == 1):
                            response = mturk.send_bonus(
                                WorkerId= workerId,
                                BonusAmount= '0.30',
                                AssignmentId= assignment['AssignmentId'],
                                Reason= 'You uploaded an additional image for a bonus.',
                                #UniqueRequestToken='string'
                            )
                            print("WorkerId %s bonus sent." %(workerId))

                        #qualification for image uploader
                        response = mturk.associate_qualification_with_worker(
                            QualificationTypeId='3EH281KFZNIIBPM0LCQ67OHZNRO0CH',
                            WorkerId= workerId,
                            IntegerValue=123,
                            SendNotification=False
                        )

                        #qualification for laundry 
                        response = mturk.associate_qualification_with_worker(
                            QualificationTypeId='3KNFVBDQHROUYPQHSJF5ELD5HEB30M',
                            WorkerId= workerId,
                            IntegerValue=123,
                            SendNotification=False
                        )

                    #deny if worker id is counted for, but incorrect completion code
                    else:
                        print("Please review %s response. Wrong completion code" %(workerId))
                         #response = mturk.reject_assignment(
                          #  AssignmentId= hit_id,
                            #RequesterFeedback= 'The completion code was not valid.'
                             #             'Without a valid completion code from the survey, there'
                              #            'is no way to verify. Please make sure to follow instructions in form if'
                              #            'you attempt this next time.')

                        #Block person from future hits for cheating     
                        response = mturk.create_worker_block(
                            WorkerId= workerId,
                            Reason= 'Used incorrect completion code. Was cheating'
                        )
                        
            else:

                #increment to find out if worker id is in the mturk responses
                count_loop = count_loop + 1
        
        #deny if worker id was never found in mturk responses to hit
        if(count_loop == worker_results['NumResults']):
            print("Please review %s response. ID not found in mturk." %(workerId))
    
    #No results for the hit are available
    else:
        print("No results ready yet")

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
def main():

    #'https://www.googleapis.com/auth/drive.metadata.readonly
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/mnt/c/Users/shayl/OneDrive/Desktop/CIS467/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

            #id of the google spreadsheet, get file and make .csv in project
            if(item['id'] == '1d4v3vf0RgWpox8d1YLtmh5W4H1THACA2gcNQuKNMEPU'):
                file_id = item['id']
                request = service.files().export_media(fileId=file_id,
                                                       mimeType='text/csv')
                fh = io.FileIO(item['name'] + '.csv', mode='wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print ("Download %d%%." % int(status.progress() * 100))
                break

    #opening csv file and parsing             
    with open('Laundry Basket Images (Responses).csv', mode='r') as csv_file:   
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print('\tWorker ID is: %s' %(row[5]))

                #check for bonus image 0 for no, 1 for yes. 4th column (index 3) holds optional third image on spreadsheet
                if(len(row[3]) == 0):
                   check_code(row[5], 0) 
                else:
                    check_code(row[5], 1)
                
                line_count += 1
   
if __name__ == '__main__':
    main()