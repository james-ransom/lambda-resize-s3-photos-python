# README #

This repro is responsible for the aws lambda code that resizes images put into the folder afterschool-photos

### Creating the lambda
```bash
aws lambda create-function --region us-east-1 --function-name CreateThumbnail --zip-file fileb://CreateThumbnail.zip --role arn:aws:iam::99999999:role/lambda-s3-execution-role --handler CreateThumbnail.handler --runtime python2.7 --timeout 10 --memory-size 1024 
```

### Deleting a lambda
```bash
aws lambda   delete-function  --function-name CreateThumbnail  --region us-east-1
```

### Adding updates for CreateThumbnail.py ###
```bash
zip -d CreateThumbnail.zip CreateThumbnail.py
zip -u CreateThumbnail.zip CreateThumbnail.py
```



### Who do I talk to?

* Repo owner 
