## TreeMap Api

### 常见操作

- put
- putAll
- remove
- clear
- replace
- replaceAll
- comparator
- get
- size
- containsValue
- entrySet
- values
- keySet
- clone
- forEach

### Entry操作

- floorEntry：参见Key操作
- higherEntry：参见Key操作
- lowerEntry：参见Key操作
- firstEntry：参见Key操作
- lastEntry：参见Key操作
- ceilingEntry：参见Key操作
- pollFirstEntry：推出最小的值（从小到大排序的话）
- pollLastEntry：推出最大的值（从小到大排序的话）

### Key操作

- firstKey：获取最小的key（从小到大排序的话）
- lastKey：获取最大的key（从小到大排序的话）
- floorKey：精确匹配，匹配不到的话返回小于参数key的最大的值
- ceilingKey：精确匹配，匹配不到的话返回大于参数key的最小的项
- higherKey：获取大于指定key的最小key的项（不包含自身）。没有返回null
- lowerKey：返回小于指定key的最大的项（不包含自身）。没有返回null
- containsKey：是否包含key

### Map操作

- headMap
- descendingMap
- subMap
- tailMap

### 其他

- navigableKeySet
- descendingKeySet

