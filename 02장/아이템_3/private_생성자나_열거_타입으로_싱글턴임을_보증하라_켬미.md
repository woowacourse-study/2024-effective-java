
# Item3. private 생성자나 열거 타입으로 싱글턴임을 보증하라

<br>

## 싱글톤 (singleton)


: **인스턴스를 오직 하나만 생성**할 수 있는 클래스

> 싱글톤을 사용 해야하는 예
> - 무상태(stateless) 객체
> - 설계상 유일해야하는 시스템 컴포넌트

<br>

### 싱글톤 단점

- 싱글톤을 사용하는 클라이언트를 테스트하기 어려워진다.
  (가짜(mock) 구현 대체 불가능)

<br>

## 싱글톤 구현 방식

> 기본 전제로 모든 방식의 다음 단계는 가진다.
> 1. 생성자는 private으로 감춰준다.
> 2. 유일한 인스턴스에 접근할 수 있는 수단으로 public static 멤버를 하나 마련

<br>

### 💡 1. public 필드 방식


: public static 멤버가 final 필드

```java
public class Kyummi {
	public static final Kyummi INSTANCE = new Kyummi();
	
	private Kyummi() { ... }
}
```

- private 생성자는 public static final 필드인 Kyummi.INSTANCE를 초기화 할 때 한 번만 호출
- 이 외에는 public/protected 생성자가 없으니 생성될 수 없다.

즉, 저 INSTANCE만 만들어져 전체 시스템에서 Kyummi 인스턴스는 하나 뿐임을 보장


#### 장점

- 해당 클래스가 싱글톤임이 API에 명백히 드러난다.
- 간결하다.

<br>

### 💡 2. 정적 팩토리 방식


: 정적 팩토리 메서드를 public static 멤버로 제공

```java
public class Kyummi {
	private static final Kyummi INSTANCE = new Kyummi();
	
	private Kyummi() { ... }
	
	public static Kyummi getInstance() {
		return INSTANCE;
	}
}
```

- `Kyummi.getInstance` 는 항상 같은 객체의 참조를 반환하므로 제 2의 Kyummi는 만들어지지 않는다.

#### 장점
- (마음이 바뀌면) API를 바꾸지 않고도 싱글톤이 아니게 변경 가능하다.
	- getInstance가 새로운 인스턴스를 제작해주도록 쉽게 변경 가능
- 제네릭 싱글톤 팩토리로 만들 수 있다.
- 정적 팩토리의 메서드 참조를 공급자(supplier)로 사용할 수 있다.
	- `Kyummi::getInstance` -> `Supplier<Kyummi>`


> 제네릭(Generics)
> : 클래스 내부에서 사용할 데이터 타입을 외부에서 지정하는 기법
>        ex) `ArrayList<String> list;` 에서 `<>` 가 제네릭

<br>

**제네릭 싱글톤 팩토리**

불변 객체를 여러 타입으로 활용할 수 있게 만들어야 할 때가 있다.
제네릭은 런타임에 타입 정보가 소거되므로 하나의 객체를 어떤 타입으로든 매개변수화할 수 있다.

- 제네릭을 이용한다 (해당 메서드가 실행될 때 사용할 데이터 타입을 외부에서 지정한다.)
	- 매개변수가 무엇이 들어와도 된다.
- 불변 객체

> 제네릭 싱글톤 팩토리 예시
> Collections.reverseOrder . Collections.emptySet


```java
// 불변 객체
private static UnaryOperator<Object> IDENTITY_FN = (t) -> t;

// 어떤 타입으로도 사용 가능
@SuppressWarnings("unchecked")
public static <T> UnaryOperator<T> identityFunction() {
	return (UnaryOperator<T>) IDENTITY_FN;
}
```

<br>

### 그럼 private 생성자는 완전 안전해? No !
권한이 있는 클라이언트는 리플렉션 API인 `AccessibleObject.setAccessible`을 사용해 private 생성자 호출 가능
-> 그래서 private로 객체가 생성되려 할 때 예외를 던지게 하면 된다.


```java
// 켬미가 생각해낸 쉬운 방법
public class Kyummi {
	public static final Kyummi INSTANCE = new Kyummi();
	private static int createKyummiCount = 0;
	
	private Kyummi() { 
		createKyummiCount++;
		if(createKyummiCount > 1) {
			throw new IllegalStateException("Kyummi는 두명일 수 없음!!");
		}
	}
}
```

<br>

### + 위 두 방식으로 만든 싱글톤 클래스 직렬화 방법

> 직렬화
> - 객체들의 데이터를 연속적인 데이터로 변형하여 전송 가능한 형태로 만드는 것
> - 객체(Object) -> Byte, Json, String ....

> 역직렬화
> - 직렬화된 데이터를 다시 객체의 형태로 만드는 것
> - Byte, Json, String .... -> 객체(Object)

<br>
단순히 Serializable을 구현한다고 선언? X !

**readResolve 메서드**를 제공해야 한다.

- 이러지않으면 직렬화된 인스턴스를 역직렬화할 때마다 새로운 인스턴스가 생성된다.
- 위에 예시로 말하면) 가짜 Kyummi가 탄생한다는 말 ! 싫으면 readResolve 메서드 추가

```java
private Kyummi readResolve() {
		return INSTANCE;
		}
```

<br>

### 💡3. 열거 타입 선언 방식

```java
public enum Kyummi {
	INSTANCE;
}
```


#### 장점
- 제일 간결하다
- 추가 노력없이 직렬화할 수 있다.
	- 심지어 아주 복잡한 직렬화 상황이나 공격에서도 제 2의 인스턴스가 생기는 일을 완벽하게 막아준다

원소가 하나뿐인 열거 타입 : **대부분 상황에서는 싱글톤을 만드는 가장 좋은 방법**

단, 만들려는 싱글톤이 Enum 외의 클래스를 상속해야 한다면 사용할 수 없다.

