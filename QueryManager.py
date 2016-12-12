# -*- coding: utf-8 -*-

import sys
import rds_config 
import pymysql
import getpass

class QueryManager():
  """
  This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
  The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
  as testing instructions are located at http://amzn.to/1LzFrj6
  
  For additional samples, visit the Alexa Skills Kit Getting Started guide at
  http://amzn.to/1LGWsLG
  """
  
  def __init__(self):
    #rds settings
    self.host  = rds_config.endpoint
    self.name = rds_config.user
    self.db = rds_config.db 
    self.pw=getpass.getpass('pw?\t')
    # test the connection
    try:
        self.connect(timeout=15)
    except pymysql.err.OperationalError:
        sys.exit('Connection failed; check password and IP and try again.')
    # save the db schema to ensure usability
    self.schema = {'fact':{'table':'FactsList',
                           'fields':{'id':'idFactsList','country':'countryID',
                                     'fact':'fact','intent':'intent','city':'city',
                                     'industry':'industry','topic':'topic'}},
                   'country':{'table':'CountryList',
                              'fields':{'id':'id', 'name':'name'}},
                   'city':{'table':'CityList',
                           'fields':{'id':'id', 'name':'name', 'country':'countryId'}},
                   'user':{'table':'UserInfo',
                           'fields':{'id':'uid', 'name':'name','age':'age',
                                     'sex':'sex','education':'education',
                                     'language':'language','industry':'industry'}},
                   'context':{'table':'UserContext',
                              'fields':{'id':'context_id','user':'uid',
                                        'country':'`requested-cid`','topic':'topic',
                                        'intent':'intent','city':'city_id'}}}
  
  
  def connect(self, timeout=5):
    """
    returns a connection to this QM's database.
    """
    return pymysql.connect(self.host, 
                           db=self.db,
                           user=self.name, 
                           passwd=self.pw, 
                           connect_timeout=timeout)
  
  
  def queryDb(self, query):
    """
    This function fetches content from mysql RDS instance
    I.E., given event (query, search DB for elements to send to dialogManager)
    If no results are found, an empty tuple is returned.        
    """
    results = ()
    con = self.connect()
    
    try:
      with con.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall() # save any results of this query
      con.commit() # commit any changes made by this query
    
    except pymysql.err.IntegrityError:
      print 'A pymysql IntegrityError has been raised.  Be sure the query meets field constraints.'
    except pymysql.err.InternalError:
      print 'A pymysql InternalError has been raised.  Be sure the query has content and is valid'
    
    finally:
      con.close()
    
    return results
            

  def getFact(self, intent):
    """
    Return a random fact string based on the supplied intent dictionary
    """    
    
    table = self.schema['fact']['table']
    target = self.schema['fact']['fields']['fact']
    
    country = intent.get('country',None)
    city = intent.get('city',None)
    intent_type = intent.get('intent',None)
    topic = intent.get('topic',None)
    industry = intent.get('industry',None)
       
    query = ["select {} from {}".format(target, table)]
    conditions = []
    
    # join tables or filter by conditions if needed
    if country is not None:
      country_table = self.schema['country']['table']
      country_id = self.schema['country']['fields']['id']
      fact_country = self.schema['fact']['fields']['country']
      country_name = self.schema['country']['fields']['name']
      query.append("left outer join {} on {}.{}={}.{}".format(country_table,
                                                              country_table,
                                                              country_id,
                                                              table,
                                                              fact_country))
      conditions.append("{}.{} like '%{}%'".format(country_table,
                                                   country_name,
                                                   country))
      
    if city is not None:
      city_table = self.schema['city']['table']
      city_id = self.schema['city']['fields']['id']
      fact_city = self.schema['fact']['fields']['city']                                                   
      city_name = self.schema['city']['fields']['name']
      query.append("left outer join {} on {}.{}={}.{}".format(city_table,
                                                              city_table,
                                                              city_id,
                                                              table,
                                                              fact_city))
      # if no country was suppplied, play along. otherwise, be quietly intelligent
      if country is not None:
        city_country = self.schema['city']['fields']['country'] 
        # country info (fact_country) reused from above
        query.append("and {}.{}={}.{}".format(city_table,
                                              city_country,
                                              table,
                                              fact_country))    
      conditions.append("{}.{} like '%{}%'".format(city_table,
                                                   city_name,
                                                   city))

    if intent_type is not None:
      fact_intent = self.schema['fact']['fields']['intent']
      conditions.append("{}.{} like '%{}%'".format(table,
                                                   fact_intent,
                                                   intent_type))
      
    if topic is not None:
      fact_topic = self.schema['fact']['fields']['topic']
      conditions.append("{}.{} like '%{}%'".format(table,
                                                   fact_topic,
                                                   topic))
    
    if industry is not None:
      fact_industry = self.schema['fact']['fields']['industry']
      conditions.append("{}.{} like '%{}%'".format(table,
                                                   fact_industry,
                                                   industry))
    
    if len(conditions) > 0:
      query.append("where")
      query.append(" and ".join(conditions))
    # pick a match out of the hat
    query.append("order by rand() limit 1;")    
    
    #print query # debugging
    r = self.queryDb(" ".join(query))
    if len(r) > 0:
      return r[0][0] # return just the string
    else:
      return ''
    
    
  def getContext(self, intent):
    """
    given a partial intent dictionary, returns the most recent matching context.
    """
    
    # context record information
    table = self.schema['context']['table']
    table_id = self.schema['context']['fields']['id']
    
    # supplied intent information
    country = intent.get('country',None)
    city = intent.get('city',None)
    intent_type = intent.get('intent',None)
    topic = intent.get('topic',None)
    user = intent.get('user',None)
    
    # tables and fields needed to locate and filter matches
    c_user = self.schema['context']['fields']['user']
    c_country = self.schema['context']['fields']['country']
    c_city = self.schema['context']['fields']['city'] 
    c_intent = self.schema['context']['fields']['intent']
    c_topic = self.schema['context']['fields']['topic']
    user_table = self.schema['user']['table']
    user_id = self.schema['user']['fields']['id']
    user_name = self.schema['user']['fields']['name']
    country_table = self.schema['country']['table']
    country_id = self.schema['country']['fields']['id']
    country_name = self.schema['country']['fields']['name']
    city_table = self.schema['city']['table']
    city_id = self.schema['city']['fields']['id']                                                    
    city_name = self.schema['city']['fields']['name']
    
    conditions = []
    query = ["select {}.{},{}.{},{}.{},{}.{},{}.{} from {}".format(user_table, user_name,
                                                                   country_table, country_name,
                                                                   city_table, city_name,
                                                                   table, c_intent,
                                                                   table, c_topic,
                                                                   table)]
        
    # join user table to get user's name
    query.append("left outer join {} on {}.{}={}.{}".format(user_table,
                                                            user_table,
                                                            user_id,
                                                            table,
                                                            c_user))
    # join country table to get country's name
    query.append("left outer join {} on {}.{}={}.{}".format(country_table,
                                                            country_table,
                                                            country_id,
                                                            table,
                                                            c_country)) 
    # join city table to get city's name
    query.append("left outer join {} on {}.{}={}.{}".format(city_table,
                                                            city_table,
                                                            city_id,
                                                            table,
                                                            c_city))
    if country is not None: # attempt to catch city collisions
      city_country = self.schema['city']['fields']['country'] 
      query.append("and {}.{}={}.{}".format(city_table,
                                            city_country,
                                            table,
                                            c_country))
    # filter by specified user
    if user is not None:
      conditions.append("{}.{} like '%{}%'".format(user_table,
                                                   user_name,
                                                   user))   
    # filter by specified country
    if country is not None:
      conditions.append("{}.{} like '%{}%'".format(country_table,
                                                   country_name,
                                                   country))
    # filter by specified city
    if city is not None:
      conditions.append("{}.{} like '%{}%'".format(city_table,
                                                   city_name,
                                                   city))
    # filter by specified intent
    if intent_type is not None:
      conditions.append("{}.{} like '%{}%'".format(table,
                                                   c_intent,
                                                   intent_type))
    # filter by specified topic
    if topic is not None:
      conditions.append("{}.{} like '%{}%'".format(table,
                                                   c_topic,
                                                   topic))
    
    # add filtering conditions to query
    if len(conditions) > 0:
      query.append("where")
      query.append(" and ".join(conditions))      
    # get most recently-added match
    query.append("order by {}.{} desc limit 1;".format(table,
                                                       table_id)) 
    r = self.queryDb(" ".join(query))
    # return a dictionary
    output = {'user':None, 'country':None, 'city':None, 'intent':None, 'topic':None}
    if len(r) > 0:
      output = {'user':r[0][0], 'country':r[0][1], 'city':r[0][2], 'intent':r[0][3], 'topic':r[0][4]} 
    return output
    
    
  def updateContext(self, intent):
    """
    Using the supplied intent dictionary, add a new context to the db.
    """

    # prepare fields
    table = self.schema['context']['table']
    c_user = self.schema['context']['fields']['user']
    c_country = self.schema['context']['fields']['country']
    c_city = self.schema['context']['fields']['city'] 
    c_intent = self.schema['context']['fields']['intent']
    c_topic = self.schema['context']['fields']['topic']
    user = intent.get('user', '') # Only the User is assumed to have been supplied
    country = intent.get('country', None)
    city = intent.get('city', None)
    intent_type = intent.get('intent', None)
    topic = intent.get('topic', None)
    columns = []
    values = []    
    
    # We could join everything, but it's easier to use helper queries.
    # get user
    user_id = self.schema['user']['fields']['id']
    user_table = self.schema['user']['table']
    user_name = self.schema['user']['fields']['name']
    u_id = self.queryDb("select {} from {} where {} like '%{}%'".format(user_id,
                                                                        user_table,
                                                                        user_name,
                                                                        user))[0][0]
    columns.append(c_user)
    values.append(str(u_id))
    
    # get country, if supplied
    if country is not None:
      country_table = self.schema['country']['table']
      country_id = self.schema['country']['fields']['id']
      country_name = self.schema['country']['fields']['name']
      cn_id = self.queryDb("select {} from {} where {} like '%{}%'".format(country_id,
                                                                           country_table,
                                                                           country_name,
                                                                           country))[0][0] 
      columns.append(c_country)
      values.append(str(cn_id))
      
    # get city, if supplied
    if city is not None:
      city_table = self.schema['city']['table']
      city_id = self.schema['city']['fields']['id']                                                    
      city_name = self.schema['city']['fields']['name']
      q = "select {} from {} where {} like '%{}%'".format(city_id,
                                                          city_table,
                                                          city_name,
                                                          city)
      if country is not None:
        city_country = self.schema['city']['fields']['country']
        # we've already found the relevant country id
        q += " and {}={}".format(city_country, cn_id)
      ct_id = self.queryDb(q)[0][0]
      columns.append(c_city)
      values.append(str(ct_id))
      
    if intent_type is not None:
      columns.append(c_intent)
      values.append(intent_type.join(["'", "'"]))
    
    if topic is not None:
      columns.append(c_topic)
      values.append(topic.join(["'", "'"]))
    
    columns = ','.join(columns)
    values = ','.join(values)
    q = "insert into {} ({}) values ({});".format(table,
                                                 columns,
                                                 values)
    print q
    self.queryDb(q)
    
  
  
'''    
###Send finished query object to dialog manager
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
'''

'''
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
'''