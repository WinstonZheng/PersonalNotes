# 面向对象思想
## 基础特性
- 继承，定义
    - 优点，
    - 缺点
- 封装

- 多态



## 设计原则
- 单一职责原则(Single Responsibility Principle)<br>
> SRP原话解释，There should never be more than one reason for a class to change.
    
    按照职责来划分类，每个类只有一个职责。这种方式往往会造成以下问题：
    1. 类的数量激增；
    2. 导致类与类之间耦合度较高。<br>
    为了防止这种问题，可以将一个多职责的类去实现不同职责的接口，实现接口的单一职责原则。此外，单一职责原则的应用，对类、接口与方法三者都需要贯彻。

- 里氏替换原则(Liskov Substitution Principle, LSP)<br>
    > If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2 then S is a subtype of T.
    
    所有引用父类的地方，必须能透明地使用子类（不会产生错误和异常）。在调用类时必须使用父类或接口，保证代码的健壮性。该原则规定了子类与父类之间的关系：
    - 子类必须完全实现父类的方法。
    > 在子类扩展中，注意子类是否能完整实现父类的业务？
    如果子类不能完整实现父类的业务，或者父类方法已经在子类产生变化，建议断开父子关系，采用依赖、聚集、组合等关系代替继承。
    
    - 子类可以有自己的个性，但是，向下转型是不正确的（用父类替换子类）。
    
    - 覆盖或实现子类方法时，输入参数可以**放大**。参数放大，意味着重载父类的方法，而非重写，同样保证在在父类调用的地方能用子类替换（由于参数放大，会优先调用父类方法）。
    
    > 注意，重载和重写的区别，重载指的是一个具备相同的方法名称，但是参数类型、数量等不同；而重写指的就是子类实现父类的方法。
    
    - 覆写或实现父类的方法时输出结果可以被缩小。当重写时，这是重写规定；当重载时，由于前一条的规定，同样保证子类替换父类，不会出现问题。
    

- 依赖倒置原则（Dependence Inversion Principle, DIP）
    1. 高层模块不能依赖于底层模块，两者都应该依赖于抽象；
    2. 抽象不应该依赖于细节，细节应该依赖于抽象。
    
> 面向接口编程
    
# Reference
- 《设计模式之禅》
   
    
    
    