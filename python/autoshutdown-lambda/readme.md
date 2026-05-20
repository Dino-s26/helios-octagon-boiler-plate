# How to use

### Prerequisites
- AWS Lambda Function
- AWS IAM Role
- AWS EventBridge Schedule Rule

### Create Lambda Function
There are 2 way to create lambda function:

1. Using AWS CLI
```
aws lambda create-function --function-name <your-function-name> --architectures arm64 --handler lambda_function.lambda_handler --timeout 90 --memory-size 128 --ephemeral-storage 512 --runtime python3.14 --logging-config '{"LogFormat": "Text"}' --zip-file <code-in-zip>
```

2. Using AWS Console
    1. Go to AWS Lambda
    2. Click on Create function
    3. Click on Author from scratch
    4. Fill in the function name, runtime, and architecture
    5. Click on Create function then copy-paste the code to the code editor
    6. Click on Deploy
    7. Copy the Function ARN for EventBridge Schedule Rule

### Create IAM Role
1. Go to AWS IAM
2. Click on Roles
3. Click on Create role
4. Select AWS service
5. Select Lambda
6. Click on Next
7. Select the policies that you want to attach to the role
    ```
    ## Policies
    - AWSLambdaBasicExecutionRole
    - AmazonEC2FullAccess
    ```
8. Click on Next
9. Click on Create role

### Create EventBridge Schedule Rule
1. Go to AWS EventBridge
2. Click on Rules
3. Click on Create rule
4. Fill in the rule name and description
5. Select the schedule
6. On Invoke part, there will be payload, you can copy-paste the example below:

    ## For start action
    ```
    {
    //for multi region setup, just add more regions and instance ids
    "regions": {
        "ap-southeast-1": ["i-12345667890abcdef"],
        "ap-southeast-3": ["i-0987654321abcdef"]
    },
    "action": "start"
    }
    ```

    ## For stop action
    ```
    {
    //for multi region setup, just add more regions and instance ids
    "regions": {
        "ap-southeast-1": ["i-12345667890abcdef"],
        "ap-southeast-3": ["i-0987654321abcdef"]
    },
    "action": "stop"
    }
    ```

7. Click on Next
8. Select the target
9. Click on Create rule

### Test Scheduler

To test the scheduler, try to adjust the time to 1 minute and then check the CloudWatch logs to see if the scheduler is working properly. After the test is completed, remember to change the time back to the desired time.

### Test Lambda Function
To test lambda function manually
1. Go to AWS Lambda
2. Click on your function
3. Click on Test
4. Fill in the payload (make sure the instance id is correct or use the example below)
    ## Example Payload
    ```
    {
    "regions": {
        "ap-southeast-1": ["i-045516eb48d2b3bb6"],
        "ap-southeast-3": ["i-030c4658d67fc7b9e","i-07651f8193d6a9f6b","i-0285904670b7934d5"]
    },
    "action": "stop"
    }
    ```
5. Click on Test
6. Check the result for error