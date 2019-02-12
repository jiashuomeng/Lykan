![tcp-sync-queue-and-accept-queue-small](../images/999999/tcp-sync-queue-and-accept-queue-small-1024x747.png)

### TCP头格式

![img](../images/999999/TCP-Header-01.png)

- TCP的包是没有IP地址的，那是IP层上的事。但是有源端口和目标端口
- 一个TCP连接需要四个元组来表示是同一个连接（src_ip, src_port, dst_ip, dst_port）准确说是五元组，还有一个是协议
- **Sequence Number**是包的序号，**用来解决网络包乱序（reordering）问题**
- **Acknowledgement Number**就是ACK——用于确认收到。**用来解决不丢包的问题**
- **Window又叫Advertised-Window**，也就是著名的滑动窗口（Sliding Window），**用于解决流控问题**
- **TCP Flag** ，也就是包的类型，**主要是用于操控TCP的状态机的**

### 建联、断联

![img](../images/999999/tcp_open_close.png)





