import boto3
import sys
import getopt

# Globals
BucketName = ''
ProfileName = 'default'
NewACL = 'authenticated-read'

# Parse CL opts
opts, args = getopt.getopt(sys.argv[1:],'hb:p:a:')
for opt, arg in opts:
    if opt == '-h':
        print '-b bucketname'
        print '-p profile name'
        print '-a ACL (authenticated-read)'
        sys.exit(0)
    if opt == '-b':
        BucketName = str(arg)
    if opt == '-p':
        ProfileName = str(arg)
    if opt == '-a':
        NewACL = str(arg)

# Get applicable creds
mySession = boto3.Session(profile_name=ProfileName)

# Get all the objects
allS3Keys = []
s3Client = mySession.client('s3')
nextToken = 1
while nextToken is not None:
    allObjects = None
    if nextToken == 1:
        allObjects = s3Client.list_objects_v2(Bucket=BucketName)
    else:
        allObjects = s3Client.list_objects_v2(Bucket=BucketName,ContinuationToken=nextToken)
    if allObjects.get('IsTruncated') == True:
        nextToken = allObjects.get('NextContinuationToken')
    else:
        nextToken = None

    for i in allObjects['Contents']:
        allS3Keys.append(str(i['Key']))

# Now set the ACL for each object
for key in allS3Keys:
    s3Client.put_object_acl(ACL=NewACL,Bucket=BucketName,Key=key)
