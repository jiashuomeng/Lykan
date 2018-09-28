## Spring容器的refresh()

> 预处理

- 在创建AnnotationConfigApplicationContext时，初始化`beanFactory`（具体在GenericApplicationContext中实现）

  ```java
  this.beanFactory = new DefaultListableBeanFactory();
  ```

- 创建 AnnotatedBeanDefinitionReader 关联 AnnotationConfigApplicationContext

  - AnnotatedBeanDefinitionReader 创建时往BeanFactory中注册了以下组件

  ```javascript
  org.springframework.context.annotation.internalConfigurationAnnotationProcessor
  
  org.springframework.context.annotation.internalAutowiredAnnotationProcessor
  
  org.springframework.context.annotation.internalRequiredAnnotationProcessor
  
  org.springframework.context.annotation.internalCommonAnnotationProcessor
  
  org.springframework.context.event.internalEventListenerProcessor
  
  org.springframework.context.event.internalEventListenerFactory
  ```

- 创建 ClassPathBeanDefinitionScanner 关联 AnnotationConfigApplicationContext

- 注册配置类（有 @Configuration 注解的类）



> 在AbstractApplicationContext类中

- `prepareRefresh()` 刷新前的预处理

  - `initPropertySources()`初始化一些属性设置;子类自定义个性化的属性设置方法
  - `getEnvironment().validateRequiredProperties();`检验属性的合法等
  - `earlyApplicationEvents= new LinkedHashSet<ApplicationEvent>();`保存容器中的一些早期的事件

- `obtainFreshBeanFactory();`获取BeanFactory

  - `refreshBeanFactory();`刷新 BeanFactory

  - `getBeanFactory();`返回刚才GenericApplicationContext创建的BeanFactory对象

  - 将创建的BeanFactory【DefaultListableBeanFactory】返回

- `prepareBeanFactory(beanFactory);`BeanFactory的预准备工作（BeanFactory进行一些设置）

  - 设置BeanFactory的类加载器、BeanExpressionResolver、PropertyEditorRegistrar

    ```java
    beanFactory.setBeanClassLoader(getClassLoader());
    
    beanFactory.setBeanExpressionResolver(new StandardBeanExpressionResolver(beanFactory.getBeanClassLoader()));
    
    beanFactory.addPropertyEditorRegistrar(new ResourceEditorRegistrar(this, getEnvironment()));
    ```

  - 添加部分BeanPostProcessor【ApplicationContextAwareProcessor】

    ```Java
    beanFactory.addBeanPostProcessor(new ApplicationContextAwareProcessor(this));
    ```

    这个BeanPostProcessor实际作用：

    ```Java
    public Object postProcessBeforeInitialization(final Object bean, String beanName) throws BeansException {
    	invokeAwareInterfaces(bean);
    	return bean;
    }
    
    private void invokeAwareInterfaces(Object bean) {
    		if (bean instanceof Aware) {
    			if (bean instanceof EnvironmentAware) {
    				((EnvironmentAware) bean).setEnvironment(this.applicationContext.getEnvironment());
    			}
    			if (bean instanceof EmbeddedValueResolverAware) {
    				((EmbeddedValueResolverAware) bean).setEmbeddedValueResolver(this.embeddedValueResolver);
    			}
    			if (bean instanceof ResourceLoaderAware) {
    				((ResourceLoaderAware) bean).setResourceLoader(this.applicationContext);
    			}
    			if (bean instanceof ApplicationEventPublisherAware) {
    				((ApplicationEventPublisherAware) bean).setApplicationEventPublisher(this.applicationContext);
    			}
    			if (bean instanceof MessageSourceAware) {
    				((MessageSourceAware) bean).setMessageSource(this.applicationContext);
    			}
    			if (bean instanceof ApplicationContextAware) {
    				((ApplicationContextAware) bean).setApplicationContext(this.applicationContext);
    			}
    		}
    	}
    ```

  - 设置忽略的自动装配的接口。被忽略后应用上下文通常会使用其他方式解决依赖关系。例如：ApplicationContext的依赖注入会使用ApplicationContextAware来实现。默认情况下，只有BeanFactoryAware接口被忽略。

    > 被忽略的组件：`EnvironmentAware`, `EmbeddedValueResolverAware`, `ResourceLoaderAware`, `ApplicationEventPublisherAware`, `MessageSourceAware`, `ApplicationContextAware`

    ```java
    this.ignoredDependencyInterfaces.add(ifc);
    ```

  - 注册可以解析的自动装配；我们能直接在任何组件中自动注入：BeanFactory、ResourceLoader、ApplicationEventPublisher、ApplicationContext

    ```java
    this.resolvableDependencies.put(dependencyType, autowiredValue);
    ```

  - 添加BeanPostProcessor【ApplicationListenerDetector】(负责注册和销毁`ApplicationContext`注册的`ApplicationListener`)

  - 给BeanFactory中注册一些能用的组件（单例Bean）
    - environment【ConfigurableEnvironment】
    - systemProperties【Map<String, Object>】
    - systemEnvironment【Map<String, Object>】

    

- `postProcessBeanFactory(beanFactory);`BeanFactory准备工作完成后进行的后置处理工作；

  - 子类通过重写这个方法来在BeanFactory创建并预准备完成以后做进一步的设置

- `invokeBeanFactoryPostProcessors(beanFactory);`执行BeanFactoryPostProcessor的方法

  - `BeanFactoryPostProcessor`：BeanFactory的后置处理器。在BeanFactory标准初始化之后执行的

  - 获取所有的BeanDefinitionRegistryPostProcessor

  - 看先执行实现了PriorityOrdered优先级接口的BeanDefinitionRegistryPostProcessor

    ```
    postProcessor.postProcessBeanDefinitionRegistry(registry)
    ```
    > 在AnnotationConfigApplicationContext初始化时，会有 ConfigurationClassPostProcessor满足这个条件。该类是在 AnnotatedBeanDefinitionReader 创建时注入的，key为：org.springframework.context.annotation.internalConfigurationAnnotationProcessor
    >
    > 
    >
    > 该类的作用是解析程序启动时传入的被@Configuration注解修饰的配置类。使用 ConfigurationClassParser 的parse方法解析出当前spring容器需要关心bean的BeanDefinition

  - 再执行实现了Ordered顺序接口的BeanDefinitionRegistryPostProcessor

    ```
    postProcessor.postProcessBeanDefinitionRegistry(registry)
    ```

  - 最后执行没有实现任何优先级或者是顺序接口的BeanDefinitionRegistryPostProcessors

    ```
    postProcessor.postProcessBeanDefinitionRegistry(registry)
    ```

  - 获取所有的BeanFactoryPostProcessor

  - 看先执行实现了PriorityOrdered优先级接口的BeanFactoryPostProcessor

  - 再执行实现了Ordered顺序接口的BeanFactoryPostProcessor

  - 最后执行没有实现任何优先级或者是顺序接口的BeanFactoryPostProcessor

- `registerBeanPostProcessors(beanFactory);`注册BeanPostProcessor

  > 		不同接口类型的BeanPostProcessor；在Bean创建前后的执行时机是不一样的
  > 		BeanPostProcessor、
  > 		DestructionAwareBeanPostProcessor、
  > 		InstantiationAwareBeanPostProcessor、
  > 		SmartInstantiationAwareBeanPostProcessor、
  > 		MergedBeanDefinitionPostProcessor[internalPostProcessors]

  - 获取所有的 BeanPostProcessor;后置处理器都默认可以通过PriorityOrdered、Ordered接口来执行优先级

  - 先注册PriorityOrdered优先级接口的BeanPostProcessor

  - 把每一个BeanPostProcessor；添加到BeanFactory中

  - 再注册Ordered接口的

  - 最后注册没有实现任何优先级接口的

  - 最终重新注册MergedBeanDefinitionPostProcessor

  - 注册一个ApplicationListenerDetector；来在Bean创建完成后检查是否是ApplicationListener，如果是

    ```
    applicationContext.addApplicationListener((ApplicationListener<?>) bean);[]
    ```

- `initMessageSource();`初始化MessageSource组件（做国际化功能；消息绑定，消息解析）

  - 获取BeanFactory
  - 看容器中是否有id为messageSource的，类型是MessageSource的组件
  - 如果有赋值给messageSource，如果没有自己创建一个DelegatingMessageSource；MessageSource：取出国际化配置文件中的某个key的值；能按照区域信息获取；
  - 把创建好的MessageSource注册在容器中，以后获取国际化配置文件的值的时候，可以自动注入MessageSource；

- `initApplicationEventMulticaster();`初始化事件派发器

  - 获取BeanFactory
  - 从BeanFactory中获取`applicationEventMulticaster`的`ApplicationEventMulticaster`
  - 如果上一步没有配置；创建一个`SimpleApplicationEventMulticaster`
  - 将创建的ApplicationEventMulticaster添加到BeanFactory中，以后其他组件直接自动注入

- `onRefresh();`留给子容器（子类）

  - 子类重写这个方法，在容器刷新的时候可以自定义逻辑

- `registerListeners();`将容器中将所有项目里面的`ApplicationListener`注册进来

  - 从容器中拿到所有的ApplicationListener
  - 将每个监听器bean名称添加到事件派发器中
  - 派发之前步骤产生的事件

- `finishBeanFactoryInitialization(beanFactory);`初始化所有剩下的单实例bean

  - 获取容器中的所有Bean，依次进行初始化和创建对象

  - 获取Bean的定义信息；RootBeanDefinition

  - Bean不是抽象的，是单实例的，是懒加载；

    - 判断是否是FactoryBean；是否是实现FactoryBean接口的Bean；

    - 不是工厂Bean。利用getBean(beanName);创建对象

      - getBean(beanName)； ioc.getBean();

      - doGetBean(name, null, null, false);

      - 先获取缓存中保存的单实例Bean。如果能获取到说明这个Bean之前被创建过（所有创建过的单实例Bean都会被缓存起来）

      - 缓存中获取不到，开始Bean的创建对象流程；

      - 标记当前bean已经被创建

      - 获取Bean的定义信息；

      - 获取当前Bean依赖的其他Bean;如果有按照getBean()把依赖的Bean先创建出来；

      - 启动单实例Bean的创建流程；

        - createBean(beanName, mbd, args);

        - `Object bean = resolveBeforeInstantiation(beanName, mbdToUse);`让BeanPostProcessor先拦截返回代理对象；

        - 【InstantiationAwareBeanPostProcessor】：提前执行

          先触发：postProcessBeforeInstantiation()；

          如果有返回值：触发postProcessAfterInitialization()；

        - 如果前面的InstantiationAwareBeanPostProcessor没有返回代理对象；调用4）

        - Object beanInstance = doCreateBean(beanName, mbdToUse, args);创建Bean

          - 【创建Bean实例】；createBeanInstance(beanName, mbd, args);

            利用工厂方法或者对象的构造器创建出Bean实例；

          - applyMergedBeanDefinitionPostProcessors(mbd, beanType, beanName);

            调用MergedBeanDefinitionPostProcessor的postProcessMergedBeanDefinition(mbd, beanType, beanName);

          - 【Bean属性赋值】populateBean(beanName, mbd, instanceWrapper);

            - 拿到InstantiationAwareBeanPostProcessor后置处理器；postProcessAfterInstantiation()；
            - 拿到InstantiationAwareBeanPostProcessor后置处理器；postProcessPropertyValues()；

          - 应用Bean属性的值；为属性利用setter方法等进行赋值；applyPropertyValues(beanName, mbd, bw, pvs);

          - 【Bean初始化】initializeBean(beanName, exposedObject, mbd);

            - 【执行Aware接口方法】invokeAwareMethods(beanName, bean);执行xxxAware接口的方法
            - 【执行后置处理器初始化之前】applyBeanPostProcessorsBeforeInitialization(wrappedBean, beanName);
            - 【执行初始化方法】invokeInitMethods(beanName, wrappedBean, mbd);
            - 【执行后置处理器初始化之后】applyBeanPostProcessorsAfterInitialization

- `finishRefresh();`完成BeanFactory的初始化创建工作；IOC容器就创建完成；
  - initLifecycleProcessor();初始化和生命周期有关的后置处理器；LifecycleProcessor。默认从容器中找是否有lifecycleProcessor的组件【LifecycleProcessor】；如果没有new DefaultLifecycleProcessor();加入到容器；
  - 拿到前面定义的生命周期处理器（BeanFactory）；回调onRefresh()；
  - publishEvent(new ContextRefreshedEvent(this));发布容器刷新完成事件；