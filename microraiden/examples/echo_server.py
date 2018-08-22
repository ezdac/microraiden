"""
This is dummy code showing how the minimal app could look like.
In his case we don't use a proxy, but directly a server
"""
import logging
import os
import click
from flask import request
from web3 import Web3, HTTPProvider

from microraiden.channel_manager import ChannelManager
from microraiden.make_helpers import make_channel_manager
from microraiden.constants import WEB3_PROVIDER_DEFAULT
from microraiden.config import NETWORK_CFG
from microraiden.proxy import PaywalledProxy
from microraiden.proxy.resources import Expensive
from microraiden.utils import get_private_key


log = logging.getLogger(__name__)


class StaticPriceResource(Expensive):
    def get(self, url: str, param: str):
        log.info('Resource requested: {} with param "{}"'.format(request.url, param))
        return param


class DynamicPriceResource(Expensive):
    def get(self, url: str, param: int):
        log.info('Resource requested: {} with param "{}"'.format(request.url, param))
        return param

    def price(self):
        return int(request.view_args['param'])


@click.command()
@click.option(
    '--private-key',
    required=True,
    help='The server\'s private key path.',
    type=str
)
@click.option(
    '--web3-url',
    default=WEB3_PROVIDER_DEFAULT,
    help='URL for the blockchain node (web3)',
    type=str
)
def main(private_key: str, web3_url: str):
    private_key = get_private_key(private_key)
    web3 = Web3(HTTPProvider(web3_url))
    run(private_key, web3=web3)


def run(
        private_key: str,
        state_file_path: str = os.path.join(click.get_app_dir('microraiden'), 'echo_server.db'),
        channel_manager: ChannelManager = None,
        join_thread: bool = True,
        web3: Web3 = None,
):
    dirname = os.path.dirname(state_file_path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    # set up a paywalled proxy
    # arguments are:
    #  - private key to use for receiving funds
    #  - file for storing state information (balance proofs)
    if web3 is None:
        web3 = Web3(HTTPProvider(WEB3_PROVIDER_DEFAULT))
    if channel_manager is None:
        NETWORK_CFG.set_defaults(int(web3.version.network))
        channel_manager = make_channel_manager(
            private_key,
            NETWORK_CFG.CHANNEL_MANAGER_ADDRESS,
            state_file_path,
            web3
        )
    app = PaywalledProxy(channel_manager)

    # Add resource defined by regex and with a fixed price of 1 token.
    app.add_paywalled_resource(
        StaticPriceResource,
        "/echofix/<string:param>",
        price=5
    )
    # Resource with a price determined by the second parameter.
    app.add_paywalled_resource(
        DynamicPriceResource,
        "/echodyn/<int:param>"
    )

    # Start the app. proxy is a WSGI greenlet, so you must join it properly.
    app.run(debug=True, host='0.0.0.0')

    if join_thread:
        app.join()
    else:
        return app
    # Now use echo_client to get the resources.


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
