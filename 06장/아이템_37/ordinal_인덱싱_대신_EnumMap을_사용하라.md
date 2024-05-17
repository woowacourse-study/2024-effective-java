> 작성자: 프람
> 작성일시: 2024.05.16
> 내용: Effective Java 3/E  아이템-37

## Ordinal 인덱싱
Ordinal이란 Enum class의 상수 선언 순서에 따른 값을 반환해주는 메서드입니다.

더 정확하게는 API 명세를 봅시다.


![image](https://github.com/koust6u/2024-effective-java/assets/111568619/32c05b8c-40ae-4691-84be-d43d6c55ae48)


요약하자면, 첫 번째 상수는 0으로 시작하고 그 뒤로 1씩 증가하여 반환한다고 합니다.

그런데 특이한것은 "대부분의 프로그래머는 이 기능을 사용하지 않는다고 합니다. 단, EnumSet, EnumMap과 같은 곳에서 사용된다고합니다.



이제 부터 왜 대부분의 프로그래머가 Ordinal 메서드를 사용하지 않는지 코드로 알아봅시다. 



**-예시 객체-**
```java
class Plant {
	enum LifeCycle { ANNUAL, PERENNIAL, BIENNIAL }
    
    final String name;
    final LifeCycle lifeCycle;
    
    Plant(String name, LifeCycle lifeCycle) {
    	this.name = name;
        this.lifeCycle = lifeCycle;
	}
    
    @Override
    public String toString() {
    	return name;
    }
}
```

**-클라이언트 코드🤮-**
```java
Set<Plant> garden 
		= new HashSet<>(List.of(new Plant("a", LifeCycle.ANNUAL), new Plant("b", LifeCycle.PERENNIAL)));
        Set<Plant>[] plantsByLifeCycle =(Set<Plant>[]) new Set[LifeCycle.values().length];
        for (int i = 0; i < plantsByLifeCycle.length; i++) {
            plantsByLifeCycle[i] = new HashSet<>();
        }

        for (Plant plant : garden) {
            plantsByLifeCycle[plant.lifeCycle.ordinal()].add(plant);
        }

        for (int i = 0; i < plantsByLifeCycle.length; i++) {
            System.out.printf("%s: %s%n",
                    Plant.LifeCycle.values()[i], plantsByLifeCycle[i]);
        }
}
```

--- 

### EnumMap - 예시1
**문제점**

+ 타입 안전하지 않다
+ OCP 위반
+ ArrayIndexOutOfBoundsException
+ 딱 봐도 사용하지 말아야 겠죠?? 



더 나은 대안은 무엇이 있을까요?



아래와 같이 EnumMap을 사용해 데이터와 열거 타입을 매핑합니다.

**-개선된 클라이언트 코드👍-**

```java
Set<Plant> garden = new HashSet<>(
                List.of(new Plant("a", LifeCycle.ANNUAL), new Plant("b", LifeCycle.PERENNIAL)));

    Map<LifeCycle, Set<Plant>> plantsByLifeCycle = new EnumMap<>(LifeCycle.class);

    for (LifeCycle lifeCycle : LifeCycle.values()) {
        plantsByLifeCycle.put(lifeCycle, new HashSet<>());
    }

    for (Plant plant : garden) {
        plantsByLifeCycle.get(plant.lifeCycle).add(plant);
    }

    System.out.println(plantsByLifeCycle);

    System.out.println(garden
            .stream().collect(groupingBy(p -> p.lifeCycle, () -> new EnumMap<>(LifeCycle.class), toSet())));
}
```

EnumMap을 사용해 데이터와 열거 타입을 매핑합니다.

EnumMap의 성능은 ordinal을 통한 배열 접근과 비슷한 성능을 보이는데, 이는 내부에서 배열을 래핑하고 있기 때문입니다.

이로써 안전성과 성능 두 마리 토끼를 모두 잡을 수 있게 되었습니다.

---

EnumMap 예시-2
**ordinal 사용🤮**

``` java
public enum Phase {
	SOLID, LIQUID, GAS;
    
    public enum Transition {
    	MELT, FREEZE, BOIL, CONDENSE, SUBLIME, DEPOSIT;
        
        // 행은 from의 oridinal을 , 열은 to의 ordinal을 인덱스로 쓴다.
        private static final Transition[][] TRANSITIONS = {
        	{null, MELT, SUBLIME},
            {FREEZE, null, BOIL}, 
            {DEPOSIT, CONDENSe, null}
        };
        
        // 한 상태에서 다른 상태로의 전이를 반환한다.
        public static Transition from(Phase from, Phase to) {
        	return TRANSITIONS[from.ordinal()][to.ordinal()];
        }
}
```





어떤가요?? 이전 ordinal 예시와 같이 똑같은 문제점들이 보이시나요?

+ IndexOutOfBoundsException 
+ NullPointerException
+ OCP 위반

**EnumMap사용👍**
```java
public enum Phase {
	SOLID, LIQUID, GAS;
    
    public enum Transition {
    	MELT(SOLID, LIQUID), FREEZE(LIQUID, SOLID),
        BOIL(LIQUID, GAS), CONDENSE(GAS, LIQUID),
        SUBLIME(SOLID, GAS), DEPOSIT(GAS, SOLID);
        
        private final Phase from;
        private final Phase to;
        
        Transition(Phase from, Phase to) {
        	this.from = from;
            this.to = to;
        }
        
        // 상전이 맵을 초기화한다.
        private static final Map<Phase, Map<Phase, Transition>> m 
        = Stream.of(values()).collect(groupingBy(t -> t.from,
        	toMap(t -> t.to, t -> t, 
            	(x,y) -> y, () -> new EnumMap<>(Phase.class))));
         
        public static Transition from(Phase from, Phase to) {
        	return m.get(from).get(to);
        }
}
```
--- 

결론
ordinal은 절대 사용하지말고, EnumMap, EnumSet으로 사용하자 !!
