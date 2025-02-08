#!/usr/bin/env python3

import argparse
import logging
import ssl

import asyncio
from aioquic.h3.connection import H3_ALPN
from aioquic.quic.configuration import QuicConfiguration
from aiomoqt.types import ParamType
from aiomoqt.client import MOQTClient, connect
from aiomoqt.utils.logger import get_logger, set_log_level, QuicDebugLogger


def parse_args():
    parser = argparse.ArgumentParser(description='MOQT WebTransport Client')
    parser.add_argument('--host', type=str, default='localhost',
                        help='Host to connect to')
    parser.add_argument('--port', type=int, default=4433,
                        help='Port to connect to')
    parser.add_argument('--namespace', type=str, required=True,
                        help='Track namespace')
    parser.add_argument('--trackname', type=str, required=True,
                        help='Track name')
    parser.add_argument('--endpoint', type=str, required=True,
                        help='MOQT WT endpoint')
    parser.add_argument('--timeout', type=int, default=30,
                        help='How long to run before unsubscribing (seconds)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output')
    return parser.parse_args()


async def main(host: str, port: int, endpoint: str, namespace: str, trackname: str, timeout: int,  debug: bool):
    log_level = logging.DEBUG if debug else logging.INFO
    set_log_level(log_level)
    logger = get_logger(__name__)
    try:
        configuration = QuicConfiguration(
            alpn_protocols=H3_ALPN,
            is_client=True,
            verify_mode=ssl.CERT_NONE,
            quic_logger=QuicDebugLogger() if debug else None,
            secrets_log_file=open("/tmp/keylog.client.txt",
                                  "a") if debug else None
        )

        client = MOQTClient(host, port, endpoint=endpoint,
                            configuration=configuration, debug=debug)

        async with client.connect() as client_session:
            await asyncio.wait_for(client_session.initialize(), timeout=30)
            client_session.announce(namespace=namespace,
                                    parameters={ParamType.AUTHORIZATION_INFO: b"auth-token-123"})
            await asyncio.sleep(timeout)
            logger.info(f"still in context: {client_session.__class__.__name__}")

        logger.info(f"finished: client session: {client.__class__.__name__}")

    except asyncio.TimeoutError:
        logger.error("Operation timed out")
        raise

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(
        host=args.host,
        port=args.port,
        endpoint=args.endpoint,
        namespace=args.namespace,
        trackname=args.trackname,
        timeout=args.timeout,
        debug=args.debug
    ))
