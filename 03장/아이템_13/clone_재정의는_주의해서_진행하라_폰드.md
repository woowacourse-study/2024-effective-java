**clone 재정의는 주의해서 진행하라**
## clone 메서드 특징
- Cloneable 인터페이스: 복제해도 되는 클래스임을 명시하는 용도의 믹스인 인터페이스
- Object에 선언: clone 메서드는 Cloneable 인터페이스에 선언 되어 있지 않다.
- native 코드로, 소스코드는 jvm.cpp에 위치
```java
public interface Cloneable {} //마커 인터페이스
```
```java
public class Object {
    ...
    protected native Object clone() throws CloneNotSupportedException;// 실제 선언된 위치
    ...
}
```
- protected 접근 제어자   
## clone 사용 방법
### 동작 방식
- Cloneable 구현 후, clone()을 호출하면, 객체의 필드들을 하나하나 복사(얕은 복사)한 객체를 반환 
- Cloneable을 구현하지 않고, clone() 호출 시 CloneNotSupportedException 발생
>인터페이스를 이례적으로 사용한 방법🤮

### 사용 방법  
실무에서는 clone메서드가 public으로 제공되고, 인스턴스 복제가 제대로 이뤄지길 기대함.  
해당 기대를 만족하기 위한 모순적인 메카니즘(생성자 호출 없이 객체 생성)과 허술한 규약을 지켜야 함.
>x.clone() != x //참  
x.clone().getClass() == x.getClass() //super.clone()을 통해 객체를 얻는다는 관례를 지킨다면 참  
x.clone().equals(x) // 일반적으로 참이지만, 필수 아님.

**올바른 동작을 위한 clone 재정의** 
- 접근제어자 public 변경
- super.clone()을 통한 객체 호출
- try-catch 블록으로 검사 예외(checked exception) 처리  
throws절을 없애줘, 사용하기 편하게 만들어 준다.
- 공변 반환 타이핑으로 클라이언트가 형변환 하지 않게끔 구현.
- 모든 필드가 기본 타입이거나, 불변 객체 참조라면 더 수정할 것이 없다.
```java
@Override 
public PhoneNumber clone() {
	try {
		return (PhoneNumber) super.clone();
	} catch (CloneNotSupportedException e) {
		throw new AssertionError(); 
	}
}
```
**가변 객체를 참조한다면?**

```java
public class Stack implements Cloneable{
  private Object[] elements;🤮
  private int size=0;
  ...
}
```
- **clone의 재귀적 호출**  
  clone을 사용한다면, 원본 elements를 똑같이 참조하기 때문에 원본과 복제본이 서로 영향을 받음.👎  

```java
@Override
public Stack clone() {
  try {
    Stack result = (Stack) super.clone();
    result.elements = elements.clone();
    return result;
  }catch(CloneNotSupportedException e){
    throw new AssertionError();
  }
}
```
스택 내부 정보를 복사→elements 배열의 clone을 재귀적으로 호출해서 해결
>**배열의 clone**  
>형변환 필요 없음   
런타임 타입과 컴파일 타임 타입 모두가 원본 배열과 똑같은 배열을 반환  
> 배열 복제할 때는 clone 사용 권장
> 
elements가 final이었다면 앞선 방식은 작동하지 않음.  
Cloneable 아키텍처는 '가변 객체를 참조하는 필드는 final로 선언하라'는 일반 용법과 충돌🤮  
때문에 일부 필드에서 final 한정자를 제거해야 할 수도 있다.
- **clone의 재귀적 호출 만으로 충분하지 않을 때**
```java
public class HashTable implements Cloneable {
  private Entry[] buckets =...;

  private static class Entry {
    final Object key;
    Object value;
    Entry next;

    Entry(Object key, Object value, Entry next) {
      this.key = key;
      this.value = value;
      this.next = next;
    }
  }
  
  @Override
  public HashTable clone(){
    try{
      HashTable result = (HashTable) super.clone();
      result.buckets = buckets.clone();🤮
      return result;
    } catch (CloneNotSupportedException e){
      throw new AssertionError();
    }
  }
}
```
Stack에서처럼 bucket 배열의 clone을 재귀적으로 호출하면, **원본과 같은 연결리스트를 참조하는 문제** 발생  
**깊은 복사**를 지원해서 각 bucket을 구성하는 연결리스트를 복사해야 한다.  
```java
@Override
	public HashTable clone(){
		try{
			HashTable result = (HashTable) super.clone();
			result.buckets = new Entry[buckets.length];
			for(int i = 0; i < buckets.length; i++){
				if(buckets[i] != null){
					result.buckets[i] = buckets[i].deepCopy();
				}
			}
			return result;
		} catch (CloneNotSupportedException e){
			throw new AssertionError();
		}
	}
```
- 재귀
- 반복자로 순회

### 주의 사항
- clone에서는 하위 클래스에서 재정의 될 수 있는 메서드를 호출하지 않아야 한다.  
원본과 복제본의 상태가 달라질 가능성이 크다.(동적 바인딩)  
- clone 메서드는 적절히 동기화해줘야 한다.  

## 더 나은 객체 복사 방식
### 복사 생성자, 복사 팩터리
- 모순적인 객체 생성 메커니즘 x
- 엉성한 문서 규약 x
- 불필요한 검사 예외 x
- 형변환 필요 x
- 인터페이스 타입의 인스턴스를 인수로 받을 수 있다.
```java
 public TreeSet(Collection<? extends E> c) {
        this();
        addAll(c);
    }
```
