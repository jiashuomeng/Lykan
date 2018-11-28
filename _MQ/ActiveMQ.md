## ActiveMQ的其他命令参数

> 下载地址：https://activemq.apache.org/download-archives.html
>
> 支持协议：AMQP、MQTT、OpenWire、REST、Stomp、XMPP

**start**：于启动activemq程序

**stop**：停止当前ActiveMQ节点的运行

**restart**：重新启动当前ActiveMQ节点

**status**：查看当前ActiveMQ节点的运行状态。如果当前ActiveMQ节点没有运行，那么将返回“ActiveMQ Broker is not running”的提示信息。只能知道当前节点是否正在运行

**console**：使用控制台模式启动ActiveMQ节点；在这种模式下，开发人员可以调试、监控当前ActivieMQ节点的实时情况，并获取实时状态

**dump**：如果采用console模式运行ActiveMQ，那么就可以使用dump参数，在console控制台上获取当前ActiveMQ节点的线程状态快照

## 关键节点

![流程图](../images/999999/20160401144922696.png)

1. Producer可以使用同步消息发送模式，也可以使用异步的消息发送模式
2. 消息生产者在ActiveMQ服务节点产生消息堆积的情况下可以使用 Slow Producer 保证机制
3. JMS提供事务功能，所以生产者是否开启事务发送消息，将会影响消息发送性能
4. 应对消息堆积的方式：
   - `NON_PERSISTENT Message`在内存堆积后，转储到Temp Store区域（当然也可以设置为不转储）
   - `PERSISTENT Meaage`无论怎样都会先使用持久化方案存储到永久存储区域
   - 在这些区域也产生堆积后，通知消息生产者使用Slow Producer机制
5. ActiveMQ服务节点在成功完成`PERSISTENT Meaage`的持久存储操作后，默认（可以设置成不回执）会向消息生产者发送一个确认信息，表示该条消息已处理完成。如果ActiveMQ服务节点接收的是`NON_PERSISTENT Message`，那么生产者默认情况下不会等待服务节点的回执
6. ActiveMQ服务节点主动推送消息给某一个消费者。在这个策略中，最重要的属性是prefetchSize：单次获得的消息数量
7. 消费者需要按照处理结果向ActiveMQ服务节点告知这条（或这些）消息是否处理成功——ACK应答。ActiveMQ中有多种ACK应答方式，它们对性能的影响也不相同。

### 消息发送

1. 默认情况下，ActiveMQ服务端认为生产者端发送的是`PERSISTENT Message`

2. 发送`NON_PERSISTENT Message`时，消息发送方默认使用异步方式：即是说消息发送后发送方不会等待`NON_PERSISTENT Message`在服务端的任何回执

   - **实际上所谓的异步发送也并非绝对的异步**，消息发送者会在发送一定大小的消息后等待服务端进行回执

   - 以下语句设置消息发送者在累计发送102400byte大小的消息后（可能是一条消息也可能是多条消息）。等待服务端进行回执,以便确定之前发送的消息是否被正确处理。确定服务器端是否产生了过量的消息堆积，是否需要减慢消息生产端的生产速度

     ``` java
     connectionFactory.setProducerWindowSize(102400);
     ```

   - 也可以设置成：无论怎样每次都等待服务器端的回执。但是一般不需要这么做

     ``` java
     connectionFactory.setAlwaysSyncSend(true);
     ```

3. 如果不特意指定消息的发送类型，那么消息生产者默认发送`PERSISTENT Meaage`。并且消息发送者默认等待ActiveMQ服务端对这条消息处理情况的回执

4. ActiveMQ允许开发人员遵从JMS API中的设置方式，为消息发送端在发送`PERSISTENT Meaage`时提供异步方式

   ``` java
   connectionFactory.setUseAsyncSend(true);
   
   // 一旦进行了这样的设置，就需要设置回执窗口：
   connectionFactory.setProducerWindowSize(102400);
   ```

### 事务

1. ActiveMQ支持事务。包括Topic和Queue
2. 事务开启后，生产者提交的消息都会被服务端添加到`transaction store`。在事务提交时才会将一条或多条消息放入到消息队列中去

### 生产者策略：ProducerFlowControl

> 生产流控制，设定了ActiveMQ服务节点在产生消息堆积，并超过限制大小的情况下，如何进行消息生产者端的限流

1. 策略触发时，ActiveMQ会让消息生产者进入等待状态或者在发送者端直接抛出JMSException
2. 可以配置ActiveMQ不进行ProducerFlowControl

### 消费者策略：Dispatch Async

1. 默认情况下ActiveMQ服务端采用异步方式向客户端推送消息

   > 也就是说ActiveMQ服务端在向某个消费者会话推送消息后，不会等待消费者的响应信息，直到消费者处理完消息后，主动向服务端返回处理结果

### 消费者策略：Prefetch

1. ActiveMQ系统中，默认的策略是ActiveMQ服务端一旦有消息，就主动按照设置的规则推送给当前活动的消费者。

2. 其中每次推送都有一定的数量限制，这个限制值就是prefetchSize

3. 针对Queue、Topic、`NON_PERSISTENT Message`、`PERSISTENT Message`、的队列，ActiveMQ有不同的默认“预取数量”

   ``` java
   PERSISTENT Message—Queue：prefetchSize=1000
   NON_PERSISTENT Message—Queue：prefetchSize=1000
   PERSISTENT Message—Topic：prefetchSize=100
   NON_PERSISTENT Message—Topic：prefetchSize=32766
   ```

4. 非必要情况下，请不要设置prefetchSize=1，因为这样就是一条一条的取数据

5. 也不要设置为prefetchSize=0，因为这将导致关闭服务器端的推送机制，改为客户端主动请求





