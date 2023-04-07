

import socket
import io
import time
import struct
import back
import back.logging


def send(sock: socket.socket, data: bytes):
    """
    Implementation of the sending logic for sending data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.
        data -- A bytes object, containing the data to send over the network.
    """

    # Naive implementation where we chunk the data to be sent into
    # packets as large as the network will allow, and then send them
    # over the network, pausing half a second between sends to let the
    # network "rest" :)

    # logger = back.logging.get_logger("back-sender")
    # chunk_size = back.MAX_PACKET
    # pause = .1
    # offsets = range(0, len(data), back.MAX_PACKET)
    # for chunk in [data[i:i + chunk_size] for i in offsets]:
    #     sock.send(chunk)
    #     logger.info("Pausing for %f seconds", round(pause, 2))
    #     time.sleep(pause)
    logger = back.logging.get_logger("back-sender")
    chunk_size = back.MAX_PACKET - 6
    est_trans = 0.01
    dev_trans = 0
    pause = 0.01
    offsets = range(0, len(data), chunk_size)
    lpi = len(data) / chunk_size
    sendC = 0

    for chunk in [data[i:i + chunk_size] for i in offsets]:
        sendC = sendC + 1
        if sendC <= lpi:
            packet = struct.pack('hhh', sendC, 0, 0) + chunk
        else:
            packet = struct.pack('hhh', sendC, 0, 1) + chunk
        while 1:
            # sock.send(packet)
            # logger.info("Pausing for %f seconds", round(pause, 2))
            # begin = time.time()
            # sock.settimeout(pause)
            # ackPckt = sock.recv(6)
            # pcktH = struct.unpack('hhh', ackPckt)
            # if pcktH[0] != sendC:
            #     continue
            # end = time.time()
            # sample_trans = end - begin
            # est_trans = (1-0.125) * est_trans + (0.125 * sample_trans)
            # dev_trans = (1-0.25) * dev_trans + (0.25 * dev_trans)
            # pause = est_trans + (4 * dev_trans)
            # break
            try:
                sock.send(packet)
                logger.info("Pausing for %f seconds", round(pause, 2))
                begin = time.time()
                sock.settimeout(pause)
                ackPckt = sock.recv(6)
                pcktH = struct.unpack('hhh', ackPckt)
                if pcktH[0] != sendC:
                    continue
                end = time.time()
                sample_trans = end - begin
                est_trans = (1-0.125) * est_trans + (0.125 * sample_trans)
                dev_trans = (1-0.25) * dev_trans + (0.25 * dev_trans)
                pause = est_trans + (4 * dev_trans)
                break
            except socket.timeout:
                continue

        # time.sleep(pause)


def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """
    logger = back.logging.get_logger("back-receiver")
    # Naive solution, where we continually read data off the socket
    # until we don't receive any more data, and then return.
    num_bytes = 0
    cnt = 1
    while 1:
        info = sock.recv(back.MAX_PACKET)

        if info:
            logger.info("Received %d bytes", len(info))
            pcktH = struct.unpack('hhh', info[0:6])
            infoLen=len(info)
            # if infoLen != back.MAX_PACKET and pcktH[2] != 1:
            #     continue
            if pcktH[2]!=1:
                packet = struct.pack('hhh', pcktH[0], 1, 0)
            else:
                packet = struct.pack('hhh', pcktH[0], 1, 1)
            sock.send(packet)
            if pcktH[0] ==cnt:
                
                cnt = cnt + 1
                info = info[6:]
                dest.write(info)
                num_bytes += len(info)
                dest.flush()
            else:
                continue
        else:
            break
    return num_bytes
