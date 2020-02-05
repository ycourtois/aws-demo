# Lambda functions + API gateway

## Deployment

### Prerequisites

Create an S3 bucket to store your artifacts.

Once done, update BUCKET_ARTIFACT variable.

```
BUCKET_ARTIFACT=tsv-bdx-demo
STACK_NAME=tsv-bdx-demo-cars

sam build
sam package --output-template-file sam.packaged.yaml --s3-bucket ${BUCKET_ARTIFACT} --s3-prefix sam
sam deploy --template-file sam.packaged.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM
```

## Local Testing

Create a dedicated docker network to run our application.

`docker network create sam-local`

Launch local dynamodb database.

`docker run --name dynamodb --network-alias=dynamodb --network sam-local -p 8000:8000 amazon/dynamodb-local`

`sam local start-api --docker-network sam-local -n cars-api-env.json`

## Local Debug

Remote debug does not work with PyCharm.
Use VSCode : https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-debugging-python.html

1. Install debug dependency

    In order to proceed to remote debug, you need an external dependency named `ptvsd`
    
    Add `ptvsd` inside `requirements.txt`
    
    Add the following instructions inside your function to wait for remote connection.
    
    ```
    ptvsd.enable_attach(address=('0.0.0.0', 5590), redirect_output=True)
    ptvsd.wait_for_attach()
    ```

2. Start api:

    `sam local start-api -n cars-api-env.json -d 5590`

3. Launch request: `http://localhost:3000/cars`

4. Start remote debugging from VSCode

    ```
    "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Remote Attach",
                "type": "python",
                "request": "attach",
                "port": 5590,
                "host": "localhost",
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}/.aws-sam/build/GetCarsFunction",
                        "remoteRoot": "/var/task"
                    }
                ]
            }
        ]
    }
    ```
