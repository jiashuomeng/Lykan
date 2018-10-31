```java
public boolean lock(String key, long expireTime) {
 
    // 获取到当前时间的毫秒值
    long now = Instant.now().toEpochMilli();
 
    // 锁对象（redis中与key对应的value值） ： 锁失效的绝对时间
    long lockExpireTime = now + expireTime;
 
    // setIfAbsent 是原子操作，某一时刻有多个应用的多个线程同时调用该方法的话，如果没有value则只有一个能成功设置value返回true，剩下的都会返回false。如果有value都会返回false
    boolean isLock = redisTemplate.opsForValue().setIfAbsent(key, String.valueOf(lockExpireTime));
 
    if (isLock) {
        // 取锁成功, 为key设置一小时的过期时间。这个过期时间与lockExpireTime不同。只要大于获取锁后任务的执行时间就行，如果小于执行时间的话就会出现任务还没执行完锁就释放了
        redisTemplate.expire(key, 1, TimeUnit.HOURS);
        return true;
    } else {
        // 获取锁失败，从redis中拿到获取锁失效的绝对时间
        Object lockExpireTimeFromRedis = redisTemplate.opsForValue().get(key);
 
        if (lockExpireTimeFromRedis != null) {
            long oldExpireTime = Long.parseLong((String) lockExpireTimeFromRedis);
 
            // 锁失效时间如果小于当前时间,说明锁已经超时,重新取锁
            if (oldExpireTime <= now) {
 
                // 多个线程同时调用 getAndSet，该方法是一个CAS操作，假设1线程的oldExpireTime与redis里面存储数据相同，则替换redis中的数据，然后将旧数据返回。
                // 2、3、4线程再拿着 oldExpireTime 去比较的时候发现redis中的数据与旧数据已经不相等了，然后返回自己的lockExpireTime，redis中数据不变
                // currentExpireTime 会保证只有一个线程返回旧数据，剩下的线程都会返回新数据
                long currentExpireTime = Long.parseLong(redisTemplate.opsForValue().getAndSet(key, String.valueOf(lockExpireTime)));
 
                //相等,则取锁成功
                if (currentExpireTime == oldExpireTime) {
                    redisTemplate.expire(key, 1, TimeUnit.HOURS);
                    return true;
                } else {
                    return false;
                }
            }
        } else {
            // 如果获取不到，说明锁被释放了，可重新参与竞争
            return false;
        }
    }
    return false;
}
 
 
public boolean unlock(String key) {
    redisTemplate.delete(key);
    return true;
}
```

