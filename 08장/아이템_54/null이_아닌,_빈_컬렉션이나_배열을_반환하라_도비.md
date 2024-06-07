

> **핵심정리**
> null이 아닌, 빈 배열이나 컬렉션을 반환하라. null을 반환하는 API는 사용하기 어렵고
오류처리 코드도 늘어난다. 그렇다고 성능이 좋은것도 아니다.


## 들어가기 전에: Java에서의 null란?

#### 역사적 배경
 `null`의 개념은 ALGOL과 같은 초기 프로그래밍 언어에서 유래되었으며, Tony Hoare에 의해 널 참조의 개념이 처음 도입되었다. Tony Hoare는 이를 "가장 큰 실수"라고 언급하였다.
#### 왜 "가장 큰 실수"일까?
1. 오류 발생 가능성 증가
	`null` 참조는 프로그램의 실행 중 예기치 않은 오류를 발생시키기 쉽다. 가장 흔한 예가 NullPointerException(NPE)으로, 이는 Java 프로그램에서 매우 빈번하게 발생하는 예외이다. 이러한 예외는 프로그램의 안정성을 크게 떨어뜨린다.

2. 복잡한 코드 작성 요구
	`null` 참조를 적절히 처리하지 않으면 오류가 발생할 수 있으므로, 모든 참조형 변수 사용 시마다 `null` 체크를 해야 한다. 이는 코드를 복잡하게 만들고 가독성을 저하시킨다.
	
```java
if (object != null) {
    object.method();
} else {
    // 예외 처리
}
```
3. 코드 유지보수 어려움
	`null` 참조로 인해 발생하는 예외는 디버깅을 어렵게 만든다. 어떤 변수가 `null`인지, 왜 `null`인지 추적하는 과정은 시간과 노력을 많이 요구한다. 이는 코드의 유지보수를 어렵게 만든다.
	
4. 설계 철학 문제
	`null` 참조는 객체지향 프로그래밍의 철학과 어긋난다. 객체지향 프로그래밍에서는 모든 객체가 자신의 행동과 상태를 가지고 있어야 하는데, `null`은 아무런 행동도 상태도 가지지 않는 비객체(non-object)이다.


#### null의 정의

`null`은 프로그래밍 언어에서 특별한 리터럴로, 아무런 객체나 값을 참조하지 않는 상태를 나타낸다. Java에서 `null`은 특정 참조 변수가 어떤 객체도 가리키지 않음을 의미한다. 이는 변수에 할당될 수 있는 특별한 값으로, 초기화되지 않은 객체 참조를 나타내는 데 사용된다.

#### null의 특징

- **참조형 변수(Reference Type)에만 사용**: `null`은 객체를 참조하는 변수에만 할당될 수 있다. 기본 데이터 타입(`int`, `float`, `char` 등)에는 `null`을 할당할 수 없다.
- **초기값**: 참조형 변수는 명시적으로 초기화하지 않으면 기본값으로 `null`이 할당된다.
- **메모리 할당 없음**: `null`은 객체가 메모리에 할당되지 않았음을 의미한다. 이는 특정 변수가 유효한 메모리 주소를 가리키지 않음을 나타낸다.

#### null과 관련된 오류

- **NullPointerException**: Java에서 `null` 참조에 대해 메서드를 호출하거나 필드에 접근하려고 할 때 발생하는 런타임 예외이다. 이는 객체가 초기화되지 않은 상태에서 발생할 수 있다.

```java
String str = null;
int length = str.length(); // NullPointerException 발생
```


> 결론: null로 인해 발생되는 잠재점 문제가 많다!
> 잠재적 문제를 방지하기 위한 불필요한 코드가 많아짐.
> null 자체로 Java 철학에 맞지 않은 상황 발생


## 그렇다면 빈 컬렉션과 배열을 이용하자

결론부터 말하자면, 컬렉션이나 배열을 반환해주는 메서드에서, 그 내용이 존재하지 않을 때에는 빈 컬렉션과 빈 배열을 이용하여 반환토록 해주자.


안티 패턴 🤢:
```java
public List<Cheese> getCheeses) {
	if (chessesInStock.isEmpty()) {
		return null;  // 🤮
	}
	return new ArrayList<>(cheesesInStock);
}
```

권장 :
```java
public List<Cheese> getCheeses() {
	return new ArrayList<> (cheesesInStock); // 😘
}
```

또한, 빈 컬렉션으로 반환할 수도 있다.

```java
public List<Cheese> getCheeses() {
	if (chessesInStock.isEmpty()) {
		return Collections.emptyList();  // 😘
	}
	return new ArrayList<>(cheesesInStock);
}
```


배열을 반환할 때도 비슷하다.

```java
private static final Cheesel EMPTY_CHEESE_ARRAY = new Cheese [0];
															  public Cheese[] getCheeses() {
	return cheesesInstock. toArray(EMPTY_CHEESE_ARRAY);
}
```

그렇다고 해서 단순히 성능을 개선할 목적이라면 toArray에 넘기는 배열을 미리 할당하는건 추천하지 않는다고 한다.
오히려 성능이 떨어진다는 연구결과도 있다.

```java
return cheesesInStock. toArray(
		new Cheese[cheesesInStock.size()]
		)
```


