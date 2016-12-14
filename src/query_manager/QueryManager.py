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
    #self.pw=getpass.getpass('pw?\t')
    self.pw = rds_config.pw
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
                                     'language':'language','industry':'industry',
                                     'amazonID':'amazonID'}},
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
    amazonID = intent.get('amazon_id',None)
    
    # tables and fields needed to locate and filter matches
    c_user = self.schema['context']['fields']['user']
    c_country = self.schema['context']['fields']['country']
    c_city = self.schema['context']['fields']['city'] 
    c_intent = self.schema['context']['fields']['intent']
    c_topic = self.schema['context']['fields']['topic']
    user_table = self.schema['user']['table']
    user_id = self.schema['user']['fields']['id']
    user_aid = self.schema['user']['fields']['amazonID']
    user_name = self.schema['user']['fields']['name']
    country_table = self.schema['country']['table']
    country_id = self.schema['country']['fields']['id']
    country_name = self.schema['country']['fields']['name']
    city_table = self.schema['city']['table']
    city_id = self.schema['city']['fields']['id']                                                    
    city_name = self.schema['city']['fields']['name']
    
    conditions = []
    query = ["select {}.{},{}.{},{}.{},{}.{},{}.{},{}.{} from {}".format(user_table, user_name,
                                                                         country_table, country_name,
                                                                         city_table, city_name,
                                                                         table, c_intent,
                                                                         table, c_topic,
                                                                         user_table, user_aid,
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
    # filter by specified user auth_token (amazon id)
    if amazonID is not None:
      conditions.append("{}.{} like '%{}%'".format(user_table,
                                                   user_aid,
                                                   amazonID))   
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
    output = {'username':None, 'country':None, 'city':None, 'intent':None, 'topic':None, 'amazon_id':None}
    if len(r) > 0:
      output = {'amazon_id':r[0][5], 'username':r[0][0], 'country':r[0][1], 'city':r[0][2], 'intent':r[0][3], 'topic':r[0][4]} 
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
    amazonID = intent.get('amazon_id', '') # Only the User's aID is assumed to have been supplied
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
    user_aid = self.schema['user']['fields']['amazonID']
    u_id = self.queryDb("select {} from {} where {} like '%{}%'".format(user_id,
                                                                        user_table,
                                                                        user_aid,
                                                                        amazonID)) 
    if len(u_id) > 0:
      u_id=u_id[0][0]
    else:
      u_id='NULL'
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
                                                                           country))
      if len(cn_id) > 0:
        cn_id=cn_id[0][0]
      else:
        cn_id='NULL' 
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

      print q
      
      ct_id = self.queryDb(q)
      if len(ct_id) > 0:
        ct_id=ct_id[0][0]
      else:
        ct_id='NULL'
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
    

  def is_user_account_complete(self, amazon_id):
    """
    Given an Amazon ID, check to see if that user is in our db or not.
    Returns a boolean==True only if a record exists and is fully populated.
    Adds the Amazon ID to the db if it is not already there.
    """
    complete = True
    user = self.queryDb("select * from UserInfo where amazonID='{}';".format(amazon_id))
    if len(user) > 0:
      for field in user[0]:
        if field is None: # some field isn't populated
          complete = False
          break
    else: # auth_token isn't in database at all
      complete = False    
      self.addUser({self.schema['user']['fields']['amazonID']:amazon_id})
    return complete


  def get_name(self, amazon_id):
    """
    Returns user's name given their amazon auth_token
    """
    table = self.schema['user']['table']
    user_name = self.schema['user']['fields']['name']
    user_aid = self.schema['user']['fields']['amazonID']

    query = "select {} from {} where {}='{}' limit 1;".format(user_name, table, user_aid, amazon_id)
    r = self.queryDb(query)
    if len(r) > 0:
      return r[0][0] # return just the string
    else:
      return 'Sasha'    


  def add_user_element(self, amazon_id, user_dict):
    """
    Given a user's amazon_id and dictionary of info, update the db.
    """
    name = user_dict.get('name',None)
    age = user_dict.get('age',None)
    sex = user_dict.get('sex',None)
    language = user_dict.get('language',None)
    education = user_dict.get('education',None)
    industry = user_dict.get('industry',None)

    table = self.schema['user']['table']
    user_aid = self.schema['user']['fields']['amazonID']
    pairs = []
    queries = []
    
    if name is not None:
      c = self.schema['user']['fields']['name']
      v=name[:45].join(["'", "'"])
      pairs.append((c,v))
    if sex is not None:
      c=self.schema['user']['fields']['sex']
      v=sex[:45].join(["'", "'"])
      pairs.append((c,v))
    if language is not None:
      c=self.schema['user']['fields']['language']
      v=language[:45].join(["'", "'"])
      pairs.append((c,v))
    if education is not None:
      c=self.schema['user']['fields']['education']
      v=education[:45].join(["'", "'"])
      pairs.append((c,v))
    if industry is not None:
      c=self.schema['user']['fields']['industry']
      v=industry[:45].join(["'", "'"])
      pairs.append((c,v))
    if age is not None:
      c=self.schema['user']['fields']['age']
      v=age
      pairs.append((c,v))
    
    for p in pairs:
      q = "update {} set {}={} where {}='{}'".format(table, p[0], p[1], user_aid, amazon_id)
      queries.append(q)

    query = ';'.join(queries)

    print query
    self.queryDb(query)


  def addUser(self, user_dict):
    """
    Given a dictionary of user info to add to the db, do so.
    """
    name = user_dict.get('name',None)
    age = user_dict.get('age',None)
    sex = user_dict.get('sex',None)
    language = user_dict.get('language',None)
    education = user_dict.get('education',None)
    industry = user_dict.get('industry',None)
    amazonID = user_dict.get('amazonID',None)

    columns = []
    values = []
    
    if amazonID is not None:
      columns.append(self.schema['user']['fields']['amazonID'])
      values.append(amazonID[:45].join(["'", "'"]))
    if name is not None:
      columns.append(self.schema['user']['fields']['name'])
      values.append(name[:45].join(["'", "'"]))
    if sex is not None:
      columns.append(self.schema['user']['fields']['sex'])
      values.append(sex[:45].join(["'", "'"]))
    if language is not None:
      columns.append(self.schema['user']['fields']['language'])
      values.append(language[:45].join(["'", "'"]))
    if education is not None:
      columns.append(self.schema['user']['fields']['education'])
      values.append(education[:45].join(["'", "'"]))
    if industry is not None:
      columns.append(self.schema['user']['fields']['industry'])
      values.append(industry[:45].join(["'", "'"]))
    if age is not None:
      columns.append(self.schema['user']['fields']['age'])
      values.append(age)

    table = self.schema['user']['table']
    columns = ','.join(columns)
    values = ','.join(values)
    query = "insert into {} ({}) values ({});".format(table,
                                                      columns,
                                                      values)
    print query
    self.queryDb(query)


  def find_next_user_setup(self, auth_token):
    """
    Given a user's auth_token (amazonID), returns which if any field is missing in their record, in a particular order 
    """
    #fields = ['age', 'name', 'education', 'industry_name', 'job_title', 'language']
    fields = ['age', 'name', 'education', 'industry_name', 'language'] # job_title is not a field in db

    table = self.schema['user']['table']
    u_age = self.schema['user']['fields']['age']
    u_name = self.schema['user']['fields']['name']
    u_edu = self.schema['user']['fields']['education']
    u_ind = self.schema['user']['fields']['industry']
    u_lg = self.schema['user']['fields']['language']
    u_aid = self.schema['user']['fields']['amazonID']

    query = "select {},{},{},{},{} from {} where {} like '%{}%';".format(u_age,u_name,u_edu,u_ind,u_lg,
                                                                         table,
                                                                         u_aid, auth_token)
    r = self.queryDb(query)
    next = ''
    if len(r) > 0:
      for i in range(len(r[0])):
        if r[0][i] is None:
          next = fields[i]
          break
    return next









