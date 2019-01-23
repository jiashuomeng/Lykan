## 引入AOP

**添加 `@EnableAspectJAutoProxy` 注解**

1. 静态导入了 `AspectJAutoProxyRegistrar`

   ```java
   @Import(AspectJAutoProxyRegistrar.class) 
   ```

2. 将`AnnotationAwareAspectJAutoProxyCreator`加入到IOC容器中

   ```Java
   // 1. 
   class AspectJAutoProxyRegistrar implements ImportBeanDefinitionRegistrar {
   	@Override
   	public void registerBeanDefinitions(BeanDefinitionRegistry registry) {
   
   		AopConfigUtils.registerAspectJAnnotationAutoProxyCreatorIfNecessary(registry);
   
   	}
   }
   
   // 2.
   public static BeanDefinition registerAspectJAnnotation(BeanDefinitionRegistry registry) {
   
   	RootBeanDefinition beanDefinition = new RootBeanDefinition(AnnotationAwareAspectJAutoProxyCreator.class);
   	beanDefinition.setSource(source);
   	beanDefinition.getPropertyValues().add("order", Ordered.HIGHEST_PRECEDENCE);
   	beanDefinition.setRole(BeanDefinition.ROLE_INFRASTRUCTURE);
   	registry.registerBeanDefinition(AUTO_PROXY_CREATOR_BEAN_NAME, beanDefinition);
   	return beanDefinition;
   }
   ```

3.  `AnnotationAwareAspectJAutoProxyCreator`继承结构如下

   ```Python
   AnnotationAwareAspectJAutoProxyCreator
   	->AspectJAwareAdvisorAutoProxyCreator
   		->AbstractAdvisorAutoProxyCreator
   			->AbstractAutoProxyCreator
   					implements SmartInstantiationAwareBeanPostProcessor, BeanFactoryAware
   ```

4. 需特别关注`BeanPostProcessor`的后置处理逻辑，具体位置在`AbstractAutoProxyCreator`中。每一个Bean在创建时都会经过该步骤，当目标类需要被代理时会返回代理对象

   ``` java
   public Object postProcessAfterInitialization(Object bean, String beanName) {
   	if (bean != null) {
   		return wrapIfNecessary(bean, beanName, cacheKey);
   	}
   	return bean;
   }
   ```

5. 创建代理类具体步骤

   - 获取容器中的所有通知`List<Advisor>`
   - 根据目标类过滤上一步中的list，过滤后只有需要被代理的类新生成的list才不为空，如果为空直接返回bean结束
   - 通知排序，排序受Order接口影响，后续进入创建代理类流程
   - 用目标类、通知列表创建`ProxyFactory`后续使用这个factory创建代理类
   - `ProxyFactory`会先判断使用JDK动态代理创建器还是CGLIB代理创建器
   - 比如使用`JdkDynamicAopProxy`，该类实现了`InvocationHandler`接口，并且将通知列表包装成了`AdvisedSupport`，后续的通知拦截器链就是`AdvisedSupport`生成的
   - `JdkDynamicAopProxy`以this作为`InvocationHandler`来创建代理类
   - 创建后返回给IOC容器，创建过程结束

## 使用AOP

### AOP调用过程

1. 代理类方法被调用
2. 调用`JdkDynamicAopProxy`的`invoke(Object proxy, Method method, Object[] args)`方法
3. `AdvisedSupport`创建拦截器链
4. 执行拦截器链返回结果

###AOP各种通知伪代码

``` java
try {
    Object result = null;
    
	try {
		result = ({
			before(); // 前置通知
			Object obj =  mi.proceed(); // 目标方法执行
			return obj;
		})(); // 环绕通知
	} finally {
		after(); // 后置通知
	}

	afterReturning(result);  // 后置通知，可处理目标方法返回结果
	
	return result;
} catch (Throwable ex) {
	afterThrowing(); // 异常通知
	throw ex;
}
```

### 拦截器链原理

- `ReflectiveMethodInvocation`里面有一个List，是拦截器列表。还有一个指针，默认为-1，会以`++index`的形式使用
- 拦截器链触发的机制是调用`ReflectiveMethodInvocation`的`process()`方法，该方法用`++index`每次取出一个`MethodInterceptor`
- 每次都要调用`methodInterceptor.invoke(this)`，this代表`ReflectiveMethodInvocation`
- `MethodInterceptor`的invoke方法会定义通知的策略，然后调用`methodInterceptor.proceed()`传递到下一个链表节点
- `ReflectiveMethodInvocation`的`process`定义了递归出口，只要index值增加到`list.size()-1`就会执行目标方法，继续后续的反向调用

**前置通知源码逻辑如下**

> ```java
> MethodBeforeAdviceInterceptor implements MethodInterceptor
> ```

``` java
@Override
public Object invoke(MethodInvocation mi) throws Throwable {
    this.advice.before(mi.getMethod(), mi.getArguments(), mi.getThis());
    return mi.proceed();
}
```

