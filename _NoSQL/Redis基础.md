## 数据结构

![image-20181025134845829](../images/999999/image-20181025134845829.png)

### string（ 字符串）

#### 命令

1. 设置值：`set key value [ex seconds] [px milliseconds] [nx|xx]`

   - `ex seconds`：为键设置秒级过期时间 【相同：`setex`】
   - `px milliseconds`：键设置毫秒级过期时间
   - `nx`：键必须不存在， 才可以设置成功， 用于添加【相同：`setnx`】
   - `xx`：与nx相反， 键必须存在， 才可以设置成功， 用于更新

2. 获取值：`get key`

3. 批量设置值：`mset key value [key value ...]`

4. 批量获取值：`mget key [key ...]`

5. 计数：`incr key`

   - 值不是整数， 返回错误
   - 值不是整数， 返回错误
   - 键不存在， 按照值为0自增， 返回结果为1

   > 除了incr命令， Redis提供了
   >
   > decr（自减）
   >
   >  incrby（自增指定数字）
   > decrby（自减指定数字）
   >
   > incrbyfloat（自增浮点数）

6. 追加值：`append key value`

7. 字符串长度：`strlen key`。中文占3个字节

8. 设置并返回原值：`getset key value`

9. 设置指定位置的字符：`setrange key offeset value`

10. 获取部分字符串：`getrange key start end`

#### 命令时间复杂度

![image-20181026124028210](../images/999999/image-20181026124028210.png)

#### 内部编码

- int： 8个字节的长整型
- embstr： 小于等于39个字节的字符串
- raw： 大于39个字节的字符串

### hash（ 哈希） 

#### 命令时间复杂度

![image-20181026124857857](../images/999999/image-20181026124857857.png)

#### 内部编码

- **ziplist（ 压缩列表）** ： 当哈希类型元素个数小于`hash-max-ziplist-entries`配置（ 默认512个） 、 同时所有值都小于`hash-max-ziplist-value`配置（ 默认64字节） 时， Redis会使用ziplist作为哈希的内部实现， ziplist使用更加紧凑的结构实现多个元素的连续存储， 所以在节省内存方面比hashtable更加优秀
- **hashtable（ 哈希表）** ：当哈希类型无法满足ziplist的条件时， Redis会使用hashtable作为哈希的内部实现， 因为此时ziplist的读写效率会下降， 而hashtable的读写时间复杂度为O（ 1） 

### list（ 列表） 

#### 命令时间复杂度

![image-20181026125759520](../images/999999/image-20181026125759520.png)

#### 内部编码

- **ziplist（ 压缩列表）** ： 当列表的元素个数小于`list-max-ziplist-entries`配置（ 默认512个） ， 同时列表中每个元素的值都小于`list-max-ziplist-value`配置时（ 默认64字节） ， Redis会选用ziplist来作为列表的内部实现来减少内存的使用。
- **linkedlist（ 链表）** ： 当列表类型无法满足ziplist的条件时， Redis会使用linkedlist作为列表的内部实现
- **quicklist**：Redis3.2版本提供了quicklist内部编码， 简单地说它是以一个ziplist为节点的linkedlist， 它结合了ziplist和linkedlist两者的优势， 为列表类型提供了一种更为优秀的内部编码实现

### set（ 集合） 

#### 命令时间复杂度

![image-20181026130749816](../images/999999/image-20181026130749816.png)

#### 内部编码

- **intset（ 整数集合）** ： 当集合中的元素都是整数且元素个数小于`set-maxintset-entries`配置（ 默认512个） 时， Redis会选用intset来作为集合的内部实现， 从而减少内存的使用
- **hashtable（ 哈希表）** ： 当集合类型无法满足intset的条件时， Redis会使用hashtable作为集合的内部实现

### zset（ 有序集合） 

#### 命令时间复杂度

![image-20181026131230566](../images/999999/image-20181026131230566.png)

#### 内部编码

- **ziplist（ 压缩列表）** ： 当有序集合的元素个数小于`zset-max-ziplistentries`配置（ 默认128个） ， 同时每个元素的值都小于`zset-max-ziplist-value`配置（ 默认64字节） 时， Redis会用ziplist来作为有序集合的内部实现， ziplist可以有效减少内存的使用
- **skiplist（ 跳跃表）** ： 当ziplist条件不满足时， 有序集合会使用skiplist作为内部实现， 因为此时ziplist的读写效率会下降

> ### Bitmaps（ 位图）
>
> ### HyperLogLog
>
> ### GEO（ 地理信息定位）



## 命令

### 全局命令

- 查看全部键：`keys *`
- 键总数：`dbsize`。直接获取已经保存的键总数，时间复杂度O（1）
- 键是否存在：`exists key`
- 删除键：`del key`。删除成功返回删除的个数，删除的键不存在返回0
- 键过期：`expire key seconds`
- 查看键过期时间：`ttl`。大于等于0：代表未过期。-1：键没设置过期时间。-2：键不存在
- 键数据结构类型：`type key`
- 查看内部编码：`object encoding key` 
- 键重命名：`rename key newkey`
- 随机返回一个键：`randomkey`
- 夸库迁移：`migrate`
- 遍历key：`scan cursor [match pattern] [count number]`
  - **cursor**：是必需参数， 实际上cursor是一个游标， 第一次遍历从0开始， 每次scan遍历完都会返回当前游标的值， 直到游标值为0， 表示遍历结束
  - **match pattern**：是可选参数， 它的作用的是做模式的匹配， 这点和keys的模式匹配很像
  - **count number**：是可选参数， 它的作用是表明每次要遍历的键个数， 默认值是10， 此参数可以适当增大
- 删除 当前/全部 库的数据：`flushdb/flushall`

### 慢查询

1. `slowlog-log-slower-than`。单位微秒（ 1秒=1000毫秒=1000000微秒）。默认值10000
   - x > 0 记录超过阈值的命令。只统计命令的执行时间不会统计命令的排队时间
   - x = 0 记录所有的命令
   - x < 0 任何命令都不会进行记录
2. `slowlog-max-len`。保存慢查命令队列的长度。先进先出

``` shell
config set slowlog-log-slower-than 20000
config set slowlog-max-len 1000
# 将配置信息持久化存储
config rewrite
```

3. 获取慢查询日志`slowlog get [n]`

   ```Shell
   slowlog get
   1) 
   	1) (integer) 666 # 标识id
   	2) (integer) 1456786500 # 发生时间戳
   	3) (integer) 11615 # 命令耗时
   	4) # 执行命令和参数
   		1) "BGREWRITEAOF"
   2) 
   	1) (integer) 665
   	2) (integer) 1456718400
   	3) (integer) 12006
   	4)
   		1) "SETEX"
   		2) "video_info_200"
   		3) "300"
   		4) "2"
   ```

4. 获取慢查询队列长度`slowlog len`

5. 慢查询日志重置`slowlog reset`

### shell使用

#### redis-cli

- **-r（ repeat）**：代表将命令执行多次， 例如下面操作将会执行三次ping

  ```shell
  $ redis-cli -r 3 ping
  PONG
  PONG
  PONG
  ```

- **-i（interval）**：代表每隔几秒执行一次命令， 但是-i选项必须和-r选项一起使用

  ```shell
  $ redis-cli -r 5 -i 1 ping
  PONG
  PONG
  PONG
  PONG
  PONG
  ```

- **-x**：代表从标准输入（ stdin） 读取数据作为redis-cli的最后一个参数

  ``` shell
  $ echo "world" | redis-cli -x set hello
  ```

- **-c（ cluster）**:连接Redis Cluster节点时需要使用的， -c选项可以防止moved和ask异常

- **-a**：如果Redis配置了密码， 可以用-a（ auth） 选项， 有了这个选项就不需要手动输入auth命令

- **--scan和--pattern**：用于扫描指定模式的键， 相当于使用scan命

- **--slave**：把当前客户端模拟成当前Redis节点的从节点， 可以用来获取当前Redis节点的更新操作

- **--rdb**：会请求Redis实例生成并发送RDB持久化文件， 保存在本地

- **--pipe**：用于将命令封装成Redis通信协议定义的数据格式， 批量发送给Redis执行

- **--bigkeys**：使用scan命令对Redis的键进行采样， 从中找到内存占用比较大的键值， 这些键可能是系统的瓶颈

- **--eval**：用于执行指定Lua脚本

- **--latency**：有三个选项， 分别是--latency、 --latency-history、 --latency-dist。可以检测网络延迟

- **--stat**：可以实时获取Redis的重要统计信息

- **--raw和--no-raw**：要求命令的返回结果必须是原始的格式(--raw)

#### redis-server

- 检测当前操作系统能否提供1G的内存给Redis`redis-server --test-memory 1024`
- 启动：`./redis-server ../redis.conf`

#### redis-benchmark

> redis-benchmark-c100-n20000代表100各个客户端同时请求Redis

### 客户端连接池参数

![image-20181031133144611](../images/999999/image-20181031133144611.png)

### 客户端管理

- **列出与Redis服务端相连的所有客户端连接信息**

  ``` shell
  > client list
  id=15 addr=192.168.56.101:43568 fd=5 name= age=5 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=32768 obl=0 oll=0 omem=0 events=r cmd=client
  ```

  - **id**：客户端连接的唯一标识， 这个id是随着Redis的连接自增的， 重启Redis后会重置为0

  - **addr**：客户端连接的ip和端口

  - **fd**：socket的文件描述符， 与lsof命令结果中的fd是同一个， 如果fd=-1代表当前客户端不是外部客户端， 而是Redis内部的伪装客户端

  - **name**：客户端的名字

  - **qbuf、 qbuf-free**：分别代表当前客户端命令缓冲区的总容量和剩余容量。这个不可配置redis动态调整。当缓冲区超过1GB时，客户端会被关闭。输入缓冲区不受maxmemory控制

    > 可以使用`info clients`查看当前客户端的一个现状
    >
    > ``` shell
    > > info clients
    > # Clients
    > connected_clients:1
    > client_longest_output_list:0 # 代表输出缓冲区列表最大对象数
    > client_biggest_input_buf:0 # 代表最大的输入缓冲区
    > blocked_clients:0
    > ```

  - **obl、 oll、 omem**：obl代表固定缓冲区的长度（对象个数）。oll代表动态缓冲区列表的长度（对象个数）， omem代表使用的字节数

    > ​	输出缓冲区的容量可以通过参数 `client-output-buffer-limit` 来进行设置。按照客户端的不同分为三种： 普通客户端、 发布订阅客户端、 slave客户端。输出缓冲区也不会受到maxmemory的限制。
    >
    > ​	输出缓冲区由两部分组成： 固定缓冲区（ 16KB） 和动态缓冲区， 其中固定缓冲区返回比较小的执行结果， 而动态缓冲区返回比较大的结果。固定缓冲区使用的是字节数组， 动态缓冲区使用的是列表。 当固定缓冲区存满后会将Redis新的返回结果存放在动态缓冲区的队列中， 队列中的每个对象就是每个返回结果。

    > ```shell
    > client-output-buffer-limit <class> <hard limit> <soft limit> <soft seconds>
    > 
    > 	- <class>： 客户端类型， 分为三种。 a） normal： 普通客户端； b）slave： slave客户端， 用于复制； c） pubsub： 发布订阅客户端
    > 	- <hard limit>： 如果客户端使用的输出缓冲区大于<hard limit>， 客户端会被立即关闭
    > 	- <soft limit>和<soft seconds>： 如果客户端使用的输出缓冲区超过了<soft limit>并且持续了<soft limit>秒， 客户端会被立即关闭
    > 
    > redis默认配置：
    > 
    > client-output-buffer-limit normal 0 0 0
    > client-output-buffer-limit slave 256mb 64mb 60
    > client-output-buffer-limit pubsub 32mb 8mb 60
    > ```

    > 可以适当增大slave的输出缓冲区的， 如果master节点写入较大， slave客户端的输出缓冲区可能会比较大， 一旦slave客户端连接因为输出缓冲区溢出被kill， 会造成复制重连。

  - **age、idle**：分别代表当前客户端已经连接的时间（单位s）和最近一次的空闲时间。当age等于idle时，说明连接一直处于空闲状态

  - **flag**：用于标识当前客户端的类型

    ![image-20181031142509912](../images/999999/image-20181031142509912.png)

  - **multi**：当前事务中已执行命令个数

  - **events**：文件描述符事件。r和w分别代表客户端套接字刻可读、可写

  - **cmd**：当前客户端最后一次执行的命令，不包含参数

- **客户端的限制maxclients和timeout**

  1. 一旦连接数超过maxclients， 新的连接将被拒绝。 maxclients默认值是10000。可以通过info，clients来查询当前Redis的连接数
  2. 一旦客户端连接的idle时间超过了timeout连接将会被关闭。默认是0
  3. 可以通过 `config set maxclients` 对最大客户端连接数进行动态设置

- **client setName、client getName**

- **client kill**：杀掉指定IP地址和端口的客户端

  ``` shell
  client kill 192.168.56.101:43568
  ```

- **client pause**：用于阻塞客户端timeout毫秒数， 在此期间客户端连接将被阻塞

  ``` shell
  client pause timeout(毫秒)
  ```

- **monitor**：监控Redis正在执行的命令

  