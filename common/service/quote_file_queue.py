import hashlib
import random
import time
import json
from common.service.redis_client import redis

QUEUE_KEY = "quote_file_queue"
QUEUE_HASHES_KEY = "queue_hashes"
SLOW_QUEUE_KEY = "slow_quote_file_queue"
SLOW_QUEUE_HASHES_KEY = "slow_queue_hashes"
r = redis

def add_to_queue(data, file_hash, channel="default"):
    """添加JSON到队列尾部，使用提供的file_hash作为唯一标识

    Args:
        data: 要存储的JSON数据
        file_hash: 文件的哈希值，作为唯一标识
        channel: 队列通道，默认为"default"，可选"slow"

    Returns:
        bool: True表示成功添加，False表示已存在(未添加)
    """
    # 检查是否已存在相同hash的条目（两个通道都检查）
    if r.hexists(QUEUE_HASHES_KEY, file_hash) or r.hexists(SLOW_QUEUE_HASHES_KEY, file_hash):
        print("The file already exists in the queue.")
        return False

    queue_item = {
        "id": file_hash,  # 使用file_hash作为ID
        "data": data,
        "timestamp": time.time()
    }
    qhk = QUEUE_HASHES_KEY
    qk = QUEUE_KEY
    if channel == "slow":
        qhk = SLOW_QUEUE_HASHES_KEY
        qk = SLOW_QUEUE_KEY
    # 使用事务确保原子性操作
    with r.pipeline() as pipe:
        try:
            pipe.watch(qhk)

            # 再次检查，防止在watch期间被其他客户端修改
            if pipe.hexists(qhk, file_hash):
                pipe.unwatch()
                return False

            # 开始事务
            pipe.multi()
            pipe.hset(qhk, file_hash, "1")  # 记录已存在的hash
            pipe.rpush(qk, json.dumps(queue_item))
            pipe.execute()
            return True
        except r.exceptions.WatchError:
            # 如果被其他客户端修改，重试
            return add_to_queue(data, file_hash, channel)

def get_from_queue():
    """从队列头部获取并移除一个JSON对象，优先从优先通道获取

    Returns:
        tuple: (file_hash, data, channel) 如果队列不为空，否则返回 (None, None, None)
               其中channel表示数据来自哪个队列("default"或"slow")
    """
    # 先尝试从优先通道获取
    item_json = r.lpop(QUEUE_KEY)
    channel = "default"

    if not item_json:
        # 如果优先通道为空，尝试慢速通道
        item_json = r.lpop(SLOW_QUEUE_KEY)
        channel = "slow"
        if not item_json:
            return None, None, None

    try:
        item = json.loads(item_json)
        file_hash = item.get("id")
        data = item.get("data")

        # 从对应的已存在哈希记录中移除
        r.hdel(QUEUE_HASHES_KEY if channel == "default" else SLOW_QUEUE_HASHES_KEY, file_hash)

        return file_hash, data, channel
    except json.JSONDecodeError:
        print(f"Invalid JSON data in queue: {item_json}")
        return None, None, None

def peek_queue():
    """查看队列头部元素但不移除，优先查看优先通道

    Returns:
        tuple: (file_hash, data, channel) 如果队列不为空，否则返回 (None, None, None)
               其中channel表示数据来自哪个队列("default"或"slow")
    """
    # 先检查优先通道
    item_json = r.lindex(QUEUE_KEY, 0)
    channel = "default"

    if not item_json:
        # 如果优先通道为空，检查慢速通道
        item_json = r.lindex(SLOW_QUEUE_KEY, 0)
        channel = "slow"
        if not item_json:
            return None, None, None

    try:
        item = json.loads(item_json)
        return item.get("id"), item.get("data"), channel
    except json.JSONDecodeError:
        print(f"Invalid JSON data in queue: {item_json}")
        return None, None, None

def get_queue_length():
    """获取两个队列的总长度

    Returns:
        int: 两个队列中的元素总数
    """
    return r.llen(QUEUE_KEY) + r.llen(SLOW_QUEUE_KEY)

def is_file_in_queue(file_hash):
    """检查指定的 file_hash 是否在任一队列中

    Args:
        file_hash (str): 要检查的文件哈希值

    Returns:
        bool: True 如果存在任一队列中，False 如果不存在
    """
    # 检查优先通道的hash集合
    if r.hexists(QUEUE_HASHES_KEY, file_hash):
        return True

    # 检查慢速通道的hash集合
    if r.hexists(SLOW_QUEUE_HASHES_KEY, file_hash):
        return True

    # 如果hash集合不同步，遍历两个队列验证
    for qk in [QUEUE_KEY, SLOW_QUEUE_KEY]:
        queue_items = r.lrange(qk, 0, -1)
        for item_json in queue_items:
            try:
                item = json.loads(item_json)
                if item.get("id") == file_hash:
                    return True
            except json.JSONDecodeError:
                continue

    return False


def get_file_position(file_hash):
    """获取指定 file_hash 在队列中的位置信息

    Args:
        file_hash (str): 要查找的文件哈希值

    Returns:
        tuple: (channel, channel_position, global_position)
               channel: "default"或"slow"，表示所在队列
               channel_position: 在当前队列中的位置(从0开始)
               global_position: 在整个队列系统中的位置(优先队列长度+慢速队列位置)
               如果不在队列中返回 (None, -1, -1)
    """
    # 先检查优先通道
    queue_items = r.lrange(QUEUE_KEY, 0, -1)
    for index, item_json in enumerate(queue_items):
        try:
            item = json.loads(item_json)
            if item.get("id") == file_hash:
                return "default", index, index
        except json.JSONDecodeError:
            continue

    # 获取优先通道长度
    priority_len = r.llen(QUEUE_KEY)

    # 检查慢速通道
    queue_items = r.lrange(SLOW_QUEUE_KEY, 0, -1)
    for index, item_json in enumerate(queue_items):
        try:
            item = json.loads(item_json)
            if item.get("id") == file_hash:
                return "slow", index, priority_len + index
        except json.JSONDecodeError:
            continue

    return None, -1, -1


def simulate_add_files(num_files=5, channel="default"):
    """模拟添加多个文件到队列"""
    added_files = []

    for i in range(num_files):
        # 随机生成文件类型 (1或2)
        file_type = random.choice([1, 2])

        # 生成模拟文件路径
        file_path = f"/data/{'doc' if file_type == 1 else 'img'}_{i + 1}.{'txt' if file_type == 1 else 'jpg'}"

        # 生成文件哈希 (实际项目应该用真实文件内容计算)
        file_hash = hashlib.md5(file_path.encode()).hexdigest()

        # 构建数据字典
        file_data = {
            "path": file_path,
            "type": file_type,
            "other_info": f"sample_{i + 1}"  # 可以添加其他模拟字段
        }

        # 调用现有的add_to_queue函数
        if add_to_queue(file_data, file_hash, channel=channel):
            added_files.append({
                "hash": file_hash,
                "path": file_path,
                "type": file_type
            })

    print(f"\n模拟添加完成，成功添加 {len(added_files)}/{num_files} 个文件")
    for file in added_files:
        print(f" - {file['path']} (类型: {file['type']}, 哈希: {file['hash'][:8]}...)")

    return added_files

if __name__ == '__main__':
    print(get_file_position("d47e67d33d69561d605ca10c34e5f9d9"))