## 싱글턴 
*인스턴스를 오직 하나만 생성할 수 있는 클래스*
- 무상태 객체(stateless)
- 설계상 유일해야 하는 시스템 컴포넌트

>클래스를 싱글턴으로 만들면 이를 사용하는 클라이언트를 테스트하기가 어려워질 수 있다.
> > 타입을 인터페이스로 정의한 다음 그 인터페이스를 구현해서 만든 싱글턴이 아니라면, 가짜 구현으로 대체할 수 없기 때문.

### private 생성자 사용
private을 통해 생성자를 숨김.  
인스턴스에 접근할 유일한 수단: public static 멤버
#### public static 멤버가 final 필드인 방식  
```java
public class Coffee {
    public static final Coffee INSTANCE = new Coffee();

    private Coffee() {
        if (INSTANCE != null) throw new IllegalStateException(); //리플렉션 API를 통한 생성자 호출 방지
    }
}
```
생성자는 Coffee.INSTANCE를 초기화 할 때 한 번만 호출된다.  
인스턴스가 하나뿐임이 보장. 
- 해당 클래스가 싱글턴임이 명백히 드러남.
- 간결하다.
#### public static 멤버가 정적 팩터리 메서드인 방식
```java
public class Coffee {
    private static final Coffee INSTANCE = new Coffee();

    private Coffee() {
    }

    public static Coffee getInstance() {
        if (INSTANCE == null) {//리플렉션 API를 통한 생성자 호출 방지
            return new Coffee();
        }
        return INSTANCE;
    }
}
```
항상 같은 객체의 참조를 반환하므로 인스턴스가 하나뿐임이 보장.
- API를 바꾸지 않고도 싱글턴이 아니게 변경할 수 있음.
- 제네릭 싱글턴 팩토리로 만들 수 있다.
- 정적 팩터리의 메소드 참조를 supplier로 사용할 수 있다. 
  - ```java
     Supplier<Coffee> supplier=Coffee::getInstance;
     ```
위 장점들이 굳이 필요하지 않다면 public static 멤버가 final 필드인 방식이 낫다.
> 예외  
> AccessibleObject.setAccessible() 사용해서 private 생성자에 접근하는 경우  
>> 두 번째 인스턴스가 생성되지 않도록 방어 가능

**역직렬화 문제**  
- 직렬화: 자바에서 사용되는 Object 또는 Data를 다른 컴퓨터의 자바 시스템에서도 사용할 수 있도록 바이트 스트림 형태의 연속적인 데이터로 변환하는 포맷 변환 기술
- 역직렬화: 바이트로 변환 데이터를 원래대로 변환하는 기술

직렬화된 싱글턴 인스턴스를 송신자가 역직렬화 하면 새로운 인스턴스가 생성됨.
>모든 인스턴스 필드에 transient를 추가하고, readResolve 메서드 추가해서 해결 가능
> ```java
> private Object readResolve() {
>       return INSTANCE;
> }
>```


### 원소가 하나인 열거타입 선언(바람직)
```java
public enum Coffee {
    INSTANCE;
}
```
- 간결함
- 역직렬화 문제 없음.
- 리플렉션 문제 없음.
- 대부분의 상황에서 가장 좋은 방법이다.  
단, 다른 클래스를 상속 받아야 한다면 이 방법은 사용 불가.
