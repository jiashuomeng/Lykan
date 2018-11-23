## Netty Server端创建流程

### 1. 创建`ServerBootstrap`启动类 

- 使用建造者模式

### 2. 创建`EventLoopGroup`，设置并绑定Reactor线程池 

-  可以设置两个`EventLoopGroup`

  ```Java
   public ServerBootstrap group(EventLoopGroup parentGroup, EventLoopGroup childGroup)
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
.handler(new LoggingHandler(LogLevel.INFO))
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
- `childHandler`与`NioServerSocketChannel`对应。所有连接该监听端口的客户端都会执行它
- `handler`与客户端新接入连接的`SocketChannel`对应。每一个新接入的客户端都创建一个新的`handler`



### 5. 绑定并启动监听端口

### 6. `Selector`轮询 

### 7. Channel就绪后执行`ChannelPipeline`相关方法 

## ChannelHandler

### ChannelHandler执行顺序

#### 建立连接

#####1. channelRegistered

> 链路注册

#####2. channelActive

> 链路激活

#####3. channelRead

> 接收到请求消息

#####4. channelReadComplete

> 请求消息接收并处理完毕

#### 关闭连接

#####1. channelReadComplete
#####2. channelInactive

> 链路断开

#####3. channelUnregistered

> 取消注册

#### 出现异常

##### exceptionCaught

### 实用的ChannelHandler

#### `ByteToMessageDecoder`(系统解码框架)

#### `LengthFieldBasedFrameDecoder`(通用基于长度的半包解码器)

#### `LoggingHandler`(码流日志打印)

#### `SslHandler`(SSL安全认证)

#### `IdleStateHandler`(链路空闲检测)

#### `Base64Decoder`、`Base64Encoder`(Base64编解码)

### 启动流程

```Java
【C】AbstractNioChannel 类
{
	【M】doBeginRead()[2]，
	
	【C】AbstractUnsafe
    {
    	【M】beginRead()[1]
    	【M】bind()[1]
    }
    
    【M】
    
}
```

1. 