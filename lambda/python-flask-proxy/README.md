# Proxy lambda function with API gateway

## Deployment

### Prerequisites

Build the solution.

```
sam build
```

Create an S3 bucket to store your artifacts.

Update `s3_bucket` variable inside `samconfig.toml` file.

```
sam deploy
```

OR

Update BUCKET_ARTIFACT variable.

```
PROJECT=tsv-bdx-demo
BUCKET_ARTIFACT=${PROJECT}
STACK_NAME=${PROJECT}-cars-proxy

sam package --output-template-file sam.packaged.yaml --s3-bucket ${BUCKET_ARTIFACT} --s3-prefix sam
sam deploy --template-file sam.packaged.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --parameter-overrides ParameterKey=Project,ParameterValue=${PROJECT} ParameterKey=FlaskEnv,ParameterValue=production
```

## Local Testing

### With remote DynamoDB database

`sam local start-api -n cars-api-env.json`

### With local DynamoDB database

Create a dedicated docker network to run our application.

`docker network create sam-local`

Launch local dynamodb database.

`docker run --name dynamodb --network-alias=dynamodb --network sam-local -p 8000:8000 amazon/dynamodb-local`

`sam local start-api --docker-network sam-local -n cars-api-env-local.json`

## Local Debug

With PyCharm you need to run the remote IDE configuration first before running your python script while
for Visual Studio Code you run it after your python script.

You will find explanations below.

### With PyCharm

1. Install debug dependency

    In order to proceed to remote debug, you need an external dependency named `pydevd_pycharm`
    
    Add `pydevd_pycharm` inside `requirements.txt`
    
    Add the following instructions inside your function to wait for remote connection.
    
    ```
    pydevd_pycharm.settrace("host.docker.internal", port=5590, stdoutToServer=True,
                            stderrToServer=True)
    ```

2. Inside PyCharm, create a Python Remote Debug configuration and set locahost name to '0.0.0.0' and port to '5590'
   Launch remote debug server

3. Start api: `sam local start-api -n cars-api-env.json`

4. Launch request: `http://localhost:3000/cars`

### With VSCode

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-debugging-python.html

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
