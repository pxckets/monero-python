from . import prio
from .transaction import PaymentManager


class Account(object):
    """Oscillate account.

    Provides interface to operate on a wallet's account.

    Accounts belong to a :class:`Wallet <oscillate.wallet.Wallet>` and act like
    separate sub-wallets. No funds can be moved between accounts off-chain
    (without a transaction).

    :param backend: a wallet backend
    :param index: the account's index within the wallet
    :param label: optional account label as `str`
    """
    index = None
    wallet = None
    label = None

    def __init__(self, backend, index, label=None):
        self.index = index
        self.label = label
        self._backend = backend
        self.incoming = PaymentManager(index, backend, 'in')
        self.outgoing = PaymentManager(index, backend, 'out')

    def balances(self):
        """
        Returns a tuple of balance and unlocked balance.

        :rtype: (Decimal, Decimal)
        """
        return self._backend.balances(account=self.index)

    def balance(self, unlocked=False):
        """
        Returns specified balance.

        :param unlocked: if `True`, return the unlocked balance, otherwise return total balance
        :rtype: Decimal
        """
        return self._backend.balances(account=self.index)[1 if unlocked else 0]

    def address(self):
        """
        Return account's main address.

        :rtype: :class:`SubAddress <oscillate.address.SubAddress>`
        """
        return self._backend.addresses(account=self.index)[0]

    def addresses(self):
        """
        Returns all addresses of the account.

        :rtype: list
        """
        return self._backend.addresses(account=self.index)

    def new_address(self, label=None):
        """
        Creates a new address.

        :param label: address label as `str`
        :rtype: :class:`SubAddress <oscillate.address.SubAddress>`
        """
        return self._backend.new_address(account=self.index, label=label)

    def transfer(self, address, amount,
            priority=prio.NORMAL, payment_id=None, unlock_time=0,
            relay=True):
        """
        Sends a transfer. Returns a list of resulting transactions.

        :param address: destination :class:`Address <oscillate.address.Address>` or subtype
        :param amount: amount to send
        :param priority: transaction priority, implies fee. The priority can be a number
                    from 1 to 4 (unimportant, normal, elevated, priority) or a constant
                    from `oscillate.prio`.
        :param payment_id: ID for the payment (must be None if
                        :class:`IntegratedAddress <oscillate.address.IntegratedAddress>`
                        is used as the destination)
        :param unlock_time: the extra unlock delay
        :param relay: if `True`, the wallet will relay the transaction(s) to the network
                        immediately; when `False`, it will only return the transaction(s)
                        so they might be broadcasted later
        :rtype: list of :class:`Transaction <oscillate.transaction.Transaction>`
        """
        return self._backend.transfer(
            [(address, amount)],
            priority,
            payment_id,
            unlock_time,
            account=self.index,
            relay=relay)

    def transfer_multiple(self, destinations,
            priority=prio.NORMAL, payment_id=None, unlock_time=0,
            relay=True):
        """
        Sends a batch of transfers. Returns a list of resulting transactions.

        :param destinations: a list of destination and amount pairs:
                    [(:class:`Address <oscillate.address.Address>`, `Decimal`), ...]
        :param priority: transaction priority, implies fee. The priority can be a number
                    from 1 to 4 (unimportant, normal, elevated, priority) or a constant
                    from `oscillate.prio`.
        :param payment_id: ID for the payment (must be None if
                    :class:`IntegratedAddress <oscillate.address.IntegratedAddress>`
                    is used as the destination)
        :param unlock_time: the extra unlock delay
        :param relay: if `True`, the wallet will relay the transaction(s) to the network
                    immediately; when `False`, it will only return the transaction(s)
                    so they might be broadcast later
        :rtype: list of transaction and amount pairs:
                [(:class:`Transaction <oscillate.transaction.Transaction>`, `Decimal`), ...]
        """
        return self._backend.transfer(
            destinations,
            priority,
            payment_id,
            unlock_time,
            account=self.index,
            relay=relay)

    def sweep_all(self, address, priority=prio.NORMAL, payment_id=None,
            subaddr_indices=None, unlock_time=0, relay=True):
        """
        Sends all unlocked balance to an address. Returns a list of resulting transactions.

        :param address: destination :class:`Address <oscillate.address.Address>` or subtype
        :param priority: transaction priority, implies fee. The priority can be a number
                    from 1 to 4 (unimportant, normal, elevated, priority) or a constant
                    from `oscillate.prio`.
        :param payment_id: ID for the payment (must be None if
                    :class:`IntegratedAddress <oscillate.address.IntegratedAddress>`
                    is used as the destination)
        :param subaddr_indices: a sequence of subaddress indices to sweep from. Empty sequence
                    or `None` means sweep all positive balances.
        :param unlock_time: the extra unlock delay
        :param relay: if `True`, the wallet will relay the transaction(s) to the network
                    immediately; when `False`, it will only return the transaction(s)
                    so they might be broadcast later
        :rtype: list of :class:`Transaction <oscillate.transaction.Transaction>`
        """
        return self._backend.sweep_all(
            address,
            priority,
            payment_id,
            subaddr_indices,
            unlock_time,
            account=self.index,
            relay=relay)
