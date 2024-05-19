

# 들어가기 전에 잠깐 짚고 갈 내용
## 불공변성의 개념

- **불공변(invariant)**: 서로 다른 타입 `Type1`과 `Type2`가 있을 때, `List<Type1>`은 `List<Type2>`의 하위 타입도 상위 타입도 아니다.
- **예시**: `List<String>`은 `List<Object>`의 하위 타입이 아니다.
    - `List<Object>`에는 어떤 객체든 넣을 수 있지만, `List<String>`에는 문자열만 넣을 수 있다.
    - `List<String>`은 `List<Object>`가 하는 일을 제대로 수행하지 못하니 하위 타입이 될 수 없다 (리스코프 치환 원칙에 어긋남).


# 와일드 카드가 필요할 때는 언제인가?
## 불공변보다 유연한 타입이 필요할 때
- **예시**: `ChessBoard` 클래스
```java
public class ChessBoard<E> {
    public ChessBoard();
    public void placePiece(E e);
    public E removePiece();
    public boolean isEmpty();
}
```

- `addAllPieces` 메서드 추가:

```java
public void addAllPieces(Iterable<E> pieces) {
    for (E piece : pieces)
        placePiece(piece);
}
```

- 문제: `Iterable<Pawn>`은 `Iterable<Piece>`로 변환되지 않음.

## 한정적 와일드카드 타입으로 해결

- **생산자 매개변수에 와일드카드 타입 적용**:
    
```java
public void addAllPieces(Iterable<? extends E> pieces) {
    for (E piece : pieces)
        placePiece(piece);
}
```
- **예시**:
```java
ChessBoard<Piece> board = new ChessBoard<>();
Iterable<Pawn> pawns = ...;
board.addAllPieces(pawns);
```

## 소비자 매개변수에 와일드카드 타입 적용

- **기본 코드**:
```java
public void removeAllPieces(Collection<E> box) {
    while (!isEmpty())
        box.add(removePiece());
}
```
- 문제: `Collection<Object>`는 `Collection<Piece>`의 상위 타입이 아님
**와일드카드 타입 적용**:

```java
public void removeAllPieces(Collection<? super E> box) {
    while (!isEmpty())
        box.add(removePiece());
}
```

## 와일드카드 타입을 사용하는 기본 원칙 (PECS)

- **생산자 (Producer)**: `? extends T`
- **소비자 (Consumer)**: `? super T`

### 적용 예시

- `Chooser` 생성자:
```java
public PieceChooser(Collection<T> choices)
```
    
-  수정 후:
```java
public PieceChooser(Collection<? extends T> choices)
```

이렇게 수정하면 타입 안전성을 유지하면서 더욱 유연한 코드를 작성할 수 있다.

## union 메서드 (병합하기)

### 원래의 union 메서드

```java
public static <E> Set<E> union(Set<? extends E> s1, Set<? extends E> s2)
```
- `s1`과 `s2` 모두 `E`의 생산자이니 PECS 공식에 따라 다음처럼 선언해야 한다.
- 수정 후:
```java
public static <E> Set<E> union(Set<? extends E> s1, Set<? extends E> s2)
```
- 반환 타입은 여전히 `Set<E>`임에 주목하자. 반환 타입에는 한정적 와일드카드 타입을 사용하면 안 된다. 유연성을 높여주기는커녕 클라이언트 코드에서도 와일드카드 타입을 써야 하기 때문이다.
- 수정한 선언을 사용하면 다음 코드도 말끔히 컴파일된다.
```java
Set<Pawn> pawns = Set.of(new Pawn(), new Pawn(), new Pawn());
Set<Knight> knights = Set.of(new Knight(), new Knight());
Set<Piece> pieces = union(pawns, knights);
```

- 제대로만 사용한다면 클래스 사용자는 와일드카드 타입이 쓰였다는 사실조차 의식하지 못할 것이다. 받아들여야 할 매개변수를 받고 거절해야 할 매개변수는 거절하는 작업이 알아서 이뤄진다. 클래스 사용자가 와일드카드 타입을 신경 써야 한다면 그 API에 문제가 있을 가능성이 크다.


## 타입 매개변수와 와일드카드: 어떤 선언이 더 나을까?

타입 매개변수와 와일드카드는 공통점이 많아 메서드를 정의할 때 어느 것을 사용해도 괜찮은 경우가 많다. 예를 들어, 리스트에서 두 인덱스의 아이템을 교환(Swap)하는 정적 메서드를 두 방식 모두로 정의할 수 있다. 아래는 각각 비한정적 타입 매개변수(아이템 30)를 사용한 경우와 비한정적 와일드카드를 사용한 경우의 예시이다.

### 비한정적 타입 매개변수를 사용한 Swap 메서드
```java
public static <E> void swap(List<E> list, int i, int j) {
    E temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}
```

### 비한정적 와일드카드를 사용한 Swap 메서드

```java
public static void swap(List<?> list, int i, int j) {
    swapHelper(list, i, j);
}

private static <E> void swapHelper(List<E> list, int i, int j) {
    E temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}
```

### 어떤 선언이 더 나을까?

**기본 규칙**: 메서드 선언에 타입 매개변수가 한 번만 나오면 와일드카드로 대체하라. 비한정적 타입 매개변수라면 비한정적 와일드카드로, 한정적 타입 매개변수라면 한정적 와일드카드로 바꾸면 된다.

### 이유

1. **간결성**: 와일드카드를 사용하면 메서드 선언이 더 간단해진다. 타입 매개변수를 사용하지 않아도 되므로 메서드를 호출하는 클라이언트가 타입 매개변수를 신경 쓸 필요가 없다.
2. **유연성**: 와일드카드를 사용하면 더 유연한 코드를 작성할 수 있다. 다양한 타입의 리스트를 받아들일 수 있기 때문이다.

### 예시

- **비한정적 타입 매개변수 사용**:

```java
public static <E> void swap(List<E> list, int i, int j) {
    E temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}
```

- **비한정적 와일드카드 사용**:
```java
public static void swap(List<?> list, int i, int j) {
    swapHelper(list, i, j);
}

private static <E> void swapHelper(List<E> list, int i, int j) {
    E temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}
```

### 비한정적 와일드카드를 사용하는 경우의 단점

- **직관적이지 않은 코드**: 와일드카드를 사용하는 메서드는 때로는 직관적이지 않을 수 있다. 예를 들어, `swap` 메서드를 와일드카드로 선언하면 리스트에 다시 값을 넣을 때 타입 불일치 오류가 발생할 수 있다. 이를 해결하기 위해 도우미 메서드를 작성해야 하는데, 이는 코드를 복잡하게 만들 수 있다.

### 결론

- **단순한 사용**: 메서드 선언에 타입 매개변수가 한 번만 나오면 와일드카드를 사용하는 것이 일반적으로 더 간단하고 유연하다.
- **복잡한 사용**: 와일드카드로 인해 코드가 복잡해질 수 있는 경우에는 타입 매개변수를 사용하는 것이 더 나을 수 있다.

따라서, 상황에 따라 둘 중 하나를 선택해야 한다. 메서드 선언이 단순하고 직관적이어야 한다면 와일드카드를 사용하고, 와일드카드로 인해 코드가 복잡해진다면 타입 매개변수를 사용하는 것이 좋다고 한다!
