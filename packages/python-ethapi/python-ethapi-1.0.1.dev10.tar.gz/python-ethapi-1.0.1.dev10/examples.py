import ethapi.api as api
import json

## Ethermine.org endpoint: https://api.ethermine.org
## Ethpool.org endpoint: http://api.ethpool.org
## Ethermine ETC endpoint: https://api-etc.ethermine.org
## Flypool Zcash endpoint: https://api-zcash.flypool.org
ENDPOINT = 'https://api.ethermine.org'

## If you would like to donate eth, use the below address. Thank you!
miner_id = '0xAE6Af33fb65cbaDFCA89987640A7985F77cee6D1'
worker_id = 'worker1'

# Pool
## /poolStats
pool = api.Pool(endpoint=ENDPOINT)
print(pool.poolstats())

## /credits
pool = api.Pool(endpoint=ENDPOINT)
print(pool.credits())

## /networkStats
pool = api.Pool(endpoint=ENDPOINT)
print(pool.networkstats())

## /blocks/history
blocks = api.Blocks(endpoint=ENDPOINT)
print(blocks.history())

## /servers/history
servers = api.Servers(endpoint=ENDPOINT)
print(servers.history())

# Miner
## /miner/:miner/history
miner = api.Miner(endpoint=ENDPOINT)
print(miner.history(miner_id=MINER_ID))

## /miner/:miner/payouts
miner = api.Miner(endpoint=ENDPOINT)
print(miner.payouts(miner_id=MINER_ID))

## /miner/:miner/rounds
miner = api.Miner(endpoint=ENDPOINT)
print(miner.rounds(miner_id=MINER_ID))

## /miner/:miner/settings
miner = api.Miner(endpoint=ENDPOINT)
print(miner.settings(miner_id=MINER_ID))

## /miner/:miner/currentStats
miner = api.Miner(endpoint=ENDPOINT)
print(miner.currentstats(miner_id=MINER_ID))

## Alternate pythonistic way for above
miner = api.Miner(endpoint=ENDPOINT)
stats = miner.currentstats(miner_id=MINER_ID)
print(stats)

# Worker
## /miner/:miner/workers
worker = api.Worker(endpoint=ENDPOINT)
print(worker.workers(miner_id=MINER_ID))

## /miner/:miner/worker/:worker/history
worker = api.Worker(endpoint=ENDPOINT)
print(worker.history(miner_id=MINER_ID, worker_id=WORKER_ID))

## /miner/:miner/worker/:worker/currentStats
worker = api.Worker(endpoint=ENDPOINT)
print(worker.currentstats(miner_id=MINER_ID, worker_id=WORKER_ID))

## Alternate pythonistic way for above
worker = api.Worker(endpoint=ENDPOINT)
stats = worker.currentstats(miner_id=MINER_ID, worker_id=WORKER_ID)
print(stats)

