## 启动参数

```shell
/deploy-1.0.0.jar 
-Xms4096m #  初始堆内存大小
-Xmx4096m #  最大堆内存大小
-Xmn1536m #  年轻代内存大小，推荐整个堆内存的3/8
-XX:MetaspaceSize=1024m #  Metaspace扩容时触发FullGC的初始化阈值，也是最小的阈值。过小会频繁FGC，甚至OOM
-XX:MaxMetaspaceSize=2048m #  元数据可使用的最大空间
-XX:SurvivorRatio=8 #  survivor 和 Eden 区比例为1:1:8
-Xss256k # 单个线程的堆栈大小
-XX:-UseAdaptiveSizePolicy #  自动选择年轻代区大小和相应的Survivor区比例，控制目标系统规定的最低响应时间或者收集频率
-XX:+PrintPromotionFailure #  打印晋升失败日志
-XX:+HeapDumpOnOutOfMemoryError #  导出内存溢出的堆信息(hprof文件)
-XX:HeapDumpPath=/data/logs/deploy/oom.hprof #  保存路径
-XX:+UseConcMarkSweepGC #  使用CMS垃圾收集器
-XX:+CMSParallelRemarkEnabled #  开启并发标记，降低标记停顿
-XX:CMSInitiatingOccupancyFraction=70 #  使用70％后开始CMS收集，解决由于老年代可用空间不足导致的对象晋升失败，进而出现FULL GC
-XX:+UseCMSInitiatingOccupancyOnly #  禁止hostspot自行触发CMS GC，使用CMSInitiatingOccupancyFraction=70 判断是否进行CMS垃圾收集
-XX:+UseFastAccessorMethods # 原始类型的快速优化
-XX:+PrintGCDetails 
-XX:+PrintGCDateStamps #  打印gc触发时间
-XX:GCLogFileSize=100M # 控制GC日志文件的大小 
-Xloggc:/data/logs/deploy/gc.log 
-Djava.net.preferIPv4Stack=true  # 获取IPv4的地址，java网络接口只获取ipv4地址不获取ipv6地址
-Dfile.encoding=UTF-8 
-Dspring.profiles.active=prod
```

``` shell
/opt/jdk8/bin/java 
-server 
-Xms256m 
-Xmx256m 
-Xmn96m 
-XX:+UseG1GC 
-XX:G1HeapRegionSize=16m 
-XX:G1ReservePercent=25 
-XX:InitiatingHeapOccupancyPercent=30 
-XX:SoftRefLRUPolicyMSPerMB=0 
-XX:SurvivorRatio=8 
-verbose:gc 
-Xloggc:/dev/shm/mq_gc_%p.log 
-XX:+PrintGCDetails 
-XX:+PrintGCDateStamps 
-XX:+PrintGCApplicationStoppedTime 
-XX:+PrintAdaptiveSizePolicy 
-XX:+UseGCLogFileRotation 
-XX:NumberOfGCLogFiles=5 
-XX:GCLogFileSize=30m 
-XX:-OmitStackTraceInFastThrow 
-XX:+AlwaysPreTouch 
-XX:MaxDirectMemorySize=15g 
-XX:-UseLargePages 
-XX:-UseBiasedLocking 
-Djava.ext.dirs=/opt/jdk8/jre/lib/ext:/opt/rocketmq4.2/bin/../lib 
-cp .:/opt/rocketmq4.2/bin/../conf: 
org.apache.rocketmq.broker.BrokerStartup -n 192.168.56.101:9876 -c ./conf/broker-run.properties
```

``` shell
/opt/jdk8/bin/java 
-server 
-Xms4g 
-Xmx4g 
-Xmn2g 
-XX:MetaspaceSize=128m 
-XX:MaxMetaspaceSize=320m 
-XX:+UseConcMarkSweepGC 
-XX:+UseCMSCompactAtFullCollection 
-XX:CMSInitiatingOccupancyFraction=70 
-XX:+CMSParallelRemarkEnabled 
-XX:SoftRefLRUPolicyMSPerMB=0 
-XX:+CMSClassUnloadingEnabled 
-XX:SurvivorRatio=8 
-XX:-UseParNewGC 
-verbose:gc 
-Xloggc:/dev/shm/rmq_srv_gc.log 
-XX:+PrintGCDetails 
-XX:-OmitStackTraceInFastThrow 
-XX:-UseLargePages 
-Djava.ext.dirs=/opt/jdk8/jre/lib/ext:/opt/rocketmq4.2/bin/../lib 
-cp .:/opt/rocketmq4.2/bin/../conf: 
org.apache.rocketmq.namesrv.NamesrvStartup
```

> jstat -gc 25773 1s 

应用启动10天左右，1.2万次YGC，花费154s。无full gc