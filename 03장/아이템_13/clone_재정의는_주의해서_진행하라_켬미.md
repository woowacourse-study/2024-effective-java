# Item13. clone 재정의는 주의해서 진행하라

<br>

## 🤔 Cloneable이 뭔데?

Cloneable은 복제해도 되는 클래스임을 명시하는 용도의 믹스인 인터페이스 (Mixin interface)  
BUT. 아쉽게도 의도한 목적을 제대로 이루지 못했다.

**문제는** clone 메서드가 선언된 곳이 Cloneable이 아니 Object이고 그마저도 protected라는데 있다.   
그래서 Cloneable을 구현하는 것만으로는 외부 객체에서 clone 메서드를 호출할 수 없다.

> 물론 리플렉션을 사용하면 가능하지만, 100% 성공하는 것도 아니다. 

하지만 이런 문제점이 있음에도 알아두면 좋다 (왜? 널리 쓰이고 있으니까)

<br>

## 💡 Clone 메서드를 잘 동작하게끔 해주는 구현 방법

메서드 하나 없는 Cloneable 인터페이스는 무슨일을 할까?

![](https://i.imgur.com/D3EoBxc.png)

<br>

Object의 protected 메서드인 clone의 동작방식을 결정한다.
![](https://i.imgur.com/KTrq7cq.png)

<br>

Cloneable을 구현한 클래스의 인스턴스에서 clone을 호출하면, 그 객체의 필드들을 하나하나 복사한 객체를 반환 

>그렇지 않은 클래스의 인스턴스에서 호출하면 CloneNotSuppertedException을 던진다.

<br>

즉, Cloneable의 경우에는 상위 클래스에서 정의한 protected 메서드의 동작 방식을 변경한 것이다.

<br>

> **일반적으로 인터페이스를 구현한다는 행위의 뜻**
> 
> 인터페이스를 구현한다는 것은 일반적으로 해당 클래스가 그 인터페이스에서 정의한 기능을 제공한다고 선언하는 행위
> 
> 즉, cloneable은 좋은 인터페이스 예시가 이니니 따라하지 X

<br>

실제 실무에서는 Cloneable을 구현한 클래스는 clone 메서드를 public으로 제공하며, 사용자는 당연히 복제가 제대로 이뤄지리라 기대한다.

하지만 이 기대를 만족시키려면 그 클래스와 모든 상위 클래스는 복잡하고, 강제할 수 없고, 허술하게 기술된 프로토콜을 지켜야만 한다. 
그 결과로 깨지기 쉽고, 위험하고, 모순적인 매커니즘이 탄생한다.

<br>

#### clone 메서드 일반 규약

객체는 복사본을 생성해 반환한다. '복사'의 정확한 뜻은 그 객체를 구현한 클래스에 따라 다를 수 있다.
일반적인 의도는 다음과 같다.

1. `x.clone() != x`
2. `x.clone().getClass() == x.getClass`
3. (필수는 아님) `x.clone().equals(x)`

관례상, 이 메서드가 반환하는 객체는 super.clone을 호출해 얻어야한다.
이 클래스와 (object를 제외한) 모든 상위 클래스가 이 관례를 따른다면 다음 식은 참이다.

`x.clone().getClass() == x.getClass()`

관례상, 반환된 객체와 원본 객체는 독립적이어야 한다. 이를 만족하려면 super.clone으로 얻은 객체의 필드 중 하나 이상을 반환 전에 수정해야 할 수도 있다.

---

<br>

**강제성이 없다는 점만 빼면 생성자 연쇄(constructor chaining)와 살짝 비슷한 매커니즘이다.**

즉, clone 메서드가 super.clone이 아닌 생성자를 호출해 얻은 인스턴스를 반환해도 컴파일러는 불평하지 않을 것이다.
하지만 클래스의 하위 클래스에서 super.clone을 호출한다면 잘못된 클래스의 객체가 만들어져, 결국 하위 클래스의 clone 메서드가 제대로 동작하지 않게 된다.

<br>

## 💡 clone 재정의 방법
<br>

### 1. final 클래스일 경우

**clone을 재정의한 클래스가 final이라면 걱정해야 할 하위 클래스가 없으니 이 관례는 무시해도 안전하다.**

 하지만, final 클래스의 clone 메서드가 super.clone을 호출하지 않는다면 Cloneable을 구현할 이유도 없다. Object의 clone 구현의 동작 방식에 기댈 필요가 없기 때문이다.

super.clone()으로 완벽한 복제본을 얻을 수 있고, final 클래스라면 오히려 쓸데없는 복사를 지양한다는 관점에서 보면 불변 클래스는 굳이 clone 메서드를 제공하지 않는게 좋다. 

```java
@Override public PhoneNumber clone() {
	try {
		return (PhoneNumber) super.clone();
	} catch(CloneNotSupportedException e) {
		throw new AssertionError(); // 일어날 수 없는 일이다.
	}
}
```

> 자바의 공변 반환 타이핑을 사용하는 것을 권장한다.

<br>

### 2. 가변 클래스가 가변 객체를 참조하는 경우

#### ✨ clone을 재귀적으로 호출


**다음 클래스를 복제할 수 있도록 만들어보자**

```java
public class Stack {
	private Object[] elements;
	private int size = 0;

	// 생성자, 메서드, ...
}
```

<br>

단순히 super.clone 하면 될까?

<br>

Stack 인스턴스에 필드를 확인해보자
1. `Object[] elements` : 원본이나 복제본 중 하나를 수정하면 다른 하나도 수정되어 불변식을 해친다는 이야기
2. `int size` : 올바른 값 ~ !

즉, 프로그램이 이상하게 동작하거나 NullPointerException이 던져진다.

<br>

**clone 메서드는 사실상 생성자와 같은 효과를 낸다.**   
**즉, clone은 원본 객체에 아무런 해를 끼치지 않는 동시에 복제된 객체의 불변식을 보장해야한다.**

<br>

그래서 Object[] elements 배열의 clone을 재귀적으로 호출해주는 것이 가장 쉽다.

```java
@Override public Stack clone() {
	try {
		Statck result = (Stack) super.clone;
		result.elements = elements.clone();
		return result;
	} catch (CloneNotSupportedException e) {
		throw new AssertionError();
	}
}
```

<br>

#### ✨ clone을 재귀적으로 호출하는 것만으로는 충분하지 않을 때

```java
public class HashTable implements Cloneable {
	private Entry[] buckets = ...;

	private static class Entry {
		final Object key;
		Object value;
		Entry next;

		Entry(Object key, Object value, Entry nexy) {
			this.key = key;
			this.value = value;
			this.next = next;
		}
	}
	// .. 나머지 코드는 생략
}
```

<br>

Stack에서처럼 단순히 버킷 배열의 clone을 재귀적으로 호출해보자

```java
@Override public HashTable clone() {
	try {
		HashTable result = (HashTable) super.clone();
		result.buckets = buckets.clone();
		return result;
	} catch (CloneNotSupportedException e) {
		throw new AssertionError();
	}
}
```

복제본은 자신만의 버킷 배열을 갖지만, 이 배열은 원본과 같은 연결 리스트를 참조하여 원본과 복제본 모두 예기치 않게 동작할 가능성이 생긴다. 
이를 해결하려면 각 버킷을 구성하는 연결 리스트를 복사해야 한다. 

<br>

```java
public class HashTable implements Cloneable {
	private static class Entry {
		final Object key;
		Object value;
		Entry next;
	
		Entry(Object key, Object value, Entry key) {
			// 주입
		}

		// 재귀적으로 호출
		Entry deepCopy() {
			return new Entry(key, vlaue, 
						next == null ? null : next.deepCopy());
		}
	}

	@Override 
	public HashTable clone() {
		try {
			HashTable result = (HashTable) super.clone();
			result.buckets = new Entry[bukets.length];
			for(int i= 0; i < buckets.length; i++) {
				if(buckets[i] != null) {
					result.buckets[i] = buckets[i].deepCopy();
				}
			}
			return result;
		} catch (CloneNotSupportedException e) {
			throw new AssertionError();
		}
	} 
}
```

<br>

HashTable.Entry는 깊은 복사를 지원하도록 보강되었다.
 
 HashTable의 clone 메서드 방식
1. 먼저 적절한 크기의 새로운 버킷 배열을 할당
2. 원래의 버킷 배열을 순회하면서 비지 않은 각 버킷에 대한 깊은 복사 수행
   (이때 Entry의 deepCopy 메서드는 자신이 가리키는 연결 리스트 전체를 복사하기 위해 자신을 재귀적으로 호출)


이 방법은 간단하며, 버킷이 너무 길지 않다면 잘 작동한다. 
하지만 연결 리스트를 복제하는 방법으로는 그다지 좋지 않다.
(리스트가 길면 스택 오버플로를 일으킬 위험이 있기 때문)

이 문제를 피하려면 deepCopy를 **재귀 호출 대신 반복자를 써서 순회하는 방향으로 수정**해야한다.

```java
// 반복자를 써서 순회
Entry deepCopy() {
	Entry result = new Entry(key, value, next);
	for(Entry p = result; p.next != null; p = p.next) {
		p.next = new Entry(p.next.key, p.next.value, p.next,next);
	}
	return result;
}
```
<br>

#### ✨ super.clone을 호출, 객체 다시 생성하는 고수준 메서드 호출

super.clone을 호출하여 얻은 객체의 필드들을 초기 상태로 설정 후, 객체 다시 생성하는 고수준 메서드 호출한다.

buckets 필드를 새로운 버킷 배열로 초기화한 다음 원본 테이블에 담긴 모든 키-값 쌍 각각에 대해 복제본 테이블의 put(key, value) 메서드를 호출해 둘의 내용이 똑같게 해주면 된다.

> 코드는 간단하고 우아하지만, 저수준에서 바로 처리할 때보다 느림
> 또한 필드 단위 객체 복사를 위회하기 때문에 전체 Cloneable 아키텍처와는 어울리지 않는다.

<br>

#### clone을 동작하지 않게 구현해놓고 하위 클래스에서 재정의 못하게 하고 싶은 경우

다음과 같이 clone을 퇴화시켜놓으면 된다.

```java
@Override
protected final Object clone() throws CloneNotSupportedException {
	throw new CloneNotSupportedException();
}
```

<br>

#### Cloneable을 구현한 스레드 안전 클래스를 작성할 때, clone 메서드 동기화

Object의 clone 메서드는 동기화를 신경 쓰지 않았다. 그러니 super.clone 호출 외에 다른 할 일이 없더라고 clone을 재정의하고 동기화해줘야 한다.


---
<br>

> **요약**   
> Cloneable을 구현하는 모든 클래스는 clone을 재정의해야 한다.  
> 이때 접근 제한자는 public으로 반환 타입은 클래스 자신으로 변경한다.   
> 이 메서드는 가장 먼저 supe.clone을 호출한 후 필요한 필드를 전부 적절히 수정한다.
> 
> 일반적으로 이 말은 그 객체의 내부 '깊은 구조'에 숨어 있는 모든 가변 객체를 복사하고, 복제본이 가진 객체 참조 모두가 복사된 객체들을 가리키게 함을 뜻한다.
> 
> 이러한 내부 복사는 주로 clone을 재귀적으로 호출해 구현하지만, 이 방식이 항상 최선인 것은 아니다.  
> 기본 타입 필드와 불변 객체 참조만 갖는 클래스라면 아무 필드도 수정할 필요가 없다.

<br>

## 💡 가능한 다른 선택지는?

복사 생성자와 복사 팩터리라는 더 나은 객체 복사 방식이 있다.


### 복사 생성자


: 자신과 같은 클래스의 인스턴스를 인수로 받는 생성자

```java
public Yum(Yum yum) { ... };
```

<br>

### 복사 팩터리


: 복사 생성자를 모방한 정적 팩터리

```java
public static Yum newInstance(Yum yum) { ... };
```

<br>

### 이들이 Cloneable/clone 보다 나은 점

- 언어 모순적이고 위험천만한 객체 생성 메커니즘(생성자를 사용하지 않는 방식)을 사용하지 않는다.
- 엉성하고 문서화된 규약에 기대지 않는다.
- 정상적인 final 필드 용법과도 충돌하지 않는다.
- 불필요한 검사 예외를 던지지 않는다.
- 형변환도 필요치 않다.
- 해당 클래스가 구현한 '인터페이스' 타입의 인스턴스를 인수로 받을 수 있다.
	- 변환 생성자와 변환 팩터리를 이용하면 클라이언트는 원본의 구현 타입에 얽매이지 않고 복제본의 타입을 직접 선택할 수 있다.  
	  (HashSet 객체 s를 TreeSet 타입으로 복제 가능 -> `new TreeSet<>(s)`)
