import zmq, logging, sys, os
import zmq.utils.win32

from comms_layer import ChargerCommsManager
from router import route_message
from electric.models import testing_control

logger = logging.getLogger('electric.worker')

# construct ZMQ context for comms, with a single REQUEST endpoint
ctx = zmq.Context()
socket = ctx.socket(zmq.REP)

listen_on = os.environ.get("ELECTRIC_WORKER_LISTEN", "tcp://0.0.0.0:5001")
socket.bind(listen_on)

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

charger = ChargerCommsManager()


def stop_application():
    socket.close()
    ctx.term()
    sys.exit(0)


def run_worker():
    logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    with zmq.utils.win32.allow_interrupt(stop_application):
        logger.warn("iCharger USB reader worker listening on: %s", listen_on)

        try:
            while True:
                socks = dict(poller.poll())

                if socket in socks:
                    message = socket.recv_pyobj()

                    if "method" not in message:
                        logger.warn("method name not specified, ignoring {0}".format(message))
                        message["exception"] = IOError("no method specified in message - rejecting request")
                    else:
                        method = message["method"]

                        args = None
                        if "args" in message:
                            args = message["args"]

                        if "testing-control" in message:
                            tc = message["testing-control"]
                            testing_control.usb_device_present = tc.usb_device_present
                            testing_control.modbus_read_should_fail = tc.modbus_read_should_fail
                            testing_control.modbus_write_should_fail = tc.modbus_write_should_fail

                        message_log = "message: {0}/{1} with args: {2}".format(message["tag"], method, args)

                        try:
                            logger.info("executing message: {0}".format(message_log))
                            message["response"] = route_message(charger, method, args)
                        except Exception, e:
                            logger.error("EXCEPTION during routing/execution for : {0}, {1}".format(message_log, e))
                            message["raises"] = e

                        try:
                            # potentially; the receiver goes away - before we are finished sending -
                            logger.info("sending response for: {0}".format(message_log))
                            socket.send_pyobj(message)
                            logger.info("sent response for: {0}".format(message_log))
                        except Exception, e:
                            logger.error("unable to send response for {0}, {1}".format(message_log, e))

        except KeyboardInterrupt:
            logger.info("Ctrl-C interrupted worker - aborting...")


if __name__ == "__main__":
    run_worker()