**SimpleTypeConverter**

- **【C】TypeConverterSupport**

  - **【C】PropertyEditorRegistrySupport**

    > 【 void setConversionService(ConversionService conversionService) 】
    > 【 ConversionService getConversionService() 】

    - **【I】PropertyEditorRegistry**

      > 【 void registerCustomEditor(Class<?> requiredType, PropertyEditor propertyEditor) 】
      >
      > 【 PropertyEditor findCustomEditor(Class<?> requiredType, String propertyPath) 】

  - **【I】TypeConverter**

    > 【 T convertIfNecessary(Object value, Class<T> requiredType) 】



**PropertyEditor**

> 【 void setValue(Object value) 】
> 【 Object getValue() 】
>
> 【 String getAsText() 】
> 【 void setAsText(String text) 】
>
> 【 boolean supportsCustomEditor() 】
>
> 【 void addPropertyChangeListener(PropertyChangeListener listener) 】
> 【 void removePropertyChangeListener(PropertyChangeListener listener) 】



**ConversionService**

> 【 boolean canConvert(Class<?> sourceType, Class<?> targetType) 】
> 【 boolean canConvert(TypeDescriptor sourceType, TypeDescriptor targetType) 】
>
> 【 T convert(Object source, Class<T> targetType) 】
> 【 Object convert(Object source, TypeDescriptor sourceType, TypeDescriptor targetType) 】



```java
// PropertyEditorRegistrar 有个 `void registerCustomEditors(PropertyEditorRegistry registry)` 方法可以批量给 PropertyEditorRegistry 注册 PropertyEditor
Set<PropertyEditorRegistrar> propertyEditorRegistrars = new LinkedHashSet<>(4);
Map<Class<?>, Class<? extends PropertyEditor>> customEditors = new HashMap<>(4);

protected void registerCustomEditors(PropertyEditorRegistry registry) {

    if (!this.propertyEditorRegistrars.isEmpty()) {
        for (PropertyEditorRegistrar registrar : this.propertyEditorRegistrars) {
            registrar.registerCustomEditors(registry);
        }
    }
    
    if (!this.customEditors.isEmpty()) {
        this.customEditors.forEach((requiredType, editorClass) ->
                registry.registerCustomEditor(requiredType, BeanUtils.instantiateClass(editorClass)));
    }
}
```

