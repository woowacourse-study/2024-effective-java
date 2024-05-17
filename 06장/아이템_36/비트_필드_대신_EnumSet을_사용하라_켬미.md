# Item36. 비트 필드 대신 EnumSet을 사용하라


## 열거한 값들이 주로 집합으로 사용될 경우

<br>

### 과거

각 상수에 서로 다른 2의 거듭 제곱 값을 할당한 정수 열거 패턴을 사용

```java
public class Text {
	public static final int STYLE_BOLD            = 1 << 0; // 1
	public static final int STYLE_ITALIC          = 1 << 1; // 2
	public static final int STYLE_UNDERLINE       = 1 << 2; // 4
	public static final int STYLE_STRIKETHROUGH   = 1 << 3; // 8

	// 매개변수 styles는 0개 이상의 STYLE_ 상수를 비트별 OR한 값이다.
	public void applyStyles(int styles) { ... }
}
```

비트별 OR 를 사용해 여러 상수를 하나의 집합으로 모을 수 있으며, 이렇게 만들어진 집합을 비트 필드라 한다.
```java
text.applyStyles(STYLE_BOLD | STYLE_ITALIC);
```

#### 왜 비트 필드를 사용해?

비트 필드를 사용하면 비트별 연산을 사용해 합집합과 교집합 같은 집합 연산을 효율적으로 수행할 수 있다.

#### 단점은?
정수 열거 상수의 단점을 그대로 지니며, 추가로 다음과 같은 문제까지 안고 있다.

- 해석하기 어렵다
	- 비트 필드 값이 그래도 출력되면 단순한 정수 열거 상수를 출력할 때보다 해석하기 훨씬 어렵다.
- 비트 필드 하나에 녹아 있는 모든 원소를 순회하기도 까다롭다.
- 최대 몇 비트가 필요한지를 API 작성 시 미리 예측하여 적절한 타입 (int | long)을 선택해야 한다.
	- API를 수정하지 않고는 비트 수(36비트 | 64비트)를 더 늘릴 수 없기 때문이다.

<br>

### 현재 - 더 좋은 게 만들어졌어 !

java.util 패키지의 **EnumSet 클래스**는 열거 타입 상수의 값으로 구성된 집합을 효과적으로 표현해준다.

EnumSet 클래스는 열거 타입 상수의 값으로 구성된 집합을 효과적으로 표현해준다.

#### 장점

##### 비트 연산의 장점도 포함
- EnumSet 내부는 비트 벡터로 구현
	- (원소가 64개 이하) 대부분의 경우에 EnumSet 전체를 long 변수 하나로 표현하여 비트 필드에 비견되는 성능을 보여준다.
- removeAll | retainAll 같은 대량 작업은 비트를 효율적으로 처리할 수 있는 산술 연산을 써서 구현

##### 비트 연산의 단점 보안 및 좋은 점
- Set 인터페이스를 완벽히 구현
- 타입 안정
- 다른 어떤 Set 구현체와도 함께 사용 할 수 있다.


#### 위에 EnumSet으로 코드 변환
```java
public class Text {
	public enum Style { BOLD, ITALIC, UNDERLINE, STRIKETHROUGH }

	// 어떤 Set을 넘겨도 되나, EnumSet이 가장 좋다.
	public void applyStyles(Set<Style> styles) { ... }
}
```

```java
text.applyStyles(EnumSet.of(Style.BOLD, Style.ITALIC));
```

#### 그럼 단점은 없어?

단점이라고 하면 불변 EnumSet을 만들 수 없다는 것
