import redis

def redisAdd(dict):
    r = redis.Redis(host='localhost', port=6379, db=0)
    #get first key and value from dict
    key = list(dict.keys())[0]
    value = list(dict.values())[0]
    r.set(value, key)
    return {"message": "redis added"}

def redisGet(key):
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.get(key)

def redisDelete(key):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.delete(key)
    return {"message": "redis deleted"}

def redisUpdate(dict):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(dict['value'], dict['key'])

    return {"message": "redis updated"}

def redisCheck(key):
    r = redis.Redis(host='localhost', port=6379, db=0)
    #check if value exists
    if r.get(key):
        return True
    else:
        return False
