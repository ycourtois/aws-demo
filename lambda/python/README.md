# Lambda + API gateway

## Deployment

```
sam build
sam package --output-template-file sam.packaged.yaml --s3-bucket tsv-bdx-demo --s3-prefix sam
sam deploy --template-file sam.packaged.yaml --stack-name tsv-bdx-demo-cars --capabilities CAPABILITY_IAM
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

1. Start api:
`sam local start-api -n cars-api-env.json -d 5590`

2. Launch request: `http://localhost:3000/cars`

3. Start remote debugging from VSCode

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
