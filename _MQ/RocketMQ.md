### 基本命令

``` shell
#启动：
  nohup ./bin/mqnamesrv &
  nohup ./bin/mqbroker -n 192.168.56.101:9876 -c ./conf/broker-run.properties &

#关闭：
  ./bin/mqshutdown broker
  ./bin/mqshutdown namesrv
```

### 角色

![image-20181015125817655](../images/999999/image-20181015125817655.png)

#### Producer

> 不同的业务场景需要生产者采用不同的写人策略 。 比如同步发送、异步发送、 延迟发送、 发送事务消息等

**DefaultMQProducer**

> 默认

**发送方式**

​	同步 & 异步（异步回调）

**发送消息要经过五个步骤**

- 设置 Producer 的 GroupName
- 设置 lnstanceName ，当一个 Jvm 需要启动多个 Producer 的时候，通过设置不同的 InstanceName 来区分，不设置的话系统使用默认名称“DEFAULT”
- 设置发送失败重试次数，当网络出现异常的时候，这个次数影响消息的重复投递次数 。 想保证不丢消息，可以设置多重试几次
- 设置 NameServer 地址
- 组装消息并发送

**消息发送的返回状态**

- **FLUSH_DISK_TIMEOUT：**表示没有在规定时间内完成刷盘（需要Broker的刷盘策略被设置成 `SYNC_FLUSH` 才会报这个错误） 
- **FLUSH_SLAVE_TIMEOUT**：表示在主备方式下，并且 Broker 被设置成 `SYNC_MASTER` 方式，没有在设定时间内完成主从同步
- **SLAVE_NOT_AVAILABLE**：这个状态产生的场景和 FLUSH_SLAVE_TIMEOUT类似， 表示在主备方式下，并且 Broker 被设置成 `SYNC_MASTER`。但是没有找到被配置成 Slave 的 Broker
- **SEND_OK**：表示发送成功，发送成功的具体含义，比如消息是否已经被存储到磁盘？消息是否被同步到了 Slave 上？消息在 Slave 上是否被写人磁盘？需要结合所配置的刷盘策略、主从策略来定。

> 写一个高质量的生产者程序，重点在于对发送结果的处理，要充分考虑各种异常，写清对应的处理逻辑

**发送延迟消息**

> Broker 收到这类 消 息后 ，延迟一段时间再处理 ， 使消息在规定的一段时间后生效

​	延迟消息的使用方法是在创建 Message 对象时，调用 setDelayTimeLevel ( int level ） 方法设置延迟时间。目前延迟的时间不支持任意设置，仅支持预设值的时间长度（ 1s/5s/10s/30s/1m/2m/3m/4m/5m/6m/7m/8m/9m/10m/20m/30m/1h/2h ） 。 比如 setDelayTimeLevel(3) 表示延迟 10s

**自定义消息发送规则**

​	MessageQueueSelector：把同一类型的消息都发往相同的`Message Queue`

**对事务的支持**

RocketMQ 中 `TransactionMQProducer` 采用两阶段提交的方式实现事务消息：

1. 发送方向 RocketMQ 发送“待确认”消息
2. RocketMQ 将收到的“待确认” 消息持久化成功后， 向发送方回复消息已经发送成功，此时第一阶段消息发送完成
3. 发送方开始执行本地事件逻辑
4. 发送方根据本地事件执行结果向 RocketMQ 发送二次确认（ Commit 或是 Rollback ） 消息 ， RocketMQ 收到 Commit 状态则将第一阶段消息标记为可投递，订阅方将能够收到该消息；收到 Rollback 状态则删除第一阶段的消息，订阅方接收不到该消息
5. 如果出现异常情况，4 ）提交的二次确认最终未到达 RocketMQ，服务器在经过固定时间段后将对“待确认”消息、发起回查请求
6. 发送方收到消息回查请求后（如果发送一阶段消息的 Producer 不能工作，回查请求将被发送到和 Producer 在同一个 Group 里的其他 Producer ），通过检查对应消息 的本地事件执行结果返回 Commit 或 Roolback 状态
7. RocketMQ 收到回查请求后，按照步骤 4 ） 的逻辑处理

> 因为 RocketMQ 依赖将数据顺序写到磁盘这个特征来提高性能，步骤 4 ）却需要更改第一阶段消息的状态，这样会造成磁盘Catch 的脏页过多， 降低系统的性能 。 所以 RocketMQ 在 4.x 的版本中将这部分功能去除 

**如何存储队列位置信息**

> 使用Offset实现重新消费某条消息、 跳过一段时间内的消息等功能。

- Offset 是指某个 Topic 下的一条消息在某个 Message Queue 里的位置
- 通过 Offset 的值可以定位到这条消息，或者指示 Consumer 从这条消息开始向后继续处理
- Offset主要分为本地文件类型和 Broker 代存的类型两种。`CLUSTERING`模式由 Broker 端存储和控制 Offset 的值。`BROADCASTING`模式每个 Consumer都收到这个 Topic 的全部消息，各个 Consumer 间相互没有干扰， RocketMQ 使用 LocalfileOffsetStore ，把 Offset 存到本地

#### Consumer

> 根据使用者对读取操作的控制情况，消费者可分为两种类型

##### DefaultMQPushConsumer

> 由系统控制读取操作，收到消息后自动调用传人的处理方法来处理

- **参数**

  -  Consumer 的GroupName  # GroupName 需要和消息模式 （ MessageModel ）配合使用 

    - **消息模式1：Clustering**

      在 Clustering 模式下，同一个 ConsumerGroup ( GroupName 相同 ） 里的每个 Consumer 只消费所订阅消息的一部分内容，同一个 ConsumerGroup 里所有的 Consumer 消 费 的内 容合起来才是所订阅 Topic 内 容 的 整体

    - **消息模式2：Broadcasting**

      同一个 ConsumerGroup 里的每个 Consumer 都能消费到所订阅 Topic 的全部消息，也就是一个消息会被多次分发，被多个 Consumer 消费

  -  NameServer 的地址和端口号

  - Topic 的名称 # 如果不需要消费某个 Topic 下的所有消息，可以通过指定消息的 Tag 进行消息过滤

- **push问题**

  - 加大 Server 端的工作量，进而影响 Server 的性能
  - Client 的处理能力各不相同， Client 的状态不受 Server 控制。如果 Client 不能及时处理Server 推送过来的消息，会造成各种潜在问题

- **pull问题**

  - 循环拉取消息的间隔不好设定。间隔太短就处在一个 “忙等”的状态，浪费资源。每个Pull 的时间间隔太长 Server 端有消息到来时 有可能没有被及时处理

- **长轮询**

  - 使用 `PullRequest` “长轮询” 方式达到 **push** 效果。长轮询方式既有Pull的优点，又兼具Push方式的实时性=
  - Broker 在没有新消息的时候才阻塞，有消息会立刻返回
  - 服务端接到新消息请求后，如果队列里没有新消息，并不急于返回，通过一个循环不断查看状态，每次 waitForRunning一段时间（默认是 5 秒），然后再Check。默认情况下当 Broker 一直没有新消息，第三次 Check 的时候，等待时间超过 Request 里面的 BrokerSuspendMaxTimeMillis， 就返回空结果
  - 在HOLD住 Consumer 请求的时候需要占用资源，适合用在消息队列这种客户端连接数可控的场景中

- **流量控制**

  - RocketMQ 定义了一个快照类 `ProcessQueue` 来解决获取当前消息堆积的数量、重复处理某些消息、延迟处理某些消息等问题

  - 每个 `Message Queue` 都会有个对应的 `ProcessQueue` 对象，保存了这个 `Message Queue` 消息处理状态的快照

  - `ProcessQueue` 对象里主要的内容是一个 TreeMap 和 一个读写锁

  - TreeMap里以 `Message Queue` 的 `Offset` 作为 Key ，以消息内容的引用为 Value ，保存了所有从 `Message Queue` 获取到，但是还未被处理的消息

  - 读写锁控制着多个线对 TreeMap 对象的并发访问

  - 客户端在每次 Pull请求前会做下面三个判断来控制流量

    - 判断获取但还未处理的消息个数
    - 消息总大小
    - Offset 的跨度

    >  任何一个值超过设定的大小就隔一段时间再拉取消息，从而达到流量控制的目的。 此外 ProcessQueue 还可以辅助实现顺序消费的逻辑

  - `DefaultMQPushConsumer` 的退出，要调用 shutdown()函数， 以便释放资源、保存Offset等。 这个调用要加到 Consumer 所在应用的退出逻辑中

##### DefaultMQPullConsumer

> 读取操作中的大部分功能由使用者自主控制

#### Broker

#### NameServer

### 消息模型

- 一个 Topic 可以根据需求设置一个或多个 Message Queue, Message Queue 类似分区或 Partition 。 Topic 有 了 多个 Message Queue 后，消息可以并行地向各个Message Queue 发送，消费者也可以并行地从多个 Message Queue 读取消息并消费

### 配置参数

``` shell 
#示例
namesrvAddr=192.168.100.131:9876;192.168.100.132:9876

brokerClusterName=DefaultCluster

brokerName=broker-b # Master 和 Slave 通过使用相同的 Broker 名称来表明相互关系

brokerid=0 # 一个 Master Barker 可以有多个 Slave, 0 表示 Master ，大于 0 表示不同Slave 的 ID 

deleteWhen=04 # 与 fileReservedTime 参数呼应，表明在几点做消息删除动作，默认值 04 表示凌晨 4 点

fileReservedTime=48 # 在磁盘上保存消息的时长，单位是小时，自动删除超时的消息

brokerRole=SYNC_MASTER # brokerRole 有 3 种： SYNC_MASTER 、 ASYNC_MASTER 、 SLAVE 关键词 SYNC 和 ASYNC 表示 Master 和 Slave 之间同步消息的机制， SYNC 的意思是当 Slave 和 Master 消息同步完成后，再返回发送成功的状态

flushDiskType=ASYNC_FLUSH # 刷盘策略。分为 SYNC_FLUSH 和 ASYNC_FLUSH 两种，分别代表同步刷盘和异步刷盘。 同步刷盘情况下，消息真正写人磁盘后再返回成功状态；异步刷盘情况下，消息写人 page_cache 后就返回成功状态

listenPort=10911 # Broker 监听的端口号

storePathRootDir=/home/rocketmq/store-b # 存储消息以及一些配置信息的根目录

brokerIP1=192.168.56.101 # 设置 Broker 机器对外暴露的 ip 地址
```

### 代码demo

``` java
class SyncProducer {

    public static void main(String[] args) throws Exception {

        DefaultMQProducer producer = new DefaultMQProducer("s_group_name");
        producer.setNamesrvAddr("192.168.56.101:9876");
        producer.start();

        int max = 100;
        for (int i = 0; i < max; i++) {
            Message msg = new Message("TopicTest", "TagA", ("Hello RocketMQ" + i).getBytes(RemotingHelper.DEFAULT_CHARSET));
            SendResult sendResult = producer.send(msg);
            System.out.println("send result ->" + sendResult);
        }
    }
}
```

> ``` javascript
> send result ->
> 	SendResult [
> 		sendStatus=SEND_OK, 
> 		msgId=AC110F10FE1218B4AAC21792CEC50063, 
> 		offsetMsgId=C0A8386500002A9F000000000001A042, 
> 		messageQueue=MessageQueue [topic=TopicTest, brokerName=broker-a, queueId=2], 
> 		queueOffset=149
> 	]
> ```

``` java
class SyncConsumer {

    public static void main(String[] args) throws Exception {
        DefaultMQPushConsumer consumer = new DefaultMQPushConsumer("s_group_name");
        consumer.setNamesrvAddr("192.168.56.101:9876");

        consumer.setConsumeFromWhere(ConsumeFromWhere.CONSUME_FROM_FIRST_OFFSET);

        consumer.subscribe("TopicTest", "*");
        consumer.registerMessageListener((MessageListenerConcurrently) (msgs, context) -> {
            System.out.println(Thread.currentThread().getName() + " message ->" + msgs);
            return ConsumeConcurrentlyStatus.CONSUME_SUCCESS;
        });
        consumer.start();
    }
}
```

> ``` javascript
> ConsumeMessageThread_20 message ->[MessageExt [
> 	queueId=2, 
> 	storeSize=178, 
> 	queueOffset=149, 
> 	sysFlag=0, 
> 	bornTimestamp=1543989097157, 
> 	bornHost=/192.168.56.1:56834, 
> 	storeTimestamp=1540192719238, 
> 	storeHost=/192.168.56.101:10911, 
> 	msgId=C0A8386500002A9F000000000001A042, 
> 	commitLogOffset=106562, 
> 	bodyCRC=1179674355, 
> 	reconsumeTimes=0, 
> 	preparedTransactionOffset=0, 
> 	toString()=Message [
> 		topic=TopicTest, 
> 		flag=0, 
> 		properties={
> 			MIN_OFFSET=0, 
> 			MAX_OFFSET=150, 
> 			CONSUME_START_TIME=1543989097166, 
> 			UNIQ_KEY=AC110F10FE1218B4AAC21792CEC50063, 
> 			WAIT=true, 
> 			TAGS=TagA
> 		}, 
> 		body=16
> 	]
> ]]
> ```