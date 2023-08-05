""" This file explains explains the rules for adding and removing blocks from the local chain.
"""
import Queue
import copy
import threading
import time

from decimal import Decimal

import custom
import pt
import tools
from ntwrk import Response

from service import Service, threaded, sync


def hex_sum(a, b):
    # Sum of numbers expressed as hexidecimal strings
    return tools.buffer_(str(hex(int(a, 16) + int(b, 16)))[2: -1], 64)


def hex_invert(n):
    # Use double-size for division, to reduce information leakage.
    return tools.buffer_(str(hex(int('f' * 128, 16) / int(n, 16)))[2: -1], 64)


class BlockchainService(Service):
    tx_types = ['spend', 'mint']
    IDLE = 1
    SYNCING = 2

    def __init__(self, engine):
        Service.__init__(self, name='blockchain')
        self.engine = engine
        self.blocks_queue = Queue.Queue()
        self.tx_queue = Queue.Queue()
        self.db = None

    def on_register(self):
        self.db = self.engine.db
        return True

    @threaded
    def process(self):
        while not self.blocks_queue.empty():
            candidate_block = self.blocks_queue.get()
            self.add_block(candidate_block)
            self.blocks_queue.task_done()

        while not self.tx_queue.empty():
            candidate_tx = self.tx_queue.get()
            self.add_tx(candidate_tx)
            self.tx_queue.task_done()

    @sync
    def tx_pool(self):
        """
        Return all the transactions waiting in the pool.
        This method should be used instead of direct access to db
        :return:
        """
        return self.db.get('txs')

    @sync
    def tx_pool_add(self, tx):
        """
        This is an atomic add operation for txs pool.
        :param tx: Transaction to be added
        :return: None
        """
        txs = self.db.get('txs')
        txs.append(tx)
        self.db.put('txs', txs)

    @sync
    def tx_pool_pop_all(self):
        """
        Atomic operation to pop everything
        :return: transactions list
        """
        txs = self.db.get('txs')
        self.db.put('txs', [])
        return txs

    @sync
    def add_tx(self, tx):

        if not isinstance(tx, dict):
            return False

        address = tools.tx_owner_address(tx)
        account = tools.get_account(self.db, address)

        # tools.log('attempt to add tx: ' +str(tx))
        txs_in_pool = self.tx_pool()

        response = Response(True, None)
        if 'type' not in tx or not isinstance(tx['type'], (str, unicode)) \
                or tx['type'] not in BlockchainService.tx_types:
            response.setData('type error')
            response.setFlag(False)
        if tx in txs_in_pool:
            response.setData('no duplicates')
            response.setFlag(False)
        if not BlockchainService.tx_integrity_check(tx).getFlag():
            response.setData('tx: ' + str(tx))
            response.setFlag(False)
        if tx['count'] != tools.known_tx_count(account, tools.tx_owner_address(tx), txs_in_pool):
            response.setData('count error')
            response.setFlag(False)
        if not tools.fee_check(tx, txs_in_pool, account):
            response.setData('fee check error')
            response.setFlag(False)

        if response.getFlag():
            self.tx_pool_add(tx)
            return 'added tx into the pool: ' + str(tx)
        else:
            return 'failed to add tx because: ' + response.getData()

    @sync
    def add_block(self, block):
        """Attempts adding a new block to the blockchain.
         Median is good for weeding out liars, so long as the liars don't have 51%
         hashpower. """

        def tx_check(txs_in_block):
            """
            Checks transactions validity in a sandboxed environment where
            accounts are simulated for the block.
            :param txs_in_block: transactions inside candidate block
            :return:
            """
            if 1 != len(filter(lambda t: t['type'] == 'mint', txs_in_block)):
                return False

            account_sandbox = {}
            for tx in sorted(txs_in_block, key=lambda t: t['count']):
                if tx['type'] == 'spend':
                    address_of_tx = tools.tx_owner_address(tx)

                    if address_of_tx not in account_sandbox:
                        account_of_tx = tools.get_account(self.db, address_of_tx)
                        account_sandbox[address_of_tx] = account_of_tx

                    account_of_tx = account_sandbox[address_of_tx]
                    integrity = BlockchainService.tx_integrity_check(tx).getFlag()
                    fee_check = tools.fee_check(tx, [], account_of_tx)
                    count_check = (account_of_tx['count'] == tx['count'])

                    if integrity and fee_check and count_check:
                        account_of_tx['amount'] -= tx['amount']
                        account_of_tx['amount'] -= custom.fee
                        account_of_tx['count'] += 1
                        account_sandbox[address_of_tx] = account_of_tx
                        continue
                    else:
                        tools.log('tx not valid')
                        return False  # Block is invalid
            return True  # Block is valid

        if not isinstance(block, dict):
            tools.log('Block is not a dict')
            return False

        if 'error' in block:
            tools.log('Errors in block')
            return False

        if not ('length' in block and isinstance(block['length'], int)):
            #tools.log('Length is not valid')
            return False

        length = self.db.get('length')

        if int(block['length']) != int(length) + 1:
            #tools.log('Length is not valid')
            return False

        # TODO: understand what is going on here
        if block['diffLength'] != hex_sum(self.db.get('diffLength'),
                                          hex_invert(block['target'])):
            tools.log('difflength is wrong')
            return False

        if length >= 0:
            if tools.det_hash(self.db.get(length)) != block['prevHash']:
                tools.log('prevhash different')
                return False

        if 'target' not in block:
            tools.log('no target in block')
            return False

        nonce_and_hash = tools.hash_without_nonce(block)
        if tools.det_hash(nonce_and_hash) > block['target']:
            tools.log('hash is not applicable to target')
            return False

        if block['target'] != self.target(block['length']):
            tools.log('block: ' + str(block))
            tools.log('target: ' + str(self.target(block['length'])))
            tools.log('wrong target')
            return False

        # earliest = tools.median(self.recent_blockthings(self.db.get('times'),
        #                                                custom.mmm,
        #                                                self.db.get('length')))

        if 'time' not in block:
            tools.log('no time')
            return False
        if block['time'] > time.time() + 60 * 6:
            tools.log('Received block is coming from future. Call the feds')
            return False
        # if block['time'] < earliest:
        #    tools.log('Received block is generated earlier than median.')
        #    return False
        if not tx_check(block['txs']):
            tools.log('Received block failed transactions check.')
            return False

        self.db.put(block['length'], block)
        self.db.put('length', block['length'])
        self.db.put('diffLength', block['diffLength'])

        targets = self.db.get('targets')
        targets.update({str(block['length']): block['target']})
        self.db.put('targets', targets)

        times = self.db.get('times')
        times.update({str(block['length']): block['time']})
        self.db.put('times', times)

        orphans = self.tx_pool_pop_all()

        self.cache_blockchain()

        for orphan in sorted(orphans, key=lambda x: x['count']):
            self.add_tx(orphan)

    @sync
    def delete_block(self):
        """ Removes the most recent block from the blockchain. """
        length = self.db.get('length')
        if length < 0:
            return
        try:
            targets = self.db.get('targets')
            targets.pop(str(length))
            self.db.put('targets', targets)
        except:
            pass
        try:
            times = self.db.get('times')
            times.pop(str(length))
            self.db.put('times', times)
        except:
            pass

        block = self.db.get(length)
        orphans = self.tx_pool_pop_all()

        for tx in block['txs']:
            orphans.append(tx)

        self.db.delete(length)
        length -= 1

        self.db.put('length', length)
        if length == -1:
            self.db.put('diffLength', '0')
        else:
            block = self.db.get(length)
            self.db.put('diffLength', block['diffLength'])

        self.cache_blockchain()

        for orphan in sorted(orphans, key=lambda x: x['count']):
            self.add_tx(orphan)

    @sync
    def recent_blockthings(self, key, size, length=0):

        def get_val(length):
            leng = str(length)
            if not leng in storage:
                block = self.db.get(leng)
                if not block:
                    if leng == self.db.get('length'):
                        self.db.put('length', int(leng) - 1)
                        block = self.db.get(leng)
                    else:
                        pass
                        #error()
                # try:
                storage[leng] = self.db.get(leng)[key[:-1]]
                self.db.put(key, storage)
            return storage[leng]

        def clean_up(storage, end):
            if end < 0: return
            if not str(end) in storage:
                return
            else:
                storage.pop(str(end))
                return clean_up(storage, end - 1)

        if length == 0:
            length = self.db.get('length')

        storage = self.db.get(key)
        start = max((length - size), 0)
        end = length - max(custom.mmm, custom.history_length) - 100
        clean_up(storage, length - end)
        return map(get_val, range(start, length))

    @sync
    def cache_blockchain(self):
        length = self.db.get('length')
        last_cache_length = self.db.get('last_cache_length')
        if length - last_cache_length >= custom.cache_length:
            cache_address_set = set()
            for i in range(last_cache_length, length):
                block = self.db.get(str(i))
                for tx in block['txs']:
                    cache_address_set.add(tools.tx_owner_address(tx))
                    if tx['type'] == 'spend':
                        cache_address_set.add(tx['to'])
            for address in cache_address_set:
                account = tools.get_account(self.db, address)
                account['cache_length'] = length
                self.db.put(address, account)
            self.db.put('last_cache_length', length)
        elif last_cache_length > (length+1):  # We deleted a block involved in cache. Rerun cache routine.
            #TODO: a better cache fallback
            self.db.put('last_cache_length', 0)

    @staticmethod
    def sigs_match(_sigs, _pubs, msg):
        pubs = copy.deepcopy(_pubs)
        sigs = copy.deepcopy(_sigs)

        def match(sig, pubs, msg):
            for p in pubs:
                if pt.ecdsa_verify(msg, sig, p):
                    return {'bool': True, 'pub': p}
            return {'bool': False}

        for sig in sigs:
            a = match(sig, pubs, msg)
            if not a['bool']:
                return False
            sigs.remove(sig)
            pubs.remove(a['pub'])
        return True

    @staticmethod
    def tx_signature_check(tx):
        tx_copy = copy.deepcopy(tx)
        if 'signatures' not in tx or not isinstance(tx['signatures'], (list,)):
            tools.log('no signatures')
            return False
        if 'pubkeys' not in tx or not isinstance(tx['pubkeys'], (list,)):
            tools.log('no pubkeys')
            return False

        tx_copy.pop('signatures')
        if len(tx['pubkeys']) == 0:
            tools.log('pubkey error')
            return False
        if len(tx['signatures']) > len(tx['pubkeys']):
            tools.log('there are more signatures then required')
            return False

        msg = tools.det_hash(tx_copy)
        if not BlockchainService.sigs_match(copy.deepcopy(tx['signatures']),
                                            copy.deepcopy(tx['pubkeys']), msg):
            tools.log('sigs do not match')
            return False
        return True

    @staticmethod
    def tx_integrity_check(tx):
        """
        This functions test whether a transaction has basic things right.
        Does it have amount, recipient, right signatures and correct address types.
        :param tx:
        :param txs: These txs can come from both pool and block.
        :return:
        """
        response = Response(True, None)
        if tx['type'] == 'spend':
            if 'to' not in tx or not isinstance(tx['to'], (str, unicode)):
                response.setData('no to')
                response.setFlag(False)
            if not BlockchainService.tx_signature_check(tx):
                response.setData('signature check')
                response.setFlag(False)
            if len(tx['to']) <= 30:
                response.setData('that address is too short ' + 'tx: ' + str(tx))
                response.setFlag(False)
            if 'amount' not in tx or not isinstance(tx['amount'], (int)):
                response.setData('no amount')
                response.setFlag(False)
            # TODO: This is new. Check this voting transactions
            if 'vote_id' in tx:
                if not tx['to'][:-29] == '11':
                    response.setData('cannot hold votecoins in a multisig address')
                    response.setFlag(False)
        else:
            response.setFlag(False)
            response.setData('only spend transactions can be cheched')
        return response

    @sync
    def target(self, length):
        memoized_weights = [custom.inflection ** i for i in range(1000)]
        """ Returns the target difficulty at a particular blocklength. """
        if length < 4:
            return '0' * 4 + 'f' * 60  # Use same difficulty for first few blocks.

        def targetTimesFloat(target, number):
            a = int(str(target), 16)
            b = int(a * number)  # this should be rational multiplication followed by integer estimation
            return tools.buffer_(str(hex(b))[2: -1], 64)

        def multiply_things(things):
            out = 1
            while len(things) > 0:
                out = out * things[0]
                things = things[1:]
            return out

        def weights(length):  # uses float
            # returns from small to big
            out = memoized_weights[:length]
            out.reverse()
            return out

        def estimate_target():
            """
            We are actually interested in the average number of hashes required to
            mine a block. number of hashes required is inversely proportional
            to target. So we average over inverse-targets, and inverse the final
            answer. """

            def sumTargets(l):
                if len(l) < 1:
                    return 0
                while len(l) > 1:
                    l = [hex_sum(l[0], l[1])] + l[2:]
                return l[0]

            targets = self.recent_blockthings('targets', custom.history_length)
            w = weights(len(targets))  # should be rat instead of float
            tw = sum(w)
            targets = map(hex_invert, targets)

            def weighted_multiply(i):
                return targetTimesFloat(targets[i], w[i] / tw)  # this should use rat division instead

            weighted_targets = [weighted_multiply(i) for i in range(len(targets))]
            return hex_invert(sumTargets(weighted_targets))

        def estimate_time():
            times = self.recent_blockthings('times', custom.history_length)
            times = map(Decimal, times)
            block_lengths = [times[i] - times[i - 1] for i in range(1, len(times))]
            w = weights(len(block_lengths))  # Geometric weighting
            tw = sum(w)
            return sum([w[i] * block_lengths[i] / tw for i in range(len(block_lengths))])

        retarget = estimate_time() / custom.blocktime
        return targetTimesFloat(estimate_target(), retarget)

