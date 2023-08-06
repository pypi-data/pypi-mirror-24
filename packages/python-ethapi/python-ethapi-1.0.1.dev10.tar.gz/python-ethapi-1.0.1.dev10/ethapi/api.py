import ethapi.eth as eth

class Pool(eth.Eth):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def networkstats(self):
        return self._get('networkStats')

    def poolstats(self):
        return self._get('poolStats')

    def credits(self):
        return self._get('credits')


class Servers(eth.Eth):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def history(self):
        return self._get('servers/history')


class Blocks(eth.Eth):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def history(self):
        return self._get('blocks/history')


class Miner(eth.Eth):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def history(self, miner_id):
        return self._get('miner/' + miner_id + '/history')

    def payouts(self, miner_id):
        return self._get('miner/' + miner_id + '/payouts')

    def rounds(self, miner_id):
        return self._get('miner/' + miner_id + '/rounds')

    def settings(self, miner_id):
        return self._get('miner/' + miner_id + '/settings')

    def currentstats(self, miner_id):
        return self._get('miner/' + miner_id + '/currentStats')


class Worker(eth.Eth):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def workers(self, miner_id):
        return self._get('miner/' + miner_id + '/workers')

    def history(self, miner_id, worker_id):
        return self._get('miner/' + miner_id + '/worker/' + worker_id + '/history')

    def currentstats(self, miner_id, worker_id):
        return self._get('miner/' + miner_id + '/worker/' + worker_id + '/currentStats')
