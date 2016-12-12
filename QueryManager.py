# -*- coding: utf-8 -*-
import mysql.connector
import boto3
try:
    import configparser
except:
    from six.moves import configparser
import MySQLdb

class QueryManager():
    def __init__(self):
        #connect to ec2 instance
        ec2 = boto3.resource('ec2')


    def


    def sendQuery(queryObject):
        var aws = require('aws-sdk');
        var lambda = new aws.Lambda({
          region: 'us-east-1' //change to your region
        });

        lambda.invoke({
          FunctionName: 'DialogManager',
          Payload: JSON.stringify(queryObject, null, 2) // pass params
        }, function(error, data) {
          if (error) {
            context.done('error', error);
          }
          if(data.Payload){
           context.succeed(data.Payload)
          }
        });
