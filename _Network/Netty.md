## Netty请求处理流程

![image-20181125174048846](../images/999999/image-20181125174048846.png)

## Netty Server端创建流程

### 1. 创建`ServerBootstrap`启动类 

- 使用建造者模式

### 2. 创建`EventLoopGroup`，设置并绑定Reactor线程池 

-  可以设置两个`EventLoopGroup`

```Java
DefaultThreadFactory bossFactory = new DefaultThreadFactory("JS-BOSS", false, Thread.NORM_PRIORITY);
Executor bossExecutor = new ThreadPerTaskExecutor(bossFactory);
EventLoopGroup bossGroup = new NioEventLoopGroup(1, bossExecutor);
```

``` java
DefaultThreadFactory workFactory = new DefaultThreadFactory("JS-WORK", false, Thread.NORM_PRIORITY);
Executor workExecutor = new ThreadPerTaskExecutor(workFactory);
EventLoopGroup workerGroup = new NioEventLoopGroup(NettyRuntime.availableProcessors() * 2, workExecutor);
```

### 3. 设置并绑定服务端Channel（`NioServerSocketChannel`）

- 反射实现

  ``` java
  // ReflectiveChannelFactory
  @Override
  public T newChannel() {
      try {
          return clazz.getConstructor().newInstance();
      } catch (Throwable t) {
          throw new ChannelException("Unable to create Channel from class " + clazz, t);
      }
  }
  ```

### 4. 创建并初始化`ChannelHandler` 

``` java
.handler(new ChannelInitializer<NioServerSocketChannel>() {
             @Override
             public void initChannel(NioServerSocketChannel ch) {
                 ch.pipeline().addLast(new LoggingHandler(LogLevel.INFO));
             }
         }
)
.childHandler(new ChannelInitializer<SocketChannel>() {
    @Override
    public void initChannel(SocketChannel ch) {
        ch.pipeline().addLast(Hessian2CodeFactory.buildHessian2Decoder());
        ch.pipeline().addLast(Hessian2CodeFactory.buildHessian2Encoder());
        ch.pipeline().addLast(new Hessian2ServerHandler());
    }
});
```

- 可以使用`ChannelInitializer`添加`ChannelHandler`链
- `ServerBootstrap`可以配置两个`ChannelHandler`，分别为`handler`和`childHandler`
- `handler`与`NioServerSocketChannel`对应。所有连接该监听端口的客户端都会执行它
- `childHandler`与客户端新接入连接的`SocketChannel`对应。每一个新接入的客户端都创建一个新的`childHandler`

### 5. 设置`option` 

```java
.option(ChannelOption.SO_BACKLOG, 100)
.childOption(ChannelOption.SO_BACKLOG, 100)
```

### 6. 绑定并启动监听端口

1. 调用`io.netty.bootstrap.AbstractBootstrap # initAndRegister `

   - 创建`NioServerSocketChannel`

   - 设置 channel的options、attrs参数

   - `channel.pipeline()`添加一个`ChannelInitializer`其作用如下，调用时机见`register0`：

     ```java
     public void initChannel(final Channel ch) throws Exception {
         ChannelPipeline pipeline = ch.pipeline();
         pipeline.addLast(config.handler());
         [async] pipeline.addLast(new ServerBootstrapAcceptor(
                             ch, 
                             currentChildGroup, 
                             currentChildHandler, 
                             currentChildOptions, 
                             currentChildAttrs)
         );
     }
     ```

   - BOSS线程中按顺序取出一个线程调用`register`

     ``` java
     executors[Math.abs(idx.getAndIncrement() % executors.length)].register(channel);
     ```

     1. 创建`DefaultChannelPromise`对象直接返回。用于后面添加事件监听器

        ``` java
        Promise promise = new DefaultChannelPromise(channel, eventLoop);
        promise.channel().unsafe().register(eventLoop, promise);
        return promise;
        
        ---
        
        [io.netty.bootstrap.AbstractBootstrap # doBind]
        promise.addListener(new ChannelFutureListener() {
            @Override
            public void operationComplete(ChannelFuture future) throws Exception {
                promise.registered();
                doBind0(regFuture, channel, localAddress, promise);
            }
        });
        ```

     2. 使用BOSS线程执行`register`

        ``` java
        promise.channel().unsafe().register(eventLoop, promise);
        
        ---
            
        [io.netty.channel.AbstractChannel.AbstractUnsafe # register]
        eventLoop.execute(new Runnable() {
            @Override
            public void run() {
                register0(promise);
            }
        });
        ```

2. 实际绑定注册

   >  上一步触发BOSS线程调用 `io.netty.channel.AbstractChannel.AbstractUnsafe # register0` 完成绑定

   1. `doRegister();` 注册事件监听。因为ops为0，此时无法接收客户端请求

      ```java
      selectionKey = javaChannel().register(eventLoop().unwrappedSelector(), 0, this);
      ```

   2. `pipeline.invokeHandlerAddedIfNeeded();` 执行上文中的 `initChannel` 初始化handler

      > 在调用 `invokeHandlerAddedIfNeeded()` 方法之前，pipeline中`registered`为false。此时`pipeline.addLast()` 时只是往pending handler callback队列中添加了一个任务，并未真的将handler添加到pipeline中
      >
      > 在该方法调用之后，`registered`变为true。之后`pipeline.addLast()`会直接将handler添加到pipeline中
      >
      > 注意：此时并未将`ServerBootstrapAcceptor`加入到handler队列中。添加时机在`register`方法执行完之后。因为`register`中会将`ServerBootstrapAcceptor`的添加封装成一个task提交到当前的BOSS线程队列中。

   3. `safeSetSuccess(promise);`设置注册成功标志位，触发事件监听器

      > 事件监听器是在上文6.1.1实例代码中注册的

      - `io.netty.bootstrap.AbstractBootstrap # doBind0`

      - `io.netty.channel.AbstractChannel # bind`

      - `io.netty.channel.DefaultChannelPipeline # bind`

      - 依次调用组件中的bind。pipeline -> tail -> … -> head -> unsafe

      - unsafe中有两个重要的操作

        1. ServerSocketChannel绑定IP地址及端口号

           ``` java 
           javaChannel().bind(localAddress, config.getBacklog());
           ```

        2. 使用BOSS线程执行active通知

           ``` java
           eventLoop().execute(new Runnable() {
               @Override
               public void run() {
                   pipeline.fireChannelActive();
               }
           });
           ```

      - `pipeline.fireChannelActive()`首先会触发head的`fireChannelActive()`

      - `HeadContext`中两个重要的操作。重点看`readIfIsAutoRead()`

        ``` java
        public void channelActive(ChannelHandlerContext ctx) throws Exception {
            ctx.fireChannelActive();
        
            readIfIsAutoRead();
        }
        ```

      - 判断AutoRead == true。依次调用各组件中的read。channel->pipeline->tail->...->head->unsafe

      - `io.netty.channel.nio.AbstractNioChannel # doBeginRead` ops改成为16，开始接收客户端连接

        ```Java
        protected void doBeginRead() throws Exception {
            readPending = true;
        
            final int interestOps = selectionKey.interestOps();
            if ((interestOps & readInterestOp) == 0) {
                selectionKey.interestOps(interestOps | readInterestOp);
            }
        }
        ```

   4. `pipeline.fireChannelRegistered();`

## 请求处理流程

``` java
1. 
io.netty.channel.nio.NioEventLoop # processSelectedKeys

2. 
io.netty.channel.nio.NioEventLoop # processSelectedKeysOptimized
{
	for (int i = 0; i < selectedKeys.size; ++i) {

	    final SelectionKey k = selectedKeys.keys[i];
	    selectedKeys.keys[i] = null;

	    final Object a = k.attachment();

	    ╋ processSelectedKey(k, (AbstractNioChannel) a);
	}
}

3.
io.netty.channel.nio.NioEventLoop # processSelectedKey
{
	int readyOps = k.readyOps();
	if ((readyOps & (SelectionKey.OP_READ | SelectionKey.OP_ACCEPT)) != 0 || readyOps == 0) {
	    ╋ unsafe.read();
	}
}

4. 
io.netty.channel.nio.AbstractNioMessageChannel.NioMessageUnsafe # read
{
	private final List<Object> readBuf = new ArrayList<Object>();
	
	doReadMessages(readBuf);
        {
            SocketChannel ch = SocketUtils.accept(javaChannel());
            if (ch != null) {
                buf.add(new NioSocketChannel(this, ch));
                return 1;
            }
        }
}
{
	int size = readBuf.size();
	for (int i = 0; i < size; i ++) {
	    readPending = false;
	    ╋ pipeline.fireChannelRead(readBuf.get(i));
	}
	readBuf.clear();
	allocHandle.readComplete();
	pipeline.fireChannelReadComplete();

	if (exception != null) {
	    closed = closeOnReadError(exception);
	    pipeline.fireExceptionCaught(exception);
	}

	if (closed) {
	    close(voidPromise());
	}
}

5.
╋ io.netty.channel.DefaultChannelPipeline # fireChannelRead

6. 
io.netty.channel.AbstractChannelHandlerContext # invokeChannelRead((ChannelHandlerContext)context,  (NioSocketChannel)msg);
{
	EventExecutor executor = context.executor();
	if (executor.inEventLoop()) {
	    ╋ context.invokeChannelRead(msg);
	} else {
	    executor.execute(new Runnable() {
	        @Override
	        public void run() {
	            context.invokeChannelRead(msg);
	        }
	    });
	}
}

7. 
io.netty.channel.AbstractChannelHandlerContext # invokeChannelRead
{
	╋ ((ChannelInboundHandler) handler()).channelRead(this, msg);
}

8.
io.netty.channel.DefaultChannelPipeline.HeadContext # channelRead
{
	╋ io.netty.channel.ChannelHandlerContext # fireChannelRead
}

9.
io.netty.channel.AbstractChannelHandlerContext # fireChannelRead
{
	AbstractChannelHandlerContext context = findContextInbound(){
	    AbstractChannelHandlerContext ctx = this;
	    do {
	        ctx = ctx.next;
	    } while (!ctx.inbound);
	    return ctx;
	}
	[to -> 5] invokeChannelRead((ChannelHandlerContext)ctx, (NioSocketChannel)msg);
}

10. 
io.netty.bootstrap.ServerBootstrap.ServerBootstrapAcceptor # channelRead
```

## ChannelHandler

### ChannelHandler执行顺序

#### 建立连接

#####1. handlerAdded

> 添加handler

#####2. channelRegistered

> 链路注册

#####3. channelActive

> 链路激活

#####4. channelRead

> 接收到请求消息

#####5. channelReadComplete

> 请求消息接收并处理完毕

#### 关闭连接

#####1. channelReadComplete
#####2. channelInactive

> 链路断开

#####3. channelUnregistered

> 取消注册

#### 出现异常

##### exceptionCaught





```
Netty启动

    1. ServerBootstrap对象创建
    2. 设置parentEventLoopGroup、childEventLoopGroup
    3. 设置option参数，如backlog
    4. 设置handler、childHandler
    5. 监听端口
    6. 容器关闭释放资源

监听端口

    1. 创建Channel，比如 NioServerSocketChannel

    2. 初始化chanel，给channel赋值，具体设置option、attribute、handler等
        pipeline.addLast()接收的是实现 ChannelHandler 接口的实例。这种实例分两种一种是直接实现该接口的，直接包装成 DefaultChannelHandlerContext 加到链表中就结束了，还有一种是 ChannelInitializer 的子类。子类中重写  void initChannel(NioServerSocketChannel ch) 方法。方法中使用ch.pipeline().addLast()来添加 handler。这种形式的原理是ChannelInitializer实现了ChannelHandler的 handlerAdded 方法，在调用 handlerAdded 方法时，该方法调用了initChannel来完成功能，值得一提的是 initChannel 在执行完之后会将自身（ChannelInitializer）从链表中移除

    3. 注册
        - 以上流程都是主线程执行的，注册流程由BOSS线程驱动
        - 将 Channel 注册到Selector上，Selector 是 EventLoop 的组件，在 EventLoop 中循环处理 Selector事件。注册时会将当前的 channel 作为 attachment 传入。返回 selectionKey
        - 目前的pipeline（channel中的组件）只有head、ChannelInitializer、tail
          需要将 ChannelInitializer 切换至相应的Handler。
          具体会向 pipeline 中增加启动时设置的handler（不是childHandler）和 ServerBootstrapAcceptor。
          有 connect 请求时 ServerBootstrapAcceptor会分发给具体的childEventLoop去处理读写
        - safeSetSuccess(promise); 触发 Promise 的 Listener。监听器有一个，用于绑定ip开始监听端口。
        - pipeline.fireChannelRegistered(); 默认无动作

    4. 端口监听
        - 触发时机一般是在3中的 safeSetSuccess中，之所以是一般是因为，如果在注册完之后会同步调用bind()。Listener和同步的实现效果是相同的。都会用 EventLoop 来驱动 bind()事件
        - bind的调用顺序
            channel -> pipeline -> tail -> ... head -> unsafe。unsafe中有两个重要的步骤
            1. doBind(localAddress)， 给channel指定本地ip地址和backlog
            2. pipeline.fireChannelActive(); head 中会先放行 fireChannelActive ，当执行完之后会执行read操作。
                read 执行顺序：channel -> pipeline -> tail -> ... -> head -> unsafe
                具体在 AbstractNioChannel # doBeginRead 中开始监听端口





处理accept事件

	- NioEventLoop 创建成功后会开启一个循环任务。该任务会去循环检测：
		1. 任务队列中是否有任务，如果有任务则消费掉
		2. Selector是否有就绪事件。默认 select 等待 1000ms
	- 有就绪事件时，从 SelectionKey 中拿到 NioServerSocketChannel 开始处理。具体是：unsafe.read();
	- 从 ServerSocketChannel 中获取 SocketChannel。执行 pipeline.fireChannelRead(channel)进行处理
		- 最终会到 ServerBootstrapAcceptor 的 channelRead
		- ServerBootstrapAcceptor 封装了childHandler 和 childEventLoopGroup
		- 选取 childEventLoop，注册 SocketChannel。注册流程由 childEventLoop 驱动
			- 将 SocketChannel 注册到 childEventLoop 的Selector上，并将当前的 NioSocketChannel作为attachment传入
			- 创建责任链，创建过程由ServerBootstrap创建时指定
			- safeSetSuccess(promise);
			- pipeline.fireChannelRegistered();
			- pipeline.fireChannelActive(); head先放行，之后调用unsafe，给selectKey注册read事件

	- pipeline.fireChannelReadComplete();

io.netty.channel.nio.AbstractNioMessageChannel.NioMessageUnsafe # read



OP_READ = 1
OP_WRITE = 4
OP_CONNECT = 8
OP_ACCEPT = 16



```

```Java
ChannelInboundInvoker

    ChannelInboundInvoker fireChannelRegistered();

    ChannelInboundInvoker fireChannelUnregistered();

    ChannelInboundInvoker fireChannelActive();

    ChannelInboundInvoker fireChannelInactive();

    ChannelInboundInvoker fireExceptionCaught(Throwable cause);

    ChannelInboundInvoker fireUserEventTriggered(Object event);

    ChannelInboundInvoker fireChannelRead(Object msg);

    ChannelInboundInvoker fireChannelReadComplete();

    ChannelInboundInvoker fireChannelWritabilityChanged();

ChannelOutboundInvoker

    ChannelFuture bind(SocketAddress localAddress);

    ChannelFuture connect(SocketAddress remoteAddress);

    ChannelFuture connect(SocketAddress remoteAddress, SocketAddress localAddress);

    ChannelFuture disconnect();

    ChannelFuture close();

    ChannelFuture deregister();

    ChannelFuture bind(SocketAddress localAddress, ChannelPromise promise);

    ChannelFuture connect(SocketAddress remoteAddress, ChannelPromise promise);

    ChannelFuture connect(SocketAddress remoteAddress, SocketAddress localAddress, ChannelPromise promise);

    ChannelFuture disconnect(ChannelPromise promise);

    ChannelFuture close(ChannelPromise promise);

    ChannelFuture deregister(ChannelPromise promise);

    ChannelOutboundInvoker read();

    ChannelFuture write(Object msg);

    ChannelFuture write(Object msg, ChannelPromise promise);

    ChannelOutboundInvoker flush();

    ChannelFuture writeAndFlush(Object msg, ChannelPromise promise);

    ChannelFuture writeAndFlush(Object msg);

    ChannelPromise newPromise();

    ChannelProgressivePromise newProgressivePromise();

    ChannelFuture newSucceededFuture();

    ChannelFuture newFailedFuture(Throwable cause);

    ChannelPromise voidPromise();
```

