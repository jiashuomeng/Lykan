## 启动参数

```shell
/deploy-1.0.0.jar 
-Xms4096m #  初始堆内存大小
-Xmx4096m #  最大堆内存大小
-Xmn2072m #  年轻代内存大小，推荐整个对内存的3/8
-XX:MetaspaceSize=1024m #  Metaspace扩容时触发FullGC的初始化阈值，也是最小的阈值。过小会频繁FGC，甚至OOM
-XX:MaxMetaspaceSize=2048m #  元数据可使用的最大空间
-XX:SurvivorRatio=8 #  survivor 和 Eden 区比例为1:1:8
-Xss256k # 单个线程的堆栈大小
-XX:-UseAdaptiveSizePolicy #  自动选择年轻代区大小和相应的Survivor区比例，控制目标系统规定的最低相应时间或者收集频率
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
-Djava.awt.headless=true 
-Djava.net.preferIPv4Stack=true  # 获取IPv4的地址，java网络接口只获取ipv4地址不获取ipv6地址
-Dfile.encoding=UTF-8 
-Dspring.profiles.active=prod
```

