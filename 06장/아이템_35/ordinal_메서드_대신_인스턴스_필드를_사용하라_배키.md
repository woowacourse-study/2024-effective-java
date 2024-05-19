# [item 35] ordinal 메서드 대신 인스턴스 필드를 사용하라


> 대부분 열거 타입 상수는 하나의 정수값에 대응된다.

> ordinal 메서드는 각 타입에 해당하는 상수를 반환하는 역할을 한다.


### ordinal 사용 예시

아래 예시를 보자.
아래 열거 타입은 합주단 종류를 나타낸 것이다. numberOfMusicians()를 호출하면 ordinal을 이용하여 합주자의 수를 반환한다.
```java
public enum Ensemble {  
    SOLO, DUET, TRIO, QUARTET, QUINTET,  
    SEXTET, SEPET, OCTET, NONET, DECTET;  
      
    public int numberOfMusicians() { return ordinal() + 1; }  
}
```

### ordinal을 사용하면 안된다.
* 상수 선언 순서를 바꾸는 순간 각 상수에 해당하는 정수 값이 바뀌기 때문이다.
* 만약 8중주가 하나 더 존재한다면 어떻게 추가해야 할까? 할 수 없다.
* 값을 중간에 비워둘 수도 없다.


### 그럼 어떻게 할까?
아래와 같이 인스턴스 필드를 사용하자.
```java
public enum Ensemble {  
    SOLO(1), DUET(2), TRIO(3), QUARTET(4), QUINTET(5),  
    SEXTET(6), SEPET(7), OCTET(8), DOUBLE_QUARTET(8),  
    NONET(9), DECTET(10), TRIPLE_QUARTET(12);  
      
    private final int numberOfMusicians;  
    Ensemble(int numberOfMusicians) {  
        this.numberOfMusicians = numberOfMusicians;  
    }  
    public int numberOfMusicians() { return this.numberOfMusicians; }  
}
```

### 그럼 ordinal은 왜 존재하는가?
EnumSet과 EnumMap과 같이 열거 타입 기반의 범용 자료구조에 쓸 목적으로 설계되었다.
