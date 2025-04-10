import time


class SnowflakeIDGenerator:
    def __init__(self, datacenter_id, worker_id, sequence=0):
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = sequence
        self.last_timestamp = -1

        # 位移长度
        self.worker_id_bits = 5
        self.datacenter_id_bits = 5
        self.sequence_bits = 12

        # 最大值
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)

        # 位移
        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits

        # Twitter的epoch时间戳开始时间
        self.epoch = 1288834974657

    def _time_gen(self):
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp):
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()
        return timestamp

    def generate_id(self):
        timestamp = self._time_gen()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id")

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.max_sequence
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        id = ((timestamp - self.epoch) << self.timestamp_shift) | \
             (self.datacenter_id << self.datacenter_id_shift) | \
             (self.worker_id << self.worker_id_shift) | \
             self.sequence

        return id