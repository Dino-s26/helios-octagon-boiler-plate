import boto3
import botocore
import DateTime
import json

## initiate EC2 via Boto3

ec2 = boto3.client('ec2', region_name='ap-southeast-3')



def lambda_handler(event=None, context=None):

    instances = [] 

    ec2_results = ec2.describe_instances()
    #ec2_start = ec2.start_instances(InstanceIds=[instances])
    #ec2_stop = ec2.stop_instances(InstanceIds=[instances])


    for reservation in ec2_results['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']

            name = None
            for tag in instance.get('Tags', []):
                if tag['Key'] == 'Name' :
                    name = tag['Value']
                    break

            instances.append({
                'InstanceId': instance_id,
                'Name': name, 
                'Status': state,
            })

    return {
        'StatusCode': 200, 
        'body': instances
    }

if __name__ == "__main__":
    response = lambda_handler()
    print(json.dumps(response, indent=2))