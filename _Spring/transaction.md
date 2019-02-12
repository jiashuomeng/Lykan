### 事务传播策略

- **REQUIRED**：如果当前没有事务，就新建一个事务，如果已经存在一个事务中，加入到这个事务中。这是最常见的选择

- **SUPPORTS**：支持当前事务，如果当前没有事务，就以非事务方式执行

- **MANDATORY**：使用当前的事务，如果当前没有事务，就抛出异常

- **REQUIRES_NEW**：新建事务，如果当前存在事务，把当前事务挂起

- **NOT_SUPPORTED**：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起

- **NEVER**：以非事务方式执行，如果当前存在事务，则抛出异常

- **NESTED**：如果当前存在事务，则在嵌套事务内执行如果当前没有事务，则执行与REQUIRED类似的操作

  > 父事务中要开启子事务时会先在子事务开始的地方建立savepoint，如果子事务回滚，父事务会从savepoint继续执行。如果父事务回滚，子事务也会跟着回滚，父事务提交的时候子事务提交

**实现机制：**

- 代理手法同AOP，具体通知：`TransactionInterceptor`它继承了`TransactionAspectSupport`
- `TransactionAspectSupport`会根据配置获取`TransactionManager`来具体完成目标方法执行前后的事务控制

