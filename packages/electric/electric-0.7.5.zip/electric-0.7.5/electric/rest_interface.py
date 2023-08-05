import logging

from flask import request
from flask_restful import Resource, abort
from werkzeug.exceptions import BadRequest

from zmq_marshall import ZMQCommsManager
from electric.models import Operation
from electric.models import ObjectNotFoundException, SystemStorage, Preset, PresetIndex

logger = logging.getLogger('electric.app.{0}'.format(__name__))
comms = ZMQCommsManager()

RETRY_LIMIT = 1


def connection_state_dict(exc=None):
    """
    Returns a dict that wraps up the information provided by the exception as well as
    the connection state of the charger
    """

    state = "connected"
    if exc is not None and isinstance(exc, Exception):
        state = "disconnected"

    value = {
        "charger_presence": state
    }

    if exc is not None:
        value.update({"exception": str(exc)})

    return value


# def retry_request(func):
#     def wrapper(self, *args, **kwargs):
#         # with evil_global.lock:
#         retry = 0
#         while retry < RETRY_LIMIT:
#             try:
#                 return func(self, *args, **kwargs)
#
#             except ObjectNotFoundException as e:
#                 abort(404, message=e.message)
#
#             except BadRequest as badRequest:
#                 # Just return it, it's a validation failure
#                 raise badRequest
#
#             except ValueError as ve:
#                 raise ve
#
#             except Exception, ex:
#                 retry += 1
#
#                 logger.warning("{0}/{3}, will try {4} again (count is at {1}/{2})".format(ex,
#                                                                                           retry,
#                                                                                           RETRY_LIMIT,
#                                                                                           type(ex),
#                                                                                           str(self) + "." + str(func)))
#
#                 # If the charger isn't plugged in. This could fail.
#                 if retry >= RETRY_LIMIT:
#                     logger.warning("retry limit exceeded, aborting the call to {0} completely".format(str(func)))
#                     return connection_state_dict(ex), 504
#
#     return wrapper


class StatusResource(Resource):
    # @retry_request
    def get(self):
        info = comms.get_device_info()

        obj = info.to_primitive()
        obj.update(connection_state_dict())

        return obj


class DialogCloseResource(Resource):
    # @retry_request
    def put(self, channel_id):
        channel = int(channel_id)
        if not (channel == 0 or channel == 1):
            return connection_state_dict("Channel number must be 0 or 1"), 403
        # comms.close_messagebox(channel)

        obj = comms.get_channel_status(channel).to_primitive()
        obj.update(connection_state_dict())

        return obj


class ChannelResource(Resource):
    # @retry_request
    def get(self, channel_id):
        try:
            channel = int(channel_id)
            if not (channel == 0 or channel == 1):
                return connection_state_dict("Channel number must be 0 or 1"), 403

            # get device status, so we know more about channel state
            device_info = comms.get_device_info()
            status = comms.get_channel_status(channel, device_info.device_id)
            if status is not None:
                if device_info is not None:
                    if channel == 0:
                        status.status = device_info.ch1_status
                    elif channel == 1:
                        status.status = device_info.ch2_status

                obj = status.to_primitive()
                obj.update(connection_state_dict())

                return obj

            return connection_state_dict("No status object returned from get_channel_status call"), 403
        except Exception, e:
            raise e


class ControlRegisterResource(Resource):
    # @retry_request
    def get(self):
        control = comms.get_control_register()

        # note: intentionally no connection state
        return control.to_primitive()


class ChargeResource(ControlRegisterResource):
    # @retry_request
    def put(self, channel_id, preset_memory_slot):
        device_status = comms.run_operation(Operation.Charge, int(channel_id), int(preset_memory_slot))
        comms.turn_off_logging()
        annotated_device_status = device_status.to_primitive()
        annotated_device_status.update(connection_state_dict())
        return annotated_device_status


class DischargeResource(ControlRegisterResource):
    # @retry_request
    def put(self, channel_id, preset_memory_slot):
        device_status = comms.run_operation(Operation.Discharge, int(channel_id), int(preset_memory_slot))
        annotated_device_status = device_status.to_primitive()
        annotated_device_status.update(connection_state_dict())
        return annotated_device_status


class StoreResource(ControlRegisterResource):
    # @retry_request
    def put(self, channel_id, preset_memory_slot):
        device_status = comms.run_operation(Operation.Storage, int(channel_id), int(preset_memory_slot))
        annotated_device_status = device_status.to_primitive()
        annotated_device_status.update(connection_state_dict())
        return annotated_device_status


class BalanceResource(ControlRegisterResource):
    # @retry_request
    def put(self, channel_id, preset_memory_slot):
        device_status = comms.run_operation(Operation.Balance, int(channel_id), int(preset_memory_slot))
        annotated_device_status = device_status.to_primitive()
        annotated_device_status.update(connection_state_dict())
        return annotated_device_status


class MeasureIRResource(ControlRegisterResource):
    # @retry_request
    def put(self, channel_id):
        device_status = comms.measure_ir(int(channel_id))
        annotated_device_status = device_status.to_primitive()
        annotated_device_status.update(connection_state_dict())
        return annotated_device_status


class StopResource(ControlRegisterResource):
    # @retry_request
    def put(self, channel_id):
        channel_number = int(channel_id)
        # We do this twice. Once to stop. 2nd time to get past the "STOPS" screen.
        operation_response = comms.stop_operation(channel_number).to_primitive()
        operation_response = comms.stop_operation(channel_number).to_primitive()
        operation_response.update(connection_state_dict())
        return operation_response


class SystemStorageResource(Resource):
    # @retry_request
    def get(self):
        syst = comms.get_system_storage()
        obj = syst.to_primitive()
        obj.update(connection_state_dict())

        return obj

    # @retry_request
    def put(self):
        json_dict = request.json
        del json_dict['charger_presence']
        system_storage_object = SystemStorage(json_dict)
        return comms.save_system_storage(system_storage_object)


class PresetResource(Resource):
    # @retry_request
    def get(self, preset_memory_slot):
        preset_memory_slot = int(preset_memory_slot)
        preset = comms.get_preset(preset_memory_slot)
        return preset.to_primitive()

    # @retry_request
    def delete(self, preset_memory_slot):
        # This will only, I think ... work for "at the end"
        preset_memory_slot = int(preset_memory_slot)
        logger.info("Try to delete preset at memory slot {0}".format(preset_memory_slot))
        return comms.delete_preset_at_index(preset_memory_slot)

    # @retry_request
    def put(self, preset_memory_slot):
        preset_memory_slot = int(preset_memory_slot)
        json_dict = request.json

        # Turn it into a Preset object
        preset = Preset(json_dict)

        logger.info("Asked to save preset to mem slot: {0} with {1}".format(preset_memory_slot, json_dict))
        return comms.save_preset_to_memory_slot(preset, preset_memory_slot)


class AddNewPresetResource(Resource):
    # @retry_request
    def put(self):
        json_dict = request.json

        # Turn it into a Preset object
        preset = Preset(json_dict)

        logger.info("Asked to add a new preset: {0}".format(json_dict))
        return comms.add_new_preset(preset).to_native()


class PresetListResource(Resource):
    # @retry_request
    def get(self):
        preset_list = comms.get_full_preset_list()
        # TODO: Error handling

        all_presets = []
        for index in preset_list.range_of_presets():
            # Preset.index is the memory slot it's in, not the position within the index
            memory_slot_number = preset_list.indexes[index]
            preset = comms.get_preset(memory_slot_number)
            if preset.is_used or preset.is_fixed:
                try:
                    native = preset.to_native()
                    all_presets.append(native)
                except Exception, e:
                    logger.info("BOOM: " + e)

        return all_presets

    # @retry_request
    def post(self):
        pass


class PresetOrderResource(Resource):
    # @retry_request
    def get(self):
        preset_list = comms.get_full_preset_list()
        return preset_list.to_native()

    # @retry_request
    def post(self):
        json_dict = request.json
        preset_list = PresetIndex(json_dict)
        return comms.save_full_preset_list(preset_list)


