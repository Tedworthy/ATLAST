import ConfigParser


def parse_config_file(file):
    config_data = {}
    config = ConfigParser.RawConfigParser()
    try:
      config.read(file)
      config_data['host'] = config.get('DatabaseCon', 'host')
      config_data['port'] = config.get('DatabaseCon', 'port')
      config_data['username']  = config.get('DatabaseCon', 'user')
      config_data['dbname'] = config.get('DatabaseCon', 'dbname')
      config_data['password'] = config.get('DatabaseCon', 'password')
      config_data['Error'] = '0'
    except Exception, e:
      print "Error: " + str(e)
      config_data['Error'] = '1'
    finally:
      return config_data

