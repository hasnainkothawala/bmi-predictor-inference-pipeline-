
# bmi-predictor-inference-pipeline-
A flask based API which responds the insurance quote based on BMI and other rules.

I have created a flask application which is dependent on a mongo
container. I have dockerized the flask app as well as the mongo container.

# Below are the steps to run :
Go to `docker.env` and update `MONGO_HOST` to your IP.
Run : 
```sh
sudo docker-compose -f docker-compose.yml up --build -d
```


# End Point
The application runs on port 5001 (which can also be configured in the ENV). And exposes an end point for predicting the BMI.

## Request:

    [POST] http://localhost:5001/predict 

> {    "app_id":99516,    "age":22,    "gender":"Female",   
> "height":510,    "weight":480 }

## Response:

> { "BMI": 18.45444059976932, "Message": "BMI is in right range",
> "Quote": 450.0 }

## Productionizing the app:

This seems like a light weight rule based application.
There are 2 ways of processing the payload:

 1. Online (More realistic, since app is not compute heavy)-
    a. Use Route 64 + AWS Lambda to expose an Lambda endpoint URL. Add
       some security groups to Route 64.
    b. Use Route 64 + ECS (Fargate , EC2)
    c. Use Kubernetes (EKS), Expose an INGRESS, build and deploy the
       images on EKS, allow autoscaling with HPA and VPA.
 3. Batch
    a. SQS + AWS Lambda + AWS Batch (EC2, Fargate) - persist all the
       predictions in a database. Would also perhaps require a message
       broker such as Redis or Rabbitmq incase this combination needs to be
       used for Online (async)
       
    b. Any Messaging Queue service + Apache Airflow. Write DAGS with the
       same image and submit jobs. This combination would ensure the
       solution is vendor independent but cloud native.
       
## Things I would have worked on if had time :
 1. Make the end point secure with a token service.
 2. Add more validations while processing the payload.
 3. Perhaps consider using a SQL database and create models which would ensure data
resilience.
 4. Make the code more modular and configurable.
 5. Perhaps create a swagger documentation.
 6. Use fast-api or celery with a message broker to go async thus leveraging
multi-threading.
 7. Create a deployment.yml and deploy the app on a Mini Kube and scale it.



