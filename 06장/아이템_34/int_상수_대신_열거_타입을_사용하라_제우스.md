# 아이템 34: int 상수 대신 열거 타입을 사용하라

`열거 타입 == Enum `

## Enum 등장 전 

```java
public static final int APPLE_FUJI = 0; 
public static final int APPLE_PIPPIN = 1;
public static final int APPLE_GRANNY_SMITH = 2;

public static final int ORANGE_NAVEL = 0; 
public static final int ORANGE_TEMPLE = 1;
public static final int ORANGE_BLOOD = 2;
```

### 문제

```java
assertThat(APPLE_FUJI == ORANGE_NAVEL).isTrue();        // success
assertThat(APPLE_FUJI - ORANGE_NAVEL).isEqualTo(0);     // success

// unsafe
public Juice makeAppleJuice(int fruit) {
    // ...
}
```

- 타입 안전 아니다.
- 게다가 출력할 때와 디버깅할 때 값으로 보인다. 

## Enum 등장 후

```java
public enum Apple {
    FUJI, PIPPIN, GRANNY_SMITH
}

public enum Orange {
    NAVEL, TEMPLE, BLOOD
}
```

- 싱글턴이다.
- public 이다.
- 확장할 수 없다.
- 타입 안전이다.

```java
// safe
public Juice makeAppleJuice(Apple apple) {
    // ...
}
```

### 구현된 메서드와 인터페이스

```java
public abstract class Enum<E extends Enum<E>> implements Constable, Comparable<E>, Serializable {
    private final String name;
    private final int ordinal;
}
```

- Object
  - `toString()`
  - `equals()`
  - `hashCode()`
  - `clone()`
  - 등등
- `valueOf()`

## 메서드, 필드 선언

```java
public enum Planet {

    MERCURY(3.302e+23, 2.439e6),
    VENUS(4.869e+24, 6.052e6),
    EARTH(5.975e+24, 6.378e6),
    MARS(6.419e+23, 3.393e6),
    JUPITER(1.899e+27, 7.149e7),
    SATURN(5.685e+26, 6.027e7),
    URANUS(8.683e+25, 2.556e7),
    NEPTUNE(1.024e+26, 2.477e7)
    ;

    private static final double G = 6.67e-11;

    private final double mass;
    private final double radius;
    private final double surfaceGravity;

    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
        this.surfaceGravity = G * mass / (radius * radius);
    }

    public double mass() {
        return mass;
    }

    public double radius() {
        return radius;
    }

    public double surfaceGravity() {
        return surfaceGravity;
    }

    public double surfaceWeight(double mass) {
        return mass * surfaceGravity;
    }
}
```

```java
@Test
void planets() {
    String format = "%s에서의 무게는 %f입니다.%n";
    double mass = 65;
    Arrays.stream(Planet.values())
            .forEach(planet -> System.out.printf(format, planet, planet.surfaceWeight(mass)));
}
```

```
// 실행결과
MERCURY에서의 무게는 240.762004입니다.
VENUS에서의 무게는 576.602362입니다.
EARTH에서의 무게는 637.093774입니다.
MARS에서의 무게는 241.843343입니다.
JUPITER에서의 무게는 1611.643022입니다.
SATURN에서의 무게는 678.832408입니다.
URANUS에서의 무게는 576.477795입니다.
NEPTUNE에서의 무게는 723.906415입니다.

Process finished with exit code 0
```

## 상수별 메서드 구현

```java
public enum Operation {

    PLUS,
    MINUS,
    TIMES,
    DIVIDE
    ;

    public abstract double apply(double a, double b);
}
```

- `Enum constant 'DIVIDE' must implement abstract method 'apply(double, double)' in 'Operation'` 에러 메세지

```java
public enum Operation {

    PLUS {
        @Override
        public double apply(double a, double b) {
            return 0;
        }
    },
    MINUS {
        @Override
        public double apply(double a, double b) {
            return 0;
        }
    },
    TIMES {
        @Override
        public double apply(double a, double b) {
            return 0;
        }
    },
    DIVIDE {
        @Override
        public double apply(double a, double b) {
            return 0;
        }
    };

    public abstract double apply(double a, double b);
}
```

```java
import java.util.function.Function;

public enum Operation {

    PLUS("+", (a, b) -> a + b),
    MINUS("-", (a, b) -> a - b),
    TIMES("*", (a, b) -> a * b),
    DIVIDE("/", (a, b) -> a / b);

    private final String symbol;
    private final BiFunction<Double, Double, Double> function;

    Operation(String symbol, BiFunction<Double, Double, Double> function) {
        this.symbol = symbol;
        this.function = function;
    }

    public double apply(double a, double b) {
        return function.apply(a, b);
    }
}
```

```java
private static final Map<String, Operation> stringToOperation =
        Stream.of(values())
                .collect(Collectors.toMap(Objects::toString, Function.identity()));

public static Optional<Operation> fromString(String symbol) {
    return Optional.ofNullable(stringToOperation.get(symbol));
}
```

## 전략 열거 타입 패턴

```java
public enum PayrollDay {

    MONDAY(WEEKDAY),
    TUESDAY(WEEKDAY),
    WEDNESDAY(WEEKDAY),
    THURSDAY(WEEKDAY),
    FRIDAY(WEEKDAY),
    SATURDAY(WEEKEND),
    SUNDAY(WEEKEND)
    ;

    private final PayStrategy payStrategy;

    PayrollDay(PayStrategy payStrategy) {
        this.payStrategy = payStrategy;
    }

    public int pay(int workTime, int payRate) {
        return payStrategy.pay(workTime, payRate);
    }
}

public enum PayStrategy {

    WEEKDAY((workTime, payRate) -> workTime <= 480 ? 0 : (workTime - 480) * payRate / 2),
    WEEKEND((workTime, payRate) -> workTime * payRate / 2)
    ;

    private final BiFunction<Integer, Integer, Integer> overTimePay;

    PayStrategy(BiFunction<Integer, Integer, Integer> overTimePay) {
        this.overTimePay = overTimePay;
    }

    public int pay(int workTime, int payRate) {
        int basePay = workTime * 480;
        return basePay + overTimePay.apply(workTime, payRate);
    }
}
```

## 결론

- 정수 상수 쓰지 말고 열거 타입을 사용하자. 
