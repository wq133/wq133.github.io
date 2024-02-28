## 集合

## 1.Arraylist 和 linkedlist的 区别

共同点：
1. 元素可以重复
2. 有索引
3. 元素有序
4. 线程不安全、效率高
不同点：
ArrayList的底层数据结构是数组（动态数组）
LinkedList的底层数据结构是双向链表

- **是否保证线程安全：** `ArrayList` 和 `LinkedList` 都是不同步的，也就是不保证线程安全；

- **底层数据结构：** `ArrayList` 底层使用的是 **`Object` 数组**；`LinkedList` 底层使用的是 **双向链表** 数据结构（JDK1.6 之前为循环链表，JDK1.7 取消了循环。注意双向链表和双向循环链表的区别，下面有介绍到！）

- **插入和删除是否受元素位置的影响：**
    - `ArrayList` 采用数组存储，所以插入和删除元素的时间复杂度受元素位置的影响。 比如：执行`add(E e)`方法的时候， `ArrayList` 会默认在将指定的元素追加到此列表的末尾，这种情况时间复杂度就是 O(1)。
    - 但是如果要在指定位置 i 插入和删除元素的话（`add(int index, E element)`），时间复杂度就为 O(n)。因为在进行上述操作的时候集合中第 i 和第 i 个元素之后的(n-i)个元素都要执行向后位/向前移一位的操作。
	
    - `LinkedList` 采用链表存储，所以在头尾插入或者删除元素不受元素位置的影响（`add(E e)`、`addFirst(E e)`、`addLast(E e)`、`removeFirst()`、 `removeLast()`），时间复杂度为 O(1)，如果是要在指定位置 `i` 插入和删除元素的话（`add(int index, E element)`，`remove(Object o)`,`remove(int index)`）， 时间复杂度为 O(n) ，因为需要先移动到指定位置再插入和删除
	
- **是否支持快速随机访问：** `LinkedList` 不支持高效的随机元素访问，而 `ArrayList`（实现了 `RandomAccess` 接口） 支持。快速随机访问就是通过元素的序号快速获取元素对象(对应于`get(int index)`方法)。

- **内存空间占用：** `ArrayList` 的空间浪费主要体现在在 list 列表的结尾会预留一定的容量空间，而 LinkedList 的空间花费则体现在它的每一个元素都需要消耗比 ArrayList 更多的空间（因为要存放直接后继和直接前驱以及数据）。

![[article_img/Collection接口关系图..png]]
## 2.Hashmap
![[article_img/Map接口.png]]
### 基础
特点
	1. 无序
	2. 无索引
	3. key唯一value可以重复
	4. 线程不安全
	5. 数据结构： 哈希表


### 底层实现原理

### 1.7和1.8的区别  

#### 1.数组元素类型不同
JDK1.8 HashMap数组元素类型为`Node<K,V>`，JDK1.7 HashMap数组元素类型为`Entry<K,V>`：｜实际就是换了个类名，并没有什么本质不同。
#### 2.数据结构不同
JDK1.7 HashMap 底层是 **数组和链表** 结合在一起使用也就是 **链表散列**。

![[article_img/Jdk1.7的hashMap数据结构图.png]]
JDK1.8后HashMap底层为数组+链表或红黑树

#### 3.hash计算规则不同
JDK 1.8 的 hash 方法 相比于 JDK 1.7 hash 方法更加简化，但是原理不变。
相比于 JDK1.8 的 hash 方法 ，JDK 1.7 的 hash 方法的性能会稍差一点。

#### 4.put操作不同
JDK1.7并没有使用红黑树，如果哈希冲突后，都用链表解决。
区别于JDK1.8的尾部插入，JDK1.7采用头部插入的方式：（就是最后插入的在链表前。）
```
public V put(K key, V value) {     
    // 键为null，将元素放置到table数组的0下标处  
    if (key == null)    
        return putForNullKey(value);   
    // 计算hash和数组下标索引位置  
    int hash = hash(key.hashCode());    
    int i = indexFor(hash, table.length);    
    // 遍历链表，当key一致时，说明该key已经存在，使用新值替换旧值并返回  
    for (Entry<K,V> e = table[i]; e != null; e = e.next) {    
        Object k;    
        if (e.hash == hash && ((k = e.key) == key || key.equals(k))) {    
            V oldValue = e.value;    
            e.value = value;    
            e.recordAccess(this);    
            return oldValue;    
        }    
    }    
      
    modCount++;  
    // 插入链表  
    addEntry(hash, key, value, i);    
    return null;    
}   
  
private V putForNullKey(V value) {   
    // 一样的，新旧值替换  
    for (Entry<K,V> e = table[0]; e != null; e = e.next) {    
        if (e.key == null) {    
            V oldValue = e.value;    
            e.value = value;    
            e.recordAccess(this);    
            return oldValue;    
        }    
    }    
      
    modCount++;    
    // 插入到数组下标为0位置  
    addEntry(0, null, value, 0);    
    return null;    
}   
  
void addEntry(int hash, K key, V value, int bucketIndex) {  
    // 新值头部插入，原先头部变成新的头部元素的next  
    Entry<K, V> e = table[bucketIndex];  
    table[bucketIndex] = new Entry<K, V>(hash, key, value, e);  
    // 计数，扩容  
    if (size++ >= threshold)  
        resize(2 * table.length);  
}
```

在JDK1.8以后，由头插法改成了尾插法，因为头插法还存在一个死链的问题。


#### 5. 扩容机制不一样
JDK1.7
	1. **触发扩容的条件：** 在 JDK 1.7 中，HashMap 的扩容是在达到阈值（`threshold`）时触发的。阈值是指当前容量（`capacity`）乘以加载因子（`loadFactor`）。
	2. **扩容方式：** 扩容时，HashMap 会创建一个新的数组，将原有的键值对重新散列到新的数组中。这个过程需要锁住整个 HashMap，因此在扩容期间，其他线程无法进行读写操作，可能会导致性能瓶颈。
	
	重新计算了每个元素的哈希值，按旧链表的正序遍历链表、在新链表的头部依次插入，即在转移数据、扩容后，容易出现链表逆序的情况：
JDK1.8 
	1. 在默认的数组长度是16，存在一个默认的负载因子（也就是临界值），如果数组长度达到16*0.75 = 12 就会扩容成32。
	2. 链的长度大于8且数组长度大于64的时候，就会将链表转换红黑树。如果只是链表长度大于8但是数组长度小于64的时候，将链表转化为红黑树，以减少搜索时间。
		
	
	在 JDK 1.8 中，`HashMap.Entry` 类型的链表节点在链表长度达到一定程度时会被替换为 `TreeNode`，这是红黑树的实现。这样可以加速在链表上的查找和插入操作。这种改进减小了链表长度，提高了查找效率。
	扩容的并发改进： JDK 1.8 对于扩容的并发性做了改进，使用了更加细粒度的锁机制。
	这样，在进行扩容时，不再需要锁住整个 HashMap，而是只锁住当前正在处理的桶，提高了并发性。

### 链表和红黑树的时间复杂度对比

除了添加元素外，查询和删除效率比链表快

1. 红黑树查询、增加和删除的时间复杂度：O(log2n)

2. 链表的查询和删除的时间复杂度： O(n)，插入为：O(1)

### 为什么HashMap使用红黑树而不是AVL树
1. 红黑树和AVL树都是常见的平衡二叉树，它们的查找，删除，修改的时间复杂度都是 O(log n)
2. 红黑树相比于AVL树，它的插入更快。
3. AVL树和红黑树相比有以下的区别:
- AVL树是更加严格的平衡，因此可以提供更快的查找速度，一般读取查找密集型任务，适用AVL树
- 红黑树更适合插入修改密集型任务
- 通常，AVL树的旋转比红黑树的旋转更加难以平衡和调试


### 线程不安全的原因（考察HashMap和HashTable的区别）
多线程下可能会出现并发问题，HashMap中的方法没有被Sychronize修饰
而HashTable线程安全。
HashMap允许Null键null值，而HashTable不允许

### 怎么扩容

### 底层数组大小为什么是2^n / HashMap 的长度为什么是 2 的幂次方？

为了能让 HashMap 存取高效，尽量较少碰撞，也就是要尽量把数据分配均匀。
我们上面也讲到了过了，Hash 值的范围值-2147483648 到 2147483647，前后加起来大概 40 亿的映射空间，只要哈希函数映射得比较均匀松散，一般应用是很难出现碰撞的。
但问题是一个 40 亿长度的数组，内存是放不下的。所以这个散列值是不能直接拿来用的。用之前还要先做对数组的长度取模运算，得到的余数才能用来要存放的位置也就是对应的数组下标。这个数组下标的计算方法是“ `(n - 1) & hash`”。（n 代表数组长度，&位与运算）。
这也就解释了 HashMap 的长度为什么是 2 的幂次方。

### 扩容死锁产生的过程
JDK1.7 及之前版本的 `HashMap` 在多线程环境下扩容操作可能存在死循环问题，这是由于当一个桶位中有多个元素需要进行扩容时，多个线程同时对链表进行操作，头插法可能会导致链表中的节点指向错误的位置，从而形成一个环形链表，进而使得查询元素的操作陷入死循环无法结束。

为了解决这个问题，JDK1.8 版本的 HashMap 采用了尾插法而不是头插法来避免链表倒置，使得插入的节点永远都是放在链表的末尾，避免了链表中的环形结构。但是还是不建议在多线程下使用 `HashMap`，因为多线程下使用 `HashMap` 还是会存在数据覆盖的问题。并发环境下，推荐使用 `ConcurrentHashMap` 。

## Concurrenthashmap实现原理

### 结构

JDK1.7中是由Segment数组（类似HashMap的结构所以每一个 `HashMap` 的内部可以进行扩容），Segment默认最多个数是16，一旦确认不能更改，默认支持最多 16 个线程并发。


Java7 中 `ConcurrentHashMap` 使用的分段锁，也就是每一个 Segment 上同时只有一个线程可以操作，每一个 `Segment` 都是一个类似 `HashMap` 数组的结构，它可以扩容，它的冲突会转化为链表。但是 `Segment` 的个数一但初始化就不能改变。

Java8 中的 `ConcurrentHashMap` 使用的 `Synchronized` 锁加 CAS 的机制。结构也由 Java7 中的 **`Segment` 数组 + `HashEntry` 数组 + 链表** 进化成了 **Node 数组 + 链表 / 红黑树**，Node 是类似于一个 HashEntry 的结构。它的冲突再达到一定大小时会转化成红黑树，在冲突小于一定数量时又退回链表。


### 为什么线程安全

 在JDK8中,ConcurrentHashMap的底层数据结构与HashMap一样,也是采用“数组+链表+红黑树”的形式。同时,它又采用锁定头节点的方式降低了锁粒度,以较低的性能代价实现了线程安全。底层数据结构的逻辑可以参考HashMap的实现,
 它的线程安全的实现机制如下：
  1. 初始化数组或头节点时,ConcurrentHashMap并没有加锁,而是CAS的方式进行原子替换（原子操作,基于Unsafe类的原子操作API）。 
  2. 插入数据时会进行加锁处理,但锁定的不是整个数组,而是槽中的头节点。所以,ConcurrentHashMap中锁的粒度是槽,而不是整个数组,并发的性能很好。
  3. 扩容时会进行加锁处理,锁定的仍然是头节点。并且,支持多个线程同时对数组扩容,提高并发能力。每个线程需先以CAS操作抢任务,争抢一段连续槽位的数据转移权。抢到任务后,该线程会锁定槽内的头节点,然后将链表或树中的数据迁移到新的数组里。
  4. 查找数据时并不会加锁,所以性能很好。另外,在扩容的过程中,依然可以支持查找操作。  如果某个槽还未进行迁移,则直接可以从旧数组里找到数据。如果某个槽已经迁移完毕,但是整个扩容还没结束,则扩容线程会创建一个转发节点存入旧数组,届时查找线程根据转发节点的提示,从新数组中找到目标数据。
  
  加分回答 ConcurrentHashMap实现线程安全的难点在于多线程并发扩容,
  即当一个线程在插入数据时,若发现数组正在扩容,那么它就会立即参与扩容操作,完成扩容后再插入数据到新数组。在扩容的时候,多个线程共同分担数据迁移任务,每个线程负责的迁移数量是 `(数组长度 。>> 3) / CPU核心数`。 
  也就是说,为线程分配的迁移任务,是充分考虑了硬件的处理能力的。多个线程依据硬件的处理能力,平均分摊一部分槽的迁移工作。另外,如果计算出来的迁移数量小于16,则强制将其改为16,这是考虑到目前服务器领域主流的CPU运行速度,每次处理的任务过少,对于CPU的算力也是一种浪费。


### 分段锁怎么实现  






---
## CopyOnWriteList 



怎么保证线程安全，为什么这么做


