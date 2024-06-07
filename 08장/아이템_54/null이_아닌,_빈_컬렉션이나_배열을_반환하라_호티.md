# 아이템 54: null이 아닌, 빈 컬렉션이나 배열을 반환하라

다음은 주변에서 흔히 볼 수 있는 메서드다

**컬렉션이 비었으면 null을 반환한다. (절대 따라 하면 안되는 코드이다)**

```java
private final List<Cheese> cheesesInStock = ...;

/**
 * @return 매장 안의 모든 치즈 목록을 반환한다.
 * 	단, 재고가 하나도 없다면 null을 반환한다.
 */
public List<Cheese> getCheeses() {
	return cheesesInStock.isEmtpy() ? null
		: new ArrayList<>(cheesesInStock);
}
```

재고가 없다고 해서 특별히 취급할 이유는 없다. 그럼에도 이 코드처럼 null을 반환한다면, 클라이언트는 이 null을 처리하는 코드를 추가로 작성해야 한다.

```java
List<Cheese> cheeses = shop.getCheeses();
if (cheeses != null && cheeses.contains(Cheese.STILTON))
	...
}
```

null을 반환하려면 반환하는 쪽에서도 이 상황을 특별히 취급해줘야 해서 코드가 더 복잡해진다.

### **빈 컨테이너를 할당하는 데도 비용이드니**
**빈 컨테이너보다는 null을 반환하는 것이 나을까?**

이는 두 가지 면에서 틀린 주장이다.

1. 성능 분석 결과 이 할당이 성능 저하의 주범이라고 확인되지 않는 한 
이정도의 성능 차이는 신경 쓸 수준이 못 된다.
`→ retrun new ArraryList<>(cheeseInStock);`
2. 빈 컬렉션과 배열은 굳이 새로 할당하지 않고도 반환할 수 있다.
**예시 :** `(ex. Collections.emptyList, Collections.emptySet, Collections.emptyMap)`

가능성은 작지만, 사용 패턴에 따라 빈 컬렉션 할당이 성능을 눈에 띄게 떨어뜨릴 수도 있다. 
해법은 간단하다, 불변 컬렉션을 반환하는 것이다. 왜냐하면 불변 객체는 자유롭게 공유해도 안전하기 때문이다. 
`(ex. Collections.emptyList, Collections.emptySet, Collections.emptyMap)`

단, 이 역시 최적화에 해당하니 꼭 필요할 때만 사용하자. 
최적화가 필요하다고 판단되면 수정 전화 후의 성능을 측정하여 실제로 성능이 개선되는지 꼭 확인하자

---

이는 배열을 사용할 때도 마찬가지다. 절대 null을 반환하지 말고 길이가 0인 배열을 반환하라.

```java
private static final Cheese[] EMTPY_CHEESE_ARRAY = new Cheese[0];

public Cheese[] getCheeses() {	
	return cheesesInStock.toArray(**EMTPY_CHEESE_ARRAY**);
}
```

> **`<T> T[] toArray(T[] a)`**: 이 메소드는 제네릭을 사용하여, 지정된 타입의 배열을 인자로 받고, 리스트의 요소들을 이 배열에 담아 반환합니다. 
**인자로 전달된 배열의 길이가 리스트의 요소 수보다 크거나 같으면, 리스트의 요소들이 이 배열에 복사되고 반환됩니다**. 
**배열의 길이가 리스트의 요소 수보다 작다면, 메소드는 새로운 배열을 생성하여 그 배열에 요소들을 복사한 후 반환합니다.**
> 
> 
> ```java
> java코드 복사
> List<String> list = new ArrayList<>();
> list.add("apple");
> list.add("banana");
> String[] array = list.toArray(new String[0]); // 빈 배열을 인자로
> 
> ```
> 
> 위 예제에서는 `String[]` 타입의 배열을 반환합니다. 배열 크기가 리스트의 크기보다 작은 경우 (여기서는 0), `toArray` 메소드는 적절한 크기의 새 배열을 만들어서 반환합니다. 이 방식은 타입 안전성을 제공하고, 반환된 배열을 추가적인 타입 캐스팅 없이 바로 사용할 수 있게 해줍니다.
> 

길이 0짜리 배열을 미리 선언해두고 매번 그 배열을 반환하면 된다. 길이 0인 배열은 모두 불변이기 때문이다.

단순히 성능을 개선할 목적이라면 `toArray`에 넘기는 배열을 미리 할당하는 건 추천하지 않는다.
오히려 성능이 떨어진다는 연구결과가 있다

> 특정 상황에서는 `toArray(new T[0])` 방식이 `toArray(new T[size])`보다 빠를 수 있습니다, 이는 내부적으로 최적화되어 있기 때문입니다.
> 

```java
return cheesesInStock.toArray(new Cheese[**cheesesInStock.size()**]);
```

# **정리**

- null이 아닌, 빈 배열이나 컬렉션을 반환하라.
- null을 반환하는 API는 사용하기 어렵고 오류 처리 코드도 늘어난다. 
그렇다고 성능이 좋은 것도 아니다.