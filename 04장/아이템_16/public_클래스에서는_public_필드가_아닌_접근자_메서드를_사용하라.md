# [item 16] public 클래스에서는 public 필드가 아닌 접근자 메서드를 사용하라

---

### public 클래스에서 가변 필드의 접근 제한자를 public으로 사용하는 경우 문제점
아래 클래스를 보자.
```java
class Point {
	public double x; // 멤버 변수의 접근 제한자가 public!
	public double y;
}
```
public 필드를 제공하면 아래와 같은 단점이 있다.
* 불변식을 보장할 수 없다.
* API(톱 레벨 클래스)를 수정하지 않고서 내부 구현을 바꿀 수 없다.

> API를 수정하지 않고서 내부 구현을 바꿀 수 없다는 말은 무엇일까?
> 아래 코드가 있다.
```java
public class MyClass {
    public int myField;
    
    public MyClass(int myField) {
        this.myField = myField;
    }
}
```
```java
public class AnotherClass {
    public void doSomething(MyClass obj) {
        System.out.println(obj.myField);
    }
}
```
> 만약, 여기서 MyClass의 필드가 private으로 바뀐다면, 
> AnotherClass.doSomething(MyClass obj)의 obj.myField 사용에서 컴파일 오류가 난다.
> 이는 두 클래스 모두를 수정해야하는 상황이 온다. 이런 상황을 말하는 것이다.

---

### 해결 방법
위에서 말한 문제점을 해결하기 위해 필드를 private으로 바꾸고 public 접근자를 추가한다.
```java
public Point {
	private double x;
	private double y;

	public Point(double x, double y) {
		this.x = x;
		this.y = y;
	}

	public double getX() {return x;}
	public double getY() {return y;}
	public void setX(double x) { this.x = x; }
	public void setY(double y) { this.y = y; }
```
이와 같이 코드를 작성하면 아래와 같은 장점이 있다.
* 내부 표현을 마음대로 바꿀 수 있다. 이전에는 클라이언트가 필드를 직접 참조하여 내부 표현을 바꾸기가 어려웠지만 지금은 사용하지 않기 때문에 쉽다.

---

### 불변 객체를 참조하는 public 필드라면?
직접 노출시 단점이 조금은 줄어들지만, 좋은 생각이 아니다.
* API를 변경하지 않고는 표현 방식을 바꿀 수 없다.
* 필드를 읽을 때 부수작업을 수행한다.
  단, 불변식은 보장할 수 있다.
