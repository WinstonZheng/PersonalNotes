# 观察者模式
观察者模式也叫发布-订阅模式，主要角色分为观察者（接口）与被观察者（接口），被观察者状态改变，通知观察者做出对应的行为（类似于异步的回调函数）。

## 使用场景
著名的发布订阅方式，当一个类状态变化，需要通知另一个类做相应的操作。
1. 关联行为场景（可拆分）；
2. 事件多级触发；
3. 跨系统的消息交换场景，如消息队列的处理机制。


## 实现

```java
// 基础实现
// 抽象观察者
public abstract class Subject{
    // 维护一个观察者数组
    private List<Observer> obsList = new Vector<>();
    // 增加观察者
    public void addObserver(Observer o){
        obsList.add(o);
    }
    // 删除一个观察者
    public void deleteObserver(Observer o){
        obsList.delete(o);
    }
    // 通知所有观察者
    public void notifyObservers(){
        for(Observer obs : this.obsList){
            obs.update();
        }
    }
    
}
// 具体观察者
public class ConcreteSubject extends Subject{
    public void doSomething{
        /**
        * do something.
        **/
        super.notifyObservers();
    }
}
//抽象观察者
public interface Observer{
    // 更新方法
    public void update();
}
// 具体观察者
public class ConcreteObserver implements Observer{
    public void update(){
        System.out.println("观察者进行处理操作！");
    }
}



```


## 优缺点
- 优点
    - 被观察者和观察者是抽象耦合，具备良好的可扩展性；
    - 形成一条触发机制。
- 缺点
    - 开发效率，一对多，开发调试复杂；（观察者可能具备两个身份，也就是串成链，建议最多传递两次）
    - 运行效率（异步），默认顺序执行，其中一个链条断了，影响整体执行效率；


> 广播链和责任链？广播链消息随时更改，而责任链消息基本保持不变。

## MessageQueue

## 扩展

- 注意在java中，实现了Observable和Observer接口，可以用；
- 被观察者状态改变，调用观察者方法，实际上就是给观察者发送一条消息，也就是在一般情况下，观察者被调用的接口传入两个参数，一个是被观察者；另一个是消息DTO；
- 面对观察者的复杂业务逻辑，观察者需要快速响应，考虑采用两种方法：1. 多线程（异步架构）；2. 缓存技术（同步框架）；
- 减少观察者的工作负担，如果不需要通知观察者，直接在被观察者中判断。



