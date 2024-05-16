# [item 34 ] int 상수 대신 열거 타입을 사용하라

**목차**
> * 열거 타입을 지원하기 전
> * 열거 타입과 사용하는 법
> * 열거 타입과 데이터, 동작을 연관짓는 법
> * 열거 타입에서 제공하는 함수


**열거 타입이란?**
> 일정 개수의 상수 값을 정의한 다음, 그 외의 값은 허용하지 않는 타입   
> ex. 사계절, 태양계의 행성, 카드게임의 카드 종류

### 열거 타입을 지원하기 전에 열거 타입을 정의한 법

**(1) 정수 열거 패턴**
```java
public static final int APPLE_FUJI = 0;
public static final int APPLE_PIPPIN = 1;
public static final int APPLE_GRANNY_SMITH = 2;

public static final int ORANGE_NAVEL = 0;
public static final int ORANGE_TEMPLE = 1;
public static final int ORANGE_BLOOD = 2;
```
단점
* 타입 안전을 보장할 방법이 없다.
    * ORANGE_TEMPLE과 APPLE_PIPPIN을 \=\=연산자로 비교해도 컴파일러는 아무런 경고 메시지를 출력하지 않는다.
* 표현력이 좋지 않다.
    * `int i = (APPLE_FUJI - ORANGE_TEMPLE) / APPLE_PIPPIN;`
* 이름공간을 지원하지 않는다.
    * 때문에 어쩔 수 없이 접두어를 써서 이름 충돌을 방지해야 한다.
* 문자열로 출력하기가 다소 까다로우며, 디버거로 살펴보면 숫자로만 보여서 도움이 되지 않는다.

**(2) 문자열 열거 패턴**
```java
public static final int APPLE_FUJI = "APPLE_FUJI";
public static final int APPLE_PIPPIN = "APPLE_PIPPIN";
public static final int APPLE_GRANNY_SMITH = "APPLE_GRANNY_SMITH";

public static final int ORANGE_NAVEL = "ORANGE_NAVEL;
public static final int ORANGE_TEMPLE = "ORANGE_TEMPLE";
public static final int ORANGE_BLOOD = "ORANGE_BLOOD";
```
단점(정수 열거 패턴 보다 더 나쁘다!)
* 상수의 의미를 출력할 수 있지만 문자열 값을 하드코딩 해야한다.
    * 문자열 오타가 있어도 확인할 길이 없다. -> 런타임 버그
*  문자열 비교에 따른 성능 저하


### 열거 타입을 지원한 이후에 열거 타입 정의하는 법
```java
public enum Apple { FUJI, PIPPIN, GRANNY_SMITH }
public enum Orange { NAVEL, TEMPLE, BLOOD }
```
장점
*  열거 타입 선언으로 만들어진 인스턴스들은 딱 하나씩만 존재한다.
* 타입 안전성을 제공한다.
    * \== 연산자로 선언하면 컴파일 오류가 발생한다.
* toString 메서드는 출력하기에 적합한 문자열을 내어준다.
* 열거 타입에는 임의의 메서드나 필드를 추가할 수 있다.
* values()를 제공한다.
* valueOf(String) 메서드를 제공한다.
* 만약 어떤 타입을 삭제했을 때, 그 타입을 참조한 클라이언트 코드는 컴파일 오류가 발생한다.
    * 바람직한 대응 가능

### 열거 타입 상수 각각을 특정 데이터와 연결 짓기

**필드를 추가하면 된다.**   
아래와 같이 필드를 추가하면 열거 타입 상수를 각각 특정 데이터와 연결지을 수 있다.
```java
public enum Planet {
    MERCURY(3.302e+23, 2.439e6),
    VENUS  (4.869e+24, 6.052e6),
    EARTH  (5.975e+24, 6.378e6),
    MARS   (6.419e+23, 3.393e6),
    JUPITER(1.899e+27, 7.149e7),
    SATURN (5.685e+26, 6.027e7),
    URANUS (8.683e+25, 2.556e7),
    NEPTUNE(1.024e+26, 2.477e7);

    private final double mass;           // 질량(단위: 킬로그램)
    private final double radius;         // 반지름(단위: 미터)
    private final double surfaceGravity; // 표면중력(단위: m / s^2)

    // 중력상수(단위: m^3 / kg s^2)
    private static final double G = 6.67300E-11;

    // 생성자
    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
        surfaceGravity = G * mass / (radius * radius);
    }

    public double mass()           { return mass; }
    public double radius()         { return radius; }
    public double surfaceGravity() { return surfaceGravity; }

    public double surfaceWeight(double mass) {
        return mass * surfaceGravity;  // F = ma
    }
}
```


### 상수별 동작을 정의하는 법
그럼 상수별 동작을 적용하는 방법은 무엇일까?

**(1) 추상 메서드를 정의할 수 있다.**   
클래스 내부에 추상 메서드를 정의하면 각 상수별로 동작을 정의할 수 있다.   
이렇게 하면 상수를 추가할 때, 반드시 추상 메서드를 재정의 해야한다. 때문에 각 상수별 동작을 놓지지 못한다.
```java
enum Operation {
    PLUS ("+") {
        @Override
        public double apply(double x, double y) {
            return x+y;
        }
    },
    MINUS ("-") {
        @Override
        public double apply(double x, double y) {
            return x-y;
        }
    },
    TIMES ("*") {
        @Override
        public double apply(double x, double y) {
            return x*y;
        }
    },
    DIVIDE ("/") {
        @Override
        public double apply(double x, double y) {
            return x/y;
        }
    };

    private final String symbol;

    Operation(String symbol) {
        this.symbol = symbol;
    }

    public abstract double apply(double x, double y);
```

#### 만약 상수별 동작을 서로 공유할 때면?
그럼 상수 별로 각각 동작하는 것이 아닌, 서로 같은 동작을 공유한다면 어떨까?   
예를 들어, 아래와 같이 요일을 선언한 열거타입이 있다고 가정해보자.
```java
enum PayrollDay {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY;
}
```
그리고 각각의 요일에는 다음과 같은 동작이 있다.   
* `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY` : 초과 근무 수당이 기본급의 10퍼센트이다.
* `SATURDAY`, `SUNDAY` : 초과 근무 수당이 기본급의 50퍼센트이다.

**기존대로라면, 아래와 같이 동작을 공유하지만 각각 구현해야 할 것이다.**
```java
    MONDAY {
		@Override
        public double pay(double basePay) {
            return basePay * 0.1;
        }
    }, 
    TUESDAY {
    @Override
        public double pay(double basePay) {
            return basePay * 0.1;
        }
	},
    WEDNESDAY {
	    @Override
        public double pay(double basePay) {
            return basePay * 0.1;
        }
    }, 
    THURSDAY {
        @Override
        public double pay(double basePay) {
            return basePay * 0.1;
        }
    }, 
    FRIDAY {
        @Override
        public double pay(double basePay) {
            return basePay * 0.1;
        }
    }, 
    SATURDAY {
        @Override
        public double pay(double basePay) {
            return basePay * 0.5;
        }
    }, 
    SUNDAY {
        @Override
        public double pay(double basePay) {
            return basePay * 0.5;
        }
    };

	public abstract double pay(double basePay)
}
```
이는 매우 많은 중복이 발생한다. 상당히 비효율적이다.

**때문에 이를 해결하기 위해서, switch문을 이용할 수 있다.**
```java
enum PayrollDay {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY;

    private static final int MINS_PER_SHIFT = 8 * 60;

    int pay(double basePay) {
        double overtimePay;

        switch(this) {
            // 주말
            case SATURDAY : case SUNDAY :
                overtimePay = basePay * 0.5;
                break;
            // 주중
            default:
                overtimePay = basePay * 0.1;
        }

        return overtimePay;
    }
}
```
하지만 이 또한, 새로운 값을 추가하는 순간 코드에 오류가 발생할 수 있다.

이를 해결하기 위해 **전략 열거 타입 패턴**을 사용할 수 있다.

### 전략 열거 타입 패턴
전략 열거 타입 패턴은 각 상수별로 전략을 선택하도록 하는 것이다.   
코드는 아래와 같다.
```java
```java
enum PayrollDay {
    MONDAY(PayType.WEEKDAY)
    , TUESDAY(PayType.WEEKDAY)
    , WEDNESDAY(PayType.WEEKDAY)
    , THURSDAY(PayType.WEEKDAY)
    , FRIDAY(PayType.WEEKDAY)
    , SATURDAY(PayType.WEEKEND)
    , SUNDAY(PayType.WEEKEND);

    private final PayType payType; // 전략을 필드로 갖는다.

    PayrollDay(PayType payType) {
        this.payType = payType;
    }

    public int pay(int minutesWorked, int payRate) {
        return payType.pay(minutesWorked, payRate);
    }

    // 전략 열거 타입
    enum PayType { // 전략을 열거 타입으로 선언
        WEEKDAY {
	        @Override
	        public double pay(double basePay) {
	            return basePay * 0.1;
	        }
        },
        WEEKEND {
			@Override
	        public double pay(double basePay) {
	            return basePay * 0.5;
	        }
        };

        abstract int pay(int mins, int payRate);
    }
}
```

- 새로운 상수를 추가할 때 무조건 잔업수당 전략을 선택해야 한다.
- 이 패턴은 `switch`문보다 조금 더 복잡하지만, 더 안전하고 유연하다.

> 단, 기존 열거 타입에 상수별 동작을 혼합해 넣는다면, `switch`문이 더 좋은 선택이 될 수 있다.



### 열거 타입에서 제공하는 함수
#### values 메서드
위에서 제공한 Planet 열거 타입을 이용해서 여덟 행성에서의 무게를 출력해보자.
```java
public class WeightTable {
   public static void main(String[] args) {
      double earthWeight = Double.parseDouble(args[0]);
      double mass = earthWeight / Planet.EARTH.surfaceGravity();
      for (Planet p : Planet.values())
         System.out.printf("%s에서의 무게는 %f이다.%n", p, p.surfaceWeight(mass));
   }
}

```

**values()를 사용했을 때 장점**
* 간편하게 모든 값을 출력할 수 있다.
*  만약 상수를 제거해도 values를 사용한 클라이언트 코드에는 아무런 영향이 없다.

#### toString 함수
열거 타입은 기본적으로 열거타입의 이름을 제공하는 toString 메서드를 제공한다.   
원하는 값이 있다면 아래 처럼 연산자를 반환하도록 오버라이딩 할 수 있다.
```java
public enum Operation { 
	PLUS("+"), 
	MINUS("-"), 
	TIMES("*"), 
	DIVDE("/"); 
	
	private final String symbol; 
	
	Operation(String symbol) {
		this.symbol = symbol; 
	}

	@Override
	public String toString() { // toString 메서드 오버라이딩
		return symbol;
	}
}
```


### valueOf 메서드
valueOf(String) 메서드는 상수 이름을 입력받아 그 이름에 해당하는 상수를 반환해주는 메서드이다.   
valueOf 메서드는 상수 이름만을 반환받기 때문에, toString을 재정의한다고 정의한 값에 따라 valueOf의 내용이 바뀌는 것이 아니다.   
아래 코드를 보자.
```java
public enum Operation { 
	PLUS("+"), 
	MINUS("-"), 
	TIMES("*"), 
	DIVDE("/"); 
	
	private final String symbol; 
	
	Operation(String symbol) {
		this.symbol = symbol; 
	}

	@Override
	public String toString() { // toString 메서드 오버라이딩
		return symbol;
	}
}

public class Main {  
  
    public static void main(String[] args) {  
	    Operation plus1 = Operation.valueOf("PLUS"); // 제대로 반환
        Operation plus2 = Operation.valueOf("+");   // 예외 발생!
    }  
}
```
Operation 열거 타입은 toString을 재정의 했으나, valueOf는 변화가 없다.

만약, toString을 정의한 대로 valueOf를 사용하고 싶으면 어떻게 해야 할까?
즉, `Operation plus2 = Operation.valueOf("+");`를 사용할 수 있는 방법 말이다.
이를 위해서는 우리가 함수를 아래와 같이 재정의 해줘야 한다.
```java
enum Operation {
    PLUS ("+"),
    MINUS ("-"),
    TIMES ("*"),
    DIVIDE ("/");

    private final String symbol;

    Operation(String symbol) {
        this.symbol = symbol;
    }

    @Override
    public String toString() {
        return symbol;
    }

    
    // fromString : toString으로 재정의한 값에 따라 열거 타입을 반환한다.
    
    public static final Map<String, Operation> stringToEnum = Stream.of(values()).collect(Collectors.toMap(Object::toString, e -> e));

    public static Optional<Operation> fromString(String symbol) {
        return Optional.ofNullable(stringToEnum.get(symbol));
    }
}
```
위와 같이 코드를 짜면, `Operation.fromString("+");` 가 가능하다.


#### 결론 : 열거 타입은 언제 쓰는가?
* 필요한 원소를 컴파일타임에 다 알 수 있는 상수집합이라면 항상 열거 타입을 사용하자.
* 열거 타입에 정의된 상수 개수가 영원히 고정 불변일 필요가 없다.
