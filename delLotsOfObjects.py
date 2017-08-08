import boto3
import sys
import getopt
import datetime
import pytz

# Globals
BucketName = ''
FolderName = ''
HowManyDays = None
ProfileName = 'default'
Env = 'us-east-1'
Delete = False

# Parse CL opts
opts, args = getopt.getopt(sys.argv[1:],'he:b:p:f:k:d')
for opt, arg in opts:
    if opt == '-h':
        print '-b bucketname'
        print '-f foldername'
        print '-k days to keep'
        print '-p profile name'
        print '-e region'
        sys.exit(0)
    if opt == '-e':
        Env = str(arg)
    if opt == '-p':
        ProfileName = str(arg)
    if opt == '-b':
        BucketName = str(arg)
    if opt == '-f':
        FolderName = str(arg)
    if opt == '-k':
        HowManyDays = str(arg)
    if opt == '-d':
        Delete = True

if HowManyDays is None or BucketName is None or ProfileName is None or Env is None:
    print 'Missing or invalid options'
    print '-b bucketname'
    print '-f foldername'
    print '-d days to keep'
    print '-p profile name'
    print '-e region'
    sys.exit(1)

# Get all the objects
allS3Keys = {}
s3Client = boto3.client('s3',
    profile_name=ProfileName,
    region_name=Env)
nextToken = 1
while nextToken is not None:
    allObjects = None
    if nextToken == 1:
        allObjects = s3Client.list_objects_v2(Bucket=BucketName,Prefix=FolderName)
    else:
        allObjects = s3Client.list_objects_v2(Bucket=BucketName,Prefix=FolderName,ContinuationToken=nextToken)
    if allObjects.get('IsTruncated') == True:
        nextToken = allObjects.get('NextContinuationToken')
    else:
        nextToken = None

    for i in allObjects['Contents']:
        allS3Keys[str(i['Key'])] = i['LastModified']

# Discover objects to delete
olderThanDate = datetime.datetime.now(tz=pytz.utc) - datetime.timedelta(int(HowManyDays))
print 'Finding all objects in ' + BucketName + '/' + FolderName + ' older than ' + str(HowManyDays) + ' days (' + str(olderThanDate) + ')'
for key in allS3Keys:
    if allS3Keys[key] < olderThanDate:
        print key + ' => ' + str(allS3Keys[key]) + ' (marked for delete)'
        if Delete:
            s3Client.delete_object(Bucket=BucketName,Key=key)
    else:
        print key + ' => ' + str(allS3Keys[key])
