# 分布式系统
## 问题
1. 网络延迟：性能、超时；
2. 网络故障：丢包、乱序和抖动（采用TCP协议解决）。

导致分布式系统的调用三态：
1. 成功；
2. 失败；
3. 超时。

## CAP原理
1. Consisitency，（强）一致性，表示系统多个副本之间呈现出一致的状态；
2. Availiability，（高）可用性，通过数据复制保证数据可用，避免单点失效问题（至少做到服务降级）；
3. Partition Tolerance，（高）可扩展性，分区容忍性，

在在线交易系统，要求强一致性，所以可用性和可扩展性较差；而如果是对一般分布式系统，可用性和扩展性要求较高，牺牲强一致性，只保证最终的一致性，一般采用BASE模型。

> Nosql追求AP，传统数据库追求CA。

### 一致性模型
- 强一致性，新的数据一旦写入，在任意副本任意时刻都能读到新值。比如：文件系统，RDBMS，Azure Table都是强一致性的；
- 弱一致性，不同副本上的值有新有旧，需要应用方做更多的工作获取最新值。比如Dynamo；
- 最终一致性，一旦更新成功，各副本的数据最终将达到一致。


> - Causal Consistency（因果一致性）：如果Process A通知Process B它已经更新了数据，那么Process B的后续读取操作则读取A写入的最新值，而与A没有因果关系的C则可以最终一致性。
- Read-your-writes Consistency（读你所写一致性）：如果Process A写入了最新的值，那么 Process A的后续操作都会读取到最新值。但是其它用户可能要过一会才可以看到。
- Session Consistency（会话一致性）：一次会话内一旦读到某个值，不会读到更旧的值。
- Monotonic Read Consistency（单调一致性）：一个用户一旦读到某个值，不会读到比这个值更旧的值，其他用户不一定。

### Base模型
Base模型，是在牺牲一致性的基础上，提供高可用性和分区容错性。
- 基本可用， 指分布式系统在出现故障的时候，保证核心可用，允许损失部分可用性；
- 软状态， 指允许系统中的数据存在中间状态，并认为该中间状态不会影响系统整体可用性，即允许系统不同节点的数据副本之间进行同步的过程存在时延；
- 最终一致性，最终一致性强调的是系统中所有的数据副本，在经过一段时间的同步后，最终能达到一致的状态。

> ACID 要求强一致性，通常运用在传统的数据库系统上。而 BASE 要求最终一致性，通过牺牲强一致性来达到可用性，通常运用在大型分布式系统中。

# 分布式事务
指事务操作位于不同的节点上，需要保证事务的ACID特性。


# 分布式锁
由于分布式原因，对于多个节点资源的共享，需要通过额外的能被多个节点访问的某个节点（位置）提供锁机制，可以分为客户端（申请资源）和服务端（维护锁，计数值），那么需要解决客户端和服务端都出现错误的问题。也就是如下问题：
1. 互斥性，要求任意时刻，只有一个客户端能够持有锁；
2. 不发生死锁，客户端如果在持有锁过程中宕机，保证后续客户端可用锁；
3. 具有容错性，只要redis的大部分节点正常运行，客户端就可以加锁和解锁；
4. 识别锁拥有者，加锁和解锁必须是同一客户端，不能解别人的锁（sychronized,创建的Monitor的对象有一个owner字段记录锁的拥有者）。

## 加锁

```java
public class RedisTool {

    private static final String LOCK_SUCCESS = "OK";
    private static final String SET_IF_NOT_EXIST = "NX";
    private static final String SET_WITH_EXPIRE_TIME = "PX";

    /**
     * 尝试获取分布式锁
     * @param jedis Redis客户端
     * @param lockKey 锁
     * @param requestId 请求标识
     * @param expireTime 超期时间
     * @return 是否获取成功
     */
    public static boolean tryGetDistributedLock(Jedis jedis, String lockKey, String requestId, int expireTime) {

        String result = jedis.set(lockKey, requestId, SET_IF_NOT_EXIST, SET_WITH_EXPIRE_TIME, expireTime);
        if (LOCK_SUCCESS.equals(result)) {
            return true;
        }
        return false;

    }

}
```
1. 采用Key当锁（采用唯一的）；
2. Value里面传递ownerId，用来识别不同的客户端，解决第4个问题；
3. 这个参数我们传的是PX，意思是我们要给这个key加一个过期的设置，具体时间由第五个参数决定，过期时间是为了解决第2个问题；
4. 这个参数我们填的是NX，意思是SET IF NOT EXIST，即当key不存在时，我们进行set操作；若key已经存在，则不做任何操作，解决第1个问题；
5. 解决第3个问题比较复杂，需要采用RedLock算法（分布式锁管理器）;

> 采用单机复制的方案是会出现多个客户端同时持有锁的情况（宕机时，master来不及写入slave）；

1. 获取当前时间（单位是毫秒）。
2. 轮流用相同的key和随机值在N个节点上请求锁，在这一步里，客户端在每个master上请求锁时，会有一个和总的锁释放时间相比小的多的超时时间。比如如果锁自动释放时间是10秒钟，那每个节点锁请求的超时时间可能是5-50毫秒的范围，这个可以防止一个客户端在某个宕掉的master节点上阻塞过长时间，如果一个master节点不可用了，我们应该尽快尝试下一个master节点。
3. 客户端计算第二步中获取锁所花的时间，只有当客户端在大多数master节点上成功获取了锁（在这里是3个），而且总共消耗的时间不超过锁释放时间，这个锁就认为是获取成功了。
4. 如果锁获取成功了，那现在锁自动释放时间就是最初的锁释放时间减去之前获取锁所消耗的时间。
5. 如果锁获取失败了，不管是因为获取成功的锁不超过一半（N/2+1)还是因为总消耗时间超过了锁释放时间，客户端都会到每个master节点上释放锁，即便是那些他认为没有获取成功的锁。


## 解锁

```java
public class RedisTool {

    private static final Long RELEASE_SUCCESS = 1L;

    /**
     * 释放分布式锁
     * @param jedis Redis客户端
     * @param lockKey 锁
     * @param requestId 请求标识
     * @return 是否释放成功
     */
    public static boolean releaseDistributedLock(Jedis jedis, String lockKey, String requestId) {

        String script = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end";
        Object result = jedis.eval(script, Collections.singletonList(lockKey), Collections.singletonList(requestId));

        if (RELEASE_SUCCESS.equals(result)) {
            return true;
        }
        return false;

    }

}
```

解锁实现的思路类似于CAS操作，首先比较value是否和当前的接收端传递的id相等， 如果相等则删除该值；如果不等，则返回false。（单机环境下CPU保证CAS指令执行是原子的，而分布式情况下，可以通过redis的Lua脚本保证指令执行的原子性）

如果不保证原子性，会造成什么问题，如果在获取值的时候，锁过期了，而另一个访问端此时加了锁，然后调用

# 分布式一致性协议
## Paxos算法






# Reference
- [RedLock](https://www.cnblogs.com/ironPhoenix/p/6048467.html)

