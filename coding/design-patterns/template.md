# 模板方法
模板方法模式（Template Method Pattern），

Define the skeleton of an algorithm in an operation, deferring some steps to subclasses.Template Method lets subclasses redefine certain setps of an algorithm without changing the algorithm's structure.（定义一个操作算法的框架，而将一些步骤延迟到子类中。使得子类可以不改变一个算法的结构即可重定义该算法的特定步骤）

抽象模板中两种方法：1. 基本方法，由子类实现，并在模板方法中调用；2. 模板方法，可以有一个或者几个，一般时由一个具体的方法（框架），实现对基本方法的调度。（一般防止恶意操作，模板方法加上final）

## 使用场景
1. 多个子类有公有的方法，并且逻辑基本相同时；
2. 重要、复杂的算法，可以把核心算法设计为模板方法，周边的相关的细节功能则在子类中实现；
3. 重构时，模板方法模式时经常使用的一个模式，把相同的代码抽取到父类中，通过钩子函数约束其行为。

## 实现

```java
// 模板类
public abstract class AbstractClass{
    
    // 基本方法
    protected abstract void doSomething();
    // 基本方法
    protected abstract void doAnything();
    // Hoke，钩子方法
    protected boolean isDoSomething(){
        return true;
    }
    
    // 模板方法
    public void templateMethod(){
        if(this.isDoSomething()){
            this.doSomethin();
        }
        this.doAnything();
    }

}

// 子类
public class ConcreteClass extends AbstractClass{

    protected void doAnything(){
    }
    
    protected boolean isDoSomething(){
        return false;
    }
           
    protected void doSomething(){
    }
}

public class Client{

    public static void main(String[] args){
        ConcreteClass clazz = new ConcreteClass();
        clazz.templateMethod();
    }

}

```

## 优缺点
- 优点
    - 封装不变部分，扩展可变部分；
    - 提取公共代码，便于维护；
    - 行为由父类控制，子类实现；
- 缺点
    - 不符合设计习惯，一般时由抽象类声明抽象的部分，子类实现具体部分。现在抽象类包含具体部分（模板方法），而且受子类影响。



