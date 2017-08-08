# s3utils

Varioud utilities to do sysadmin-type things.

## setAllS3ACLs

### command line options

 -b bucketname
 
 -p profile name (default is "default")
 
 -a acl (default is "authenticated-read")

### Purpose

AWS S3 has an interesting nuance to its use.  In addition to an IAM user (or role or instance) policy to be granted access to an S3 bucket, a bucket also has a Bucket Policy.  But, in addition to THAT, there is ALSO an object-level ACLs.  What frequently happens to me is that after a bunch of files have been uploaded to S3, although my policies may allow me access to the bucket, the object ACL still prevents me from reading the object.

This script allows any IAM user with bucket Put policy permissions to set the object acls on every object in the bucket.

## delLotsOfObjects

### command line options

 -b bucketname
 
 -p profile name (default is "default")
 
 -f foldername
 
 -k days to keep
 
 -e region (default is us-east-1)
 
 ### Purpose
 
 If you have a LOT of objects to delete, say hundreds or thousands, because you want to delete every object older than, say, 30 days, then this script it for you.  This script can easily be modified to be a one-shot...delete on regex or prefix or whatever your heart desires.
