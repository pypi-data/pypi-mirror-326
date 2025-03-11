# -*- coding: UTF-8 -*-
'''
@File    :   xldriver.py
@Time    :   2025/01/06 15:30:00
@Author  :   Jiajie Liu
@Version :   1.0
@Contact :   ljj26god@163.com
@Desc    :   This file reads dll file from vector official website and utilize necessary functions for sending CAN messages.
'''

import ctypes
import logging
from simpleCan.util import dataStructure as ds
import os

util_path = os.path.dirname(os.path.abspath(__file__))
simpleCan_path = os.path.dirname(util_path)
dll_file_path = os.path.join(simpleCan_path, 'dll_file')
dll_path = os.path.join(dll_file_path,'vxlapi64.dll')
_xlapi_dll = ctypes.windll.LoadLibrary(dll_path)
libc = ctypes.CDLL("msvcrt.dll")

# initialize functions
xlOpenDriver = _xlapi_dll.xlOpenDriver

xlGetDriverConfig = _xlapi_dll.xlGetDriverConfig

xlGetApplConfig = _xlapi_dll.xlGetApplConfig

xlGetChannelMask = _xlapi_dll.xlGetChannelMask

xlOpenPort = _xlapi_dll.xlOpenPort
xlActivateChannel = _xlapi_dll.xlActivateChannel

xlCanTransmit = _xlapi_dll.xlCanTransmit
xlCanTransmit.argtypes = [
    ds.XLportHandle,
    ds.XLaccessMark,
    ctypes.POINTER(ctypes.c_uint),
    ctypes.POINTER(ds.XLevent),
]
xlCanTransmit.restype = ds.XLstatus

xlReceive = _xlapi_dll.xlReceive
xlReceive.argtypes = [
    ds.XLportHandle,
    ctypes.POINTER(ctypes.c_uint),
    ctypes.POINTER(ds.XLevent),
]

xlCanReceive = _xlapi_dll.xlCanReceive
xlCanReceive.argtypes = [
    ds.XLportHandle,
    ctypes.POINTER(ds.XLcanRxEvent),
]

xlDeactivateChannel = _xlapi_dll.xlDeactivateChannel
xlClosePort = _xlapi_dll.xlClosePort
xlCloseDriver = _xlapi_dll.xlCloseDriver


xlGetErrorString = _xlapi_dll.xlGetErrorString

libc.memset.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t]
libc.memset.restype = ctypes.c_void_p

######################################################################################

appName = ctypes.create_string_buffer(b'CANalyzer')
pAppName = ctypes.pointer(appName)
appChannel = ctypes.c_uint()
HwType = ctypes.c_uint()
pHwType = ctypes.pointer(HwType)
HwIndex = ctypes.c_uint()
pHwIndex = ctypes.pointer(HwIndex)
HwChannel = ctypes.c_uint()
pHwChannel = ctypes.pointer(HwChannel)
busTypex = ctypes.c_uint()

xldriverConfig = ds.XLdriverConfig()
pxldriverConfig = ctypes.pointer(xldriverConfig)

portHandle = ds.XLportHandle()
pPortHandle = ctypes.pointer(portHandle)

userName = ds.userName
channelMask = ctypes.c_uint()
permissionMask = ctypes.c_uint64()
pPermissionMask = ctypes.pointer(permissionMask)
rx_queue_size = ds.rx_queue_size
xlInterfaceVersion = ds.xlInterfaceVersion
busType = ds.busType

XLeventTag_transmit = ds.XLeventTag_transmit
flags = ds.flags
activate_channel_flag = ds.activate_channel_flag
dlc = ds.dlc
def sendMessage(messageID, data, messageCount = 1):
    canID = ds.XL_CAN_EXT_MSG_ID | messageID
    myXLevent = (ds.XLevent * messageCount)()
    message_count = ctypes.c_uint(messageCount)
    try:
        libc.memset(myXLevent, 0, ctypes.sizeof(myXLevent))
        for i in range(messageCount):
            myXLevent[i].tag = XLeventTag_transmit
            myXLevent[i].tagData.msg.id = canID
            myXLevent[i].tagData.msg.flags = flags
            for j in range(len(data)):
                myXLevent[i].tagData.msg.data[j] = data[j]
            myXLevent[i].tagData.msg.dlc = dlc
        result = xlCanTransmit(portHandle, channelMask, message_count, myXLevent)
        if result == 0:
            logging.info('send message ' + str(hex(messageID)) + ' result ' + str(result))
        else:
            logging.error('send message ' + str(hex(messageID)) + ' result ' + str(result))
    except Exception as e:
        logging.error(f"Error: {e}")

def recvMessage() -> ds.ReceivedCanMessage:
    xLevent = ds.XLevent()
    pxLevent = ctypes.pointer(xLevent)
    eventCount = ctypes.c_uint(1)
    pEventCount = ctypes.pointer(eventCount)
    xlstatus = xlReceive(portHandle, pEventCount, pxLevent)
    if xlstatus == 0:
        msgID = hex(xLevent.tagData.msg.id & 0x1FFFFFFF)
        msgData = [hex(value) for value in list(xLevent.tagData.msg.data)]
        logging.info('received message ' + str(msgID))
        return ds.ReceivedCanMessage(id=msgID, data=msgData)


def setup():
    xlstatus = xlOpenDriver()
    logging.critical('open driver result is ' + str(xlstatus))

    xlstatus = xlGetDriverConfig(pxldriverConfig)
    logging.critical('get driver config result is ' + str(xlstatus))
    logging.critical('channelIndex value is ' + str(hex(xldriverConfig.channel[0].channelIndex)))
    logging.critical('channelMask value is ' + str(hex(xldriverConfig.channel[0].channelMask)))
    logging.critical('channelCapabilities value is ' + str(hex(xldriverConfig.channel[0].channelCapabilities)))
    logging.critical('channelBusCapabilities value is ' + str(hex(xldriverConfig.channel[0].channelBusCapabilities)))

    xlstatus = xlGetApplConfig(pAppName, appChannel, pHwType, pHwIndex, pHwChannel, busTypex)
    logging.critical('get appl config result is ' + str(xlstatus))
    logging.critical('hardware type is ' + ds.get_hwtype_name(HwType.value))

    global channelMask
    channelMask = xlGetChannelMask(HwType, HwIndex, HwChannel)
    logging.critical('channel mask is %d', channelMask)


    xlstatus = xlOpenPort(pPortHandle,
                          userName,
                          channelMask,
                          pPermissionMask,
                          rx_queue_size,
                          xlInterfaceVersion,
                          busType)
    assert xlstatus != -1
    logging.critical('open port result is ' + str(xlstatus))
    xlstatus = xlActivateChannel(portHandle,
                                 channelMask,
                                 busType,
                                 activate_channel_flag)
    logging.critical('Activate channel result is ' + str(xlstatus))
def teardown():
    xlstatus = xlDeactivateChannel(portHandle, channelMask)
    logging.critical('deactivate channel result is ' + str(xlstatus))

    xlstatus = xlClosePort(portHandle)
    logging.critical('close port result is ' + str(xlstatus))

    xlstatus = xlCloseDriver()
    logging.critical('close driver result is ' + str(xlstatus))








