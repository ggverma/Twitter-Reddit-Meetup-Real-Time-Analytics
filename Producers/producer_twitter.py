# Author: Gautam Verma

from TwitterAPI import TwitterAPI
from AWS_CREDS import *
import sys
## twitter credentials
consumer_key        = ""
consumer_secret     = ""
access_token_key    = ""
access_token_secret = ""

# Use this for replication. This increases the size of data. Should be 1 ideally.
MULTIPLE_POST_SEND_LIMIT = 1000
if len(sys.argv) == 2:
    MULTIPLE_POST_SEND_LIMIT = int(sys.argv[1])
KINESIS_PUT_BATCH_SIZE = MULTIPLE_POST_SEND_LIMIT / 10

KINESIS_PUT_BATCH_SIZE = 1 if KINESIS_PUT_BATCH_SIZE == 0 else KINESIS_PUT_BATCH_SIZE
KINESIS_PUT_BATCH_SIZE = 500 if KINESIS_PUT_BATCH_SIZE > 500 else KINESIS_PUT_BATCH_SIZE

count = 0
def worker():
    try:
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
        r = api.request('statuses/filter', {'locations':'-90,-90,90,90'})
        while True:
            for item in r:
                putDataToKinesisStream(item, TYPE_TWITTER, MULTIPLE_POST_SEND_LIMIT, KINESIS_PUT_BATCH_SIZE)
    except Exception as e:
        print e
        worker()

if __name__ == "__main__":
    stream_description = kinesis.describe_stream(StreamName=AWS_STREAM_NAME)

    for shard in stream_description['StreamDescription']['Shards']:
        explicit_hash_keys.append(shard['HashKeyRange']['StartingHashKey'])

    worker()
