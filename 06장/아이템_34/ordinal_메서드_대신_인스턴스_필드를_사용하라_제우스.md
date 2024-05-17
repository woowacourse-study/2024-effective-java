# ordinal 메서드 대신 인스턴스 필드를 사용하라

## Before

```java
public enum Ensemble {
    
    SOLO, 
    DUET, 
    TRIO, 
    QUARTET, 
    QUINTET,
    SEXTET,
    SEPTET,
    OCTET,
    NONET,
    DECTET
    ;
    
    public int numberOfMusicians() {
        return ordinal() + 1;
    }
}
```

## After

```java
public enum Ensemble {
    
    SOLO(1), 
    DUET(2), 
    TRIO(3), 
    QUARTET(4), 
    QUINTET(5),
    SEXTET(6),
    SEPTET(7),
    OCTET(8),
    NONET(9),
    DECTET(10)
    ;
    
    private final int numberOfMusicians;

    Ensemble(int numberOfMusicians) {
        this.numberOfMusicians = numberOfMusicians;
    }

    public int numberOfMusicians() {
        return numberOfMusicians;
    }
}
```

## 결론

- `ordinal()`은 `EnumSet`, `EnumMap`과 같이 열거 타입 기반 범용 자료구조에 사용될 목적으로 설계되었다. 
- `ordinal()` 쓰지 마라. 
