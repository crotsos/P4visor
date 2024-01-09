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

class p4VisorToSwitch(p4runtime_pb2_grpc.P4RuntimeServicer):
    def __init__(self, switch, p4InfoFilePath, bmv2FilePath):
        #self.controller_channel = grpc.insecure_channel("0.0.0.0:61001")
        #self.controller_stub = p4runtime_pb2_grpc.P4RuntimeStub(self.controller_channel)
        #self.s1 = bmv2.Bmv2SwitchConnection(name="s1", address="172.18.0.2:50001",device_id=1)
        self.s1 = switch
        #self.p4InfoFilePath = p4InfoFilePath
        #self.bmv2FilePath = bmv2FilePath

    def MasterArbitrationUpdate(self, request, context):
        response = self.s1.MasterArbitrationUpdate(request)
        print("Now printing the MAU response")
        print(response)
        return response
    
    def SetForwardingPipelineConfig(self, request, context):
        #print(request)
        #print(self.s1)
        #response = self.s1.SetForwardingPipelineConfig(request)
        #print(response)
        return empty_pb2.Empty()
    
    def PacketIn(self, request, context):
        for item in self.stream_msg_resp:
            for response in self.s1.PacketIn(item):
                yield response
    
    def PacketOut(self, request, context):
        response = self.s1.PacketOut(request)
        return 0
    
    def ReadTableEntries(self, request, context):
        for response in self.s1.ReadTableEntries(request):
            yield response
    
    def WriteTableEntry(self, request, context):
        print(request)
        response = self.s1.WriteTableEntry(request)
        return response
    
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
                #response = self.PacketOut(request, context)
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