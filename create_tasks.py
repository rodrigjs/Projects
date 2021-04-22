import boto3
import os
import xmltodict
import json

#MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
# credentials_file = os.path.join(os.path.dirname(os.getcwd()), 'credentials.json')
# with open(credentials_file, 'r') as f:
#     creds = json.load(f)
# iam_user = creds['aws']['iam_users'][0]
# access_key = iam_user['access-key-ID']
# secret = iam_user['secret-access-key']

mturk = boto3.client('mturk', aws_access_key_id = "AKIATJOYNCC73I4WQLIS",
        aws_secret_access_key = "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",
        region_name='us-east-1', 
        #endpoint_url = MTURK_SANDBOX
        )

print (mturk.get_account_balance() ['AvailableBalance'])

question = open(name='questions.xml',mode='r').read()
new_hit = mturk.create_hit(
    Title = 'Image Upload of Laundry Basket',
    Description = 'Upload two images: one image must contain your laundry basket in your home. ' + 
                'Submit one additional laundry basket image for a bonus. More information provided on the Google Form.'
                + ' Google account is required. Must use own photo taken with smartphone.',
    Keywords = 'survey, laundry, images',
    Reward = '0.60',
    MaxAssignments = 40,
    LifetimeInSeconds = 172800,
    AssignmentDurationInSeconds = 600,
    AutoApprovalDelayInSeconds = 259200,
    Question = question,
)

print "A new HIT has been created."
#print "https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId']
print "HITGroupID = " + new_hit['HIT']['HITGroupId']
print "HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)"
