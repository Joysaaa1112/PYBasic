from redis import Redis
import config.cache as cache

redis = Redis(host=cache.HOST, port=cache.PORT, password=cache.PASSWORD, db=cache.DB)
