## 创建`ApplicationContext`对象

>  这边用的是`AnnotationConfigApplicationContext`

1. **AnnotationConfigApplicationContext** 继承实现结构
   - 【C】**GenericApplicationContext**
     - 【C】**AbstractApplicationContext**
       - 【C】DefaultResourceLoader
         - 【I】ResourceLoader
       - 【I】**ConfigurableApplicationContext**
         - 【I】**ApplicationContext**
           - 【I】EnvironmentCapable
           - 【I】ListableBeanFactory
           - 【I】HierarchicalBeanFactory
           - 【I】MessageSource
           - 【I】ApplicationEventPublisher
           - 【I】ResourcePatternResolver
         - 【I】Lifecycle
         - 【I】Closeable
     - 【I】BeanDefinitionRegistry
   - 【I】AnnotationConfigRegistry

### 创建`BeanFactory`

```java
public GenericApplicationContext() {
    this.beanFactory = new DefaultListableBeanFactory();
}
```

### 创建 `AnnotatedBeanDefinitionReader`对象

1. 关联`AnnotationConfigApplicationContext`

2. 往`AnnotationConfigApplicationContext`中注册 BeanDefinition 组件

   ```SQL
   org.springframework.context.annotation.internalConfigurationAnnotationProcessor
   [ConfigurationClassPostProcessor.class]
   implements BeanDefinitionRegistryPostProcessor, PriorityOrdered, 
   			ResourceLoaderAware, BeanClassLoaderAware, EnvironmentAware
   
   ---
   
   org.springframework.context.annotation.internalAutowiredAnnotationProcessor
   [AutowiredAnnotationBeanPostProcessor.class]
   implements SmartInstantiationAwareBeanPostProcessor
   
   ---
   
   org.springframework.context.annotation.internalRequiredAnnotationProcessor
   [RequiredAnnotationBeanPostProcessor.class]
   implements SmartInstantiationAwareBeanPostProcessor, MergedBeanDefinitionPostProcessor, 				PriorityOrdered, BeanFactoryAware
   
   ---
   
   org.springframework.context.annotation.internalCommonAnnotationProcessor
   [CommonAnnotationBeanPostProcessor.class]
   implements DestructionAwareBeanPostProcessor, MergedBeanDefinitionPostProcessor,
   			PriorityOrdered, Serializable,
   			InstantiationAwareBeanPostProcessor, BeanFactoryAware
   
   ---
   
   org.springframework.context.event.internalEventListenerProcessor
   [EventListenerMethodProcessor.class]
   implements SmartInitializingSingleton, ApplicationContextAware
   
   ---
   
   org.springframework.context.event.internalEventListenerFactory
   [DefaultEventListenerFactory.class]
   implements EventListenerFactory, Ordered
   ```

### 创建`ClassPathBeanDefinitionScanner`

1. 关联`AnnotationConfigApplicationContext`

## 注册配置类

> 有 `@Configuration` 注解的类

## `refresh`方法

> 在`AbstractApplicationContext`类中

### `prepareRefresh()` 

- `initPropertySources(); `ApplicationContext子类实现可以自定义自己的 PropertySources
- `getEnvironment().validateRequiredProperties();` 校验 Property
- `this.earlyApplicationEvents = new LinkedHashSet<>()`

### `obtainFreshBeanFactory()` 

> `ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();`

1. `refreshBeanFactory();`刷新 BeanFactory

   ```java
   this.beanFactory.setSerializationId(getId());
   ```

2. `getBeanFactory();` 返回刚才`GenericApplicationContext`创建的BeanFactory对象

### `prepareBeanFactory(beanFactory)` 

- 设置BeanFactory的类加载器、BeanExpressionResolver、PropertyEditorRegistrar

  ```Java
  beanFactory.setBeanClassLoader(getClassLoader());
  
  beanFactory.setBeanExpressionResolver(new StandardBeanExpressionResolver(beanFactory.getBeanClassLoader()));
  
  beanFactory.addPropertyEditorRegistrar(new ResourceEditorRegistrar(this, getEnvironment()));
  ```

- 添加部分BeanPostProcessor【ApplicationContextAwareProcessor】

  ``` java
  beanFactory.addBeanPostProcessor(new ApplicationContextAwareProcessor(this));
  ```

  > 该接口的作用
  >
  > ``` java
  > public Object postProcessBeforeInitialization(final Object bean, String beanName) throws BeansException {
  > 	invokeAwareInterfaces(bean);
  > 	return bean;
  > }
  > 
  > private void invokeAwareInterfaces(Object bean) {
  > 	if (bean instanceof Aware) {
  > 		if (bean instanceof EnvironmentAware) {
  > 			((EnvironmentAware) bean).setEnvironment(this.applicationContext.getEnvironment());
  > 		}
  > 		if (bean instanceof EmbeddedValueResolverAware) {
  > 			((EmbeddedValueResolverAware) bean).setEmbeddedValueResolver(this.embeddedValueResolver);
  > 		}
  > 		if (bean instanceof ResourceLoaderAware) {
  > 			((ResourceLoaderAware) bean).setResourceLoader(this.applicationContext);
  > 		}
  > 		if (bean instanceof ApplicationEventPublisherAware) {
  > 			((ApplicationEventPublisherAware) bean).setApplicationEventPublisher(this.applicationContext);
  > 		}
  > 		if (bean instanceof MessageSourceAware) {
  > 			((MessageSourceAware) bean).setMessageSource(this.applicationContext);
  > 		}
  > 		if (bean instanceof ApplicationContextAware) {
  > 			((ApplicationContextAware) bean).setApplicationContext(this.applicationContext);
  > 		}
  > 	}
  > }
  > ```

- 设置忽略的自动装配的接口。被忽略后应用上下文通常会使用其他方式解决依赖关系。例如：ApplicationContext的依赖注入会使用ApplicationContextAware来实现。默认情况下，只有BeanFactoryAware接口被忽略。

  > 被忽略的组件：`EnvironmentAware`, `EmbeddedValueResolverAware`, `ResourceLoaderAware`, `ApplicationEventPublisherAware`, `MessageSourceAware`, `ApplicationContextAware`

  ``` java
  this.ignoredDependencyInterfaces.add(ifc);
  ```

- 注册可以自动解析装配的Bean；可以直接在任何组件中使用`@Resource`等注解注入

  > 注册的bean：BeanFactory、ResourceLoader、ApplicationEventPublisher、ApplicationContext

  >Demo:
  >
  >``` java
  >@Resource
  >private ApplicationEventPublisher applicationEventPublisher;
  >```

- 添加BeanPostProcessor【ApplicationListenerDetector】

  > 负责`ApplicationContext` register 和 remove 实现`ApplicationListener`接口的bean

- 给BeanFactory中注册一些能用的组件（单例Bean）

  > ```java
  > beanFactory.registerSingleton(ENVIRONMENT_BEAN_NAME, getEnvironment());
  > ```

  - environment【ConfigurableEnvironment】
  - systemProperties【Map<String, Object>】
  - systemEnvironment【Map<String, Object>】

### `postProcessBeanFactory(beanFactory)`

> 子类自定义

### `invokeBeanFactoryPostProcessors(beanFactory)`

> BeanDefinitionRegistryPostProcessor extends BeanFactoryPostProcessor

1. 获取所有的实现 `BeanDefinitionRegistryPostProcessor`接口的实例

2. 先执行实现了`PriorityOrdered`优先级接口的`BeanDefinitionRegistryPostProcessor`的`postProcessBeanDefinitionRegistry`方法

   ```java
   postProcessor.postProcessBeanDefinitionRegistry(registry)
   ```

   > 使用AnnotationConfigApplicationContext初始化时，会有 ConfigurationClassPostProcessor满足这个条件。
   >
   > 该类是在 AnnotatedBeanDefinitionReader 创建时注入的
   >
   > key为：org.springframework.context.annotation.internalConfigurationAnnotationProcessor
   >
   > 
   >
   > 该类的作用是解析程序启动时传入的被@Configuration注解修饰的配置类。使用 ConfigurationClassParser 的parse方法解析出当前spring容器需要关心bean的BeanDefinition

3. 再执行实现了Ordered顺序接口的BeanDefinitionRegistryPostProcessor的`postProcessBeanDefinitionRegistry`方法

4. 最后执行没有实现任何优先级或者是顺序接口的BeanDefinitionRegistryPostProcessor的`postProcessBeanDefinitionRegistry`方法

5. 执行所有实现 BeanDefinitionRegistryPostProcessor 接口的 postProcessBeanFactory方法

6. 获取所有的实现BeanFactoryPostProcessor接口的实例

7. 先执行实现了PriorityOrdered优先级接口的BeanFactoryPostProcessor的方法

8. 再执行实现了Ordered顺序接口的BeanFactoryPostProcessor

9. 最后执行没有实现任何优先级或者是顺序接口的BeanFactoryPostProcessor

> `BeanFactoryPostProcessor`
>
> 在应用程序上下文的标准初始化之后修改其内部bean工厂。所有bean定义都已经加载，但是还没有实例化bean。这允许覆盖或添加属性，甚至可以初始化bean
> 
>
> `BeanDefinitionRegistryPostProcessor`
>
> 在标准初始化之后修改应用程序上下文的内部bean定义注册表。所有常规bean定义都已加载，但还没有实例化bean。这允许在下一个后期处理阶段开始之前添加进一步的bean定义

###`registerBeanPostProcessors(beanFactory)`

###`initMessageSource()`

###`initApplicationEventMulticaster()`

### `onRefresh()`

###`registerListeners()`

### `finishBeanFactoryInitialization(beanFactory)`

### `finishRefresh();`











