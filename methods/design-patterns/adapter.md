# 适配器模式
Adapter Pattern, Convert the interface of a class into another interface clients expect. Adapter lets classed work together that couldn't otherwise because of incompatible interfaces.

将一个类的接口变换为客户端所期待的另一种接口，从而使原本因接口不匹配而无法在一起工作的两个类能够一起工作。

适配器模式属于包装模式。

## 使用场景
1. 系统A有一个接口A，当需要操控另外一个系统B的不同操作类B时，适配器模式产生作用，提供一个实现类C实现接口C并扩展B，通过B中的方法实现A中的方法。（系统遵守依赖导致原则和里氏替换原则，则只需要替换创建的子类，就能使用系统B的功能）

注意：适配器模式常用于扩展系统，减少代码修改带来的风险，在设计阶段一般不使用。

## 基本实现

```java
// 需要转换到的目标接口
public interface Target{
    public void request();
}

// 被转换的对象
public class Adaptee{
    public void doSomething(){
        System.out.println("I'm busy.");
    }
}

// 适配器（类适配器）
public class Adapter extends Adaptee implements Target{
    public void request(){
        super.doSomething();
    }
}

public class AdapteeTwo{
    public void doSomething(){
        System.out.println("I'm busy too.");
    }
}


// 适配器扩展，当有多个被转换对象时，可以考虑使用关联的方式进行适配（对象适配器）
public class AdapterExtend implements Target{
    private Adaptee adaptee;
    private AdapteeTwo adapteeTwo;    
    public AdapterExtend(Adaptee adaptee, AdapteeTwo adapteeTwo){
        this.adaptee = adaptee;
        this.adapteeTwo = adapteeTwo;
    }
}

```
类适配器，是类间的继承；对象适配器，是对象的合成关系，也称为关联关系。


## 优点
1. 能够将两种类关联（分别实现各自的接口）；
2. 增加类的透明性；
3. 提高类的复用度；
4. 灵活性，删改对其他的代码无影响。





