import grpc
import p4.v1.p4runtime_pb2 as p4runtime_pb2
import p4.v1.p4runtime_pb2_grpc as p4runtime_pb2_grpc
import os
import sys
import argparse
import utils.switch as switch
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils/"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))
import bmv2
from utils.convert import encodeNum
import helper
from concurrent import futures
from google.protobuf import empty_pb2

def writeIpv4Rules(p4info_helper, sw_id, dst_ip_addr, port):
    table_entry = p4info_helper.buildTableEntry(
            table_name="MyIngress.ipv4_lpm",
            match_fields={"hdr.ipv4.dstAddr": (dst_ip_addr, 32)},
            action_name="MyIngress.ipv4_forward",
            action_params={"port": port},
            )
    print("***********************here")
    print(table_entry)
    print("***********************pppppppppppppp")
    sw_id.WriteTableEntry(table_entry)
    print("Installed ingress forwarding rule on %s" % sw_id.name)

def readTableRules(p4info_helper, sw):
    """
    Reads the table entries from all tables on the switch.

    :param p4info_helper: the P4Info helper
    :param sw: the switch connection
    """
    print("\n----- Reading tables rules for %s -----" % sw.name)
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
            table_name = p4info_helper.get_tables_name(entry.table_id)
            print("%s: " % table_name, end="")
            for m in entry.match:
                print(
                    p4info_helper.get_match_field_name(table_name, m.field_id), end=""
                )
                print("%r" % (p4info_helper.get_match_field_value(m),), end="")
            action = entry.action.action
            action_name = p4info_helper.get_actions_name(action.action_id)
            print("-> action:%s with parameters:" % action_name, end="")
            for p in action.params:
                print(
                    " %s"
                    % p4info_helper.get_action_param_name(action_name, p.param_id),
                    end="",
                )
                print(" %r" % p.value, end="")
            print("")

class p4VisorToSwitch(p4runtime_pb2_grpc.P4RuntimeServicer):
    def __init__(self, switch, p4InfoFilePath, bmv2FilePath):
        #self.controller_channel = grpc.insecure_channel("0.0.0.0:61001")
        #self.controller_stub = p4runtime_pb2_grpc.P4RuntimeStub(self.controller_channel)
        #self.s1 = bmv2.Bmv2SwitchConnection(name="s1", address="172.18.0.2:50001",device_id=1)
        self.s1 = switch
        self.masterArbitrationResult = self.s1.MasterArbitrationUpdate()
        print("THIS THIS THIS")
        print(self.masterArbitrationResult)
        print("THAT THAT THAT")
        p4info_helper = helper.P4InfoHelper(p4InfoFilePath)
        self.setForwardingResult = self.s1.SetForwardingPipelineConfig(
            p4info=p4info_helper.p4info, bmv2_json_file_path=bmv2FilePath) #returns "None" but I think that's fine
        writeIpv4Rules(p4info_helper, sw_id=self.s1, dst_ip_addr="172.16.1.1", port=255)
        writeIpv4Rules(p4info_helper, sw_id=self.s1, dst_ip_addr="172.16.1.2", port=255)
        writeIpv4Rules(p4info_helper, sw_id=self.s1, dst_ip_addr="172.16.1.3", port=255)
        writeIpv4Rules(p4info_helper, sw_id=self.s1, dst_ip_addr="172.16.1.4", port=255)
        readTableRules(p4info_helper, self.s1)


    def MasterArbitrationUpdate(self, request, context):
        return self.masterArbitrationResult
    
    def SetForwardingPipelineConfig(self, request, context):
        print("****************")
        print("****************")
        print("****************")
        #self.s1.SetForwardingPipelineConfig(request, context)
        return p4runtime_pb2.SetForwardingPipelineConfigResponse()
        #return self.setForwardingResult
    
    def PacketIn(self, request, context):
        print("Packet In")
        for item in self.stream_msg_resp:
            for response in self.s1.PacketIn(item):
                yield response
    
    def PacketOut(self, request, context):
        print("PacketOut")
        print(request)
        response = self.s1.PacketOut(request)
        return response
    
    def Read(self, request, context):
        print("Reading")
        print(request)
        for response in self.s1.ReadTableEntries():
            yield response

    def Write(self, request, context):
        print("this")
        #print(request)
        print(request.updates[0].entity.table_entry)
        print(context.details)
        try:
            #response = self.s1.client_stub.Write(request, context)
            self.s1.WriteTableEntry(request.updates[0].entity.table_entry, context)
        except Exception as e:
            print(e)
        print("Here")
        return p4runtime_pb2.WriteResponse()
    
    def StreamChannel(self, request_iterator, context):
        for request in request_iterator:
            print("message recieved")
            msgType = request.WhichOneof('update')
            print(msgType)
            if (msgType == "arbitration"):
                response = self.MasterArbitrationUpdate(request, context)
                #p4info_helper = helper.P4InfoHelper(self.p4InfoFilePath)
                #self.s1.SetForwardingPipelineConfig(
            #p4info=p4info_helper.p4info, bmv2_json_file_path=self.bmv2FilePath
        #)
            else:
                print(msgType)
                response = self.PacketOut(request, context)
            print("Response recieved")
            yield response


class P4VisorToControllerrr(switch.SwitchConnection):
    def __init__(self, p4info_file_path, bmv2_file_path):
        self.p4info_helper = helper.P4InfoHelper(p4info_file_path)
        self.bmv2_file_path = bmv2_file_path
        
        


    def run(self):
        try:
            # Create a switch connection object for s1;
            # this is backed by a P4Runtime gRPC connection.
            # Also, dump all P4Runtime messages sent to switch to given txt files.
            s1 = bmv2.Bmv2SwitchConnection(
                name="s0",
                address="127.0.0.1:50001",
                device_id=1,
                proto_dump_file="p4runtime.log",
            )
        except KeyboardInterrupt:
            print(" Shutting down.")
        except grpc.RpcError as e:
            print("gRPC error")


def serving(p4InfoFilePath, bmv2FilePath):
    
    
    try:
        s1 = bmv2.Bmv2SwitchConnection(
            name="s0",
            address="127.0.0.1:50001",
            device_id=1,
            proto_dump_file="p4runtime.log",
        )
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        visorToSwitchObj = p4VisorToSwitch(s1, p4InfoFilePath, bmv2FilePath)
        p4runtime_pb2_grpc.add_P4RuntimeServicer_to_server(visorToSwitchObj, server)
        server.add_insecure_port('0.0.0.0:61001')
        server.start()
        print("Server started.")
        server.wait_for_termination()
    except KeyboardInterrupt:
        print(" Shutting down.")
    except grpc.RpcError as e:
        print("gRPC error")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="P4Runtime Controller")
    parser.add_argument(
        "--p4info",
        help="p4info proto in text format from p4c",
        type=str,
        action="store",
        required=False,
        default="./firmeware.p4info.txt",
    )
    parser.add_argument(
        "--bmv2-json",
        help="BMv2 JSON file from p4c",
        type=str,
        action="store",
        required=False,
        default="./simple.json",
    )
    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print("\np4info file %s not found!" % args.p4info)
        parser.exit(1)
    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print("\nBMv2 JSON file %s not found!" % args.bmv2_json)
        parser.exit(2)
    serving(args.p4info, args.bmv2_json)