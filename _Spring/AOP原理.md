## 原理

#### @EnableAspectJAutoProxy 

​	@Import(AspectJAutoProxyRegistrar.class)：给容器中导入AspectJAutoProxyRegistrar 

#### AspectJAutoProxyRegistrar.class

 	1. AspectJAutoProxyRegistrar  实现了 ImportBeanDefinitionRegistrar 。可以使用 registerBeanDefinitions 方法注册bean
		2. 可以注册  AnnotationAwareAspectJAutoProxyCreator.class 

```
private static BeanDefinition registerOrEscalateApcAsRequired(Class<?> cls, BeanDefinitionRegistry registry, Object source) {

RootBeanDefinition beanDefinition = new RootBeanDefinition(cls);
beanDefinition.setSource(source);
beanDefinition.getPropertyValues().add("order", Ordered.HIGHEST_PRECEDENCE);
beanDefinition.setRole(BeanDefinition.ROLE_INFRASTRUCTURE);
registry.registerBeanDefinition(AUTO_PROXY_CREATOR_BEAN_NAME, beanDefinition);
return beanDefinition;
}
```

#### AnnotationAwareAspectJAutoProxyCreator.class 

```
AnnotationAwareAspectJAutoProxyCreator
	->AspectJAwareAdvisorAutoProxyCreator
		->AbstractAdvisorAutoProxyCreator
			->AbstractAutoProxyCreator
					implements SmartInstantiationAwareBeanPostProcessor, BeanFactoryAware
				关注后置处理器（在bean初始化完成前后做事情）、自动装配BeanFactory
```

```
AbstractAutoProxyCreator.setBeanFactory()
AbstractAutoProxyCreator.有后置处理器的逻辑；

AbstractAdvisorAutoProxyCreator.setBeanFactory()
		->super.setBeanFactory(beanFactory) 
		->initBeanFactory()

AnnotationAwareAspectJAutoProxyCreator.initBeanFactory()
```

#### 创建和注册AnnotationAwareAspectJAutoProxyCreator的过程

> IOC中注册名称：org.springframework.aop.config.internalAutoProxyCreator

1. **传入配置类，创建ioc容器** 

2. **注册配置类，调用refresh（）刷新容器** 

3. **registerBeanPostProcessors(beanFactory);注册bean的后置处理器来方便拦截bean的创建** 

   - 先获取IOC容器已经定义了的需要创建对象的所有BeanPostProcessor 

     ```
     String[] postProcessorNames = beanFactory.getBeanNamesForType(BeanPostProcessor.class);
     ```

   - 给容器中加别的BeanPostProcessor

     ```
     int count = beanFactory.getBeanPostProcessorCount() + 1 + postProcessorNames.length;
     beanFactory.addBeanPostProcessor(new BeanPostProcessorChecker(beanFactory, count));
     ```

   - 注册BeanPostProcessor，实际上就是创建BeanPostProcessor对象，保存在容器中

     1. 优先注册实现了PriorityOrdered接口的BeanPostProcessor
     2. 再给容器中注册实现了Ordered接口的BeanPostProcessor 【AbstractAutoProxyCreator 走这里】
     3. 注册没实现优先级接口的BeanPostProcessor

     ```
     List<BeanPostProcessor> priority = new ArrayList<BeanPostProcessor>();
     List<BeanPostProcessor> internal = new ArrayList<BeanPostProcessor>();
     List<String> orderedNames = new ArrayList<String>();
     List<String> nonOrderedNames = new ArrayList<String>();
     
     for (String ppName : postProcessorNames) {
     	if (beanFactory.isTypeMatch(ppName, PriorityOrdered.class)) {
     		BeanPostProcessor pp = beanFactory.getBean(ppName, BeanPostProcessor.class);
     		priority.add(pp);
     		if (pp instanceof MergedBeanDefinitionPostProcessor) {
     			internal.add(pp);
     		}
     	}
     	else if (beanFactory.isTypeMatch(ppName, Ordered.class)) {
     		orderedNames.add(ppName);
     	}
     	else {
     		nonOrderedNames.add(ppName);
     	}
     }
     
     // 1. 优先注册实现了PriorityOrdered接口的BeanPostProcessor
     sortPostProcessors(priority, beanFactory);
     registerBeanPostProcessors(beanFactory, priority);
     
     // 2. 给容器中注册实现了Ordered接口的BeanPostProcessor
     List<BeanPostProcessor> orderedPostProcessors = new ArrayList<BeanPostProcessor>();
     for (String ppName : orderedNames) {
     	BeanPostProcessor pp = beanFactory.getBean(ppName, BeanPostProcessor.class);
     	orderedPostProcessors.add(pp);
     	if (pp instanceof MergedBeanDefinitionPostProcessor) {
     		internal.add(pp);
     	}
     }
     sortPostProcessors(orderedPostProcessors, beanFactory);
     registerBeanPostProcessors(beanFactory, orderedPostProcessors);
     
     // 3. 注册没实现优先级接口的BeanPostProcessor
     List<BeanPostProcessor> nonOrderedPostProcessors = new ArrayList<BeanPostProcessor>();
     for (String ppName : nonOrderedNames) {
     	BeanPostProcessor pp = beanFactory.getBean(ppName, BeanPostProcessor.class);
     	nonOrderedPostProcessors.add(pp);
     	if (pp instanceof MergedBeanDefinitionPostProcessor) {
     		internal.add(pp);
     	}
     }
     registerBeanPostProcessors(beanFactory, nonOrderedPostProcessors);
     ```

4. **创建internalAutoProxyCreator的BeanPostProcessor【AnnotationAwareAspectJAutoProxyCreator】**
   1. 创建Bean的实例
   2. populateBean；给bean的各种属性赋值
   3. initializeBean：初始化bean
      - invokeAwareMethods()：处理Aware接口的方法回调 <BeanNameAware , BeanClassLoaderAware , BeanFactoryAware >
      - applyBeanPostProcessorsBeforeInitialization()：应用后置处理器的postProcessBeforeInitialization（）
      - invokeInitMethods()；执行自定义的初始化方法
      - applyBeanPostProcessorsAfterInitialization()：执行后置处理器的postProcessAfterInitialization（）
5. **AnnotationAwareAspectJAutoProxyCreator.setBeanFactory()->initBeanFactory()**
   - super.initBeanFactory(beanFactory); 
   - this.aspectJAdvisorsBuilder = new BeanFactoryAspectJAdvisorsBuilderAdapter(..);

#### 创建代理类

> BeanPostProcessor是在Bean对象创建完成初始化前后调用的
>
> InstantiationAwareBeanPostProcessor是在创建Bean实例之前先尝试用后置处理器返回对象的

1. **传入配置类，创建ioc容器** 

2. **注册配置类，调用refresh（）刷新容器** 

3. **finishBeanFactoryInitialization(beanFactory);完成BeanFactory初始化工作；创建剩下的单实例bean**

   - 遍历获取容器中所有的Bean，依次创建对象getBean(beanName)

     ```
     getBean->doGetBean()->getSingleton()
     ```

   - 先从缓存中获取当前bean，如果能获取到，说明bean是之前被创建过的，直接使用，否则再创建

   - 先调用实现 InstantiationAwareBeanPostProcessor接口的processor的postProcessBeforeInstantiation获取bean

     ```
     bean = applyBeanPostProcessorsBeforeInstantiation(targetType, beanName);
     if (bean != null) {
     	bean = applyBeanPostProcessorsAfterInitialization(bean, beanName);
     }
     ```

     ```
     Object applyBeanPostProcessorsBeforeInstantiation(Class << ? > beanClass, String beanName) {
     	for (BeanPostProcessor bp: getBeanPostProcessors()) {
     		if (bp instanceof InstantiationAwareBeanPostProcessor) {
     			InstantiationAwareBeanPostProcessor ibp = (InstantiationBeanPostProcessor)bp;
     			Object result = ibp.postProcessBeforeInstantiation(beanClass, beanName);
     			if (result != null) {
     				return result;
     			}
     		}
     	}
     	return null;
     }
     ```

     >让BeanPostProcessor有机会返回一个代理而不是目标bean实例
     >
     >1）、判断当前bean是否在advisedBeans中（保存了所有需要增强bean）
     >2）、判断当前bean是否是基础类型的Advice、Pointcut、Advisor、AopInfrastructureBean，
     >	或者是否是切面（@Aspect）
     >3）、是否需要跳过
     >	1）、获取候选的增强器（切面里面的通知方法）【List<Advisor> candidateAdvisors】
     >		每一个封装的通知方法的增强器是 InstantiationModelAwarePointcutAdvisor；
     >		判断每一个增强器是否是 AspectJPointcutAdvisor 类型的；返回true
     >	2）、永远返回false

   - 获取不到，调用doCreateBean(beanName, mbdToUse, args); <真正的去创建一个bean实例>

4. **postProcessAfterInitialization创建代理类**

   > return wrapIfNecessary(bean, beanName, cacheKey);//包装如果需要的情况下

   1. 获取当前bean的所有增强器（通知方法）  Object[]  specificInterceptors

      - 找到候选的所有的增强器
      - 获取到能在bean使用的增强器
      - 给增强器排序

      ```
      protected List < Advisor > findEligibleAdvisors(Class << ? > beanClass, String beanName) {
      	List < Advisor > candidateAdvisors = findCandidateAdvisors();
      	List < Advisor > eligibleAdvisors = findAdvisorsThatCanApply(candidateAdvisors, beanClass, beanName);
      	extendAdvisors(eligibleAdvisors);
      	if (!eligibleAdvisors.isEmpty()) {
      		eligibleAdvisors = sortAdvisors(eligibleAdvisors);
      	}
      	return eligibleAdvisors;
      }
      ```

   2. 保存当前bean在advisedBeans中

      ```
      this.advisedBeans.put(cacheKey, Boolean.TRUE);
      ```

   3. 如果当前bean需要增强，创建当前bean的代理对象

      - 获取所有增强器（通知方法）
      - 保存到proxyFactory
      - 创建代理对象：Spring自动决定
        - JdkDynamicAopProxy(config);jdk动态代理；
        	 ObjenesisCglibAopProxy(config);cglib的动态代理；		

   4. 给容器中返回当前组件使用cglib增强了的代理对象；
   5. 以后容器中获取到的就是这个组件的代理对象，执行目标方法的时候，代理对象就会执行通知方法的流程；

#### 目标方法执行

> 容器中保存了组件的代理对象（cglib增强后的对象），这个对象里面保存了详细信息（比如增强器，目标对象，xxx）

1. CglibAopProxy.intercept();拦截目标方法的执行

2. 根据ProxyFactory对象获取将要执行的目标方法拦截器链

   ```
   List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
   ```

   - List<Object> interceptorList保存所有拦截器
   - **遍历所有的增强器，将其转为Interceptor**

3. 如果没有拦截器链，直接执行目标方法

4. 如果有拦截器链，把需要执行的目标对象，目标方法，拦截器链等信息传入创建一个 CglibMethodInvocation 对象。并调用 Object retVal =  mi.proceed();