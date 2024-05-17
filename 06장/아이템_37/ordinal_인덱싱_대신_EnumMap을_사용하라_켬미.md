# Item37. ordinal 인덱싱 대신 EnumMap을 사용하라


배열이나 리스트에서 원소를 꺼낼 때 ordinal 메서드로 인덱스를 얻는 코드가 있다.

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

이제 정원에 심은 식물들을 배열 하나로 관리하고, 이들을 생애주기별로 묶어보자

생애주기별로 총 3개의 집합을 만들고 정원을 돌며 각 식물을 해당 집합에 넣는다.

<br>

## 이 때 ordinal 값을 배열의 인덱스로 사용해도 되지 않을까?

```java
Set<Plant>[] plantsByLifyCycle = (Set<Plant>[]) new Set[Plant.LifeCycle.values().length];

for(int i=0; i<plantsByLifyCycle.length; i++) {
	plantsByLifyCycle[i] = new HashSet<>();
}

for(Plant p : garden) {
	plantsByLifyCycle[p.lifeCycle.ordinal()].add(p); // 해당 생애주기의 ordinal을 이용
}

// 결과 출력
for(int i=0; i<plantsByLifyCycle.length; i++) {
	System.out.printf("%s: %s \n",
		Plant.LifeCycle.values()[i], plantsByLifyCycle[i]); 
		// 해당 생애주기인 plant를 출력
}
```

### 동작을 할까?

YES

### 문제가 없을까?

NO

- 배열은 제네릭과 호환되지 않으니 비검사 형변환을 수행해야하고 깔끔하게 컴파일되지 않는다.
- 배열은 각 인덱스의 의미를 모르니 출력 결과에 직접 레이블을 달아야한다.
	- 출력 시 `i` -> `Plant.LifeCycle.values()\[i]` 로 설정해줘야 함
- ⭐⭐⭐ 정확한 정숫값을 사용한다는 것을 개발자가 보증해야 한다
	- 정수는 열거 타입과 달리 타입 안전하지 않기 때문
	- 잘못된 값이 들어가도 동작이 되어서 문제를 모르거나, 운 좋으면 `ArrayIndexOutOfBoundsException` 에러 발생 

<br>

## 그럼 뭘 써? 바로 EnumMap !

열가 타입을 키로 사용하도록 설계한 아주 빠른 Map 구현체, 바로 EnumMap !


```java
Map<Plant.LifeCycle, Set<Plant>> plantByLifeCycle =
	new EnumMap<>(Plant.LifeCycle.class);

for(Plant.LifeCycle lc : Plant.LifeCycle.values()) {
	plantByLifeCycle.put(lc, new HashSet<>());
}

for(Plant p : garden) {
	plantByLifeCycle.get(p.lifeCycle).add(p);
}

// 출력
System.out.println(plantByLifeCycle);
```

- 안전하지 않은 형변환은 쓰지 않고
- 맵의 키인 열거타입이 그 자체로 출력용 문자열을 제공하니 출력 결과에 직접 레이블 달 일도 없다.
- 배열 인덱스를 계산하는 과정에서 오류가 날 가능성 봉쇄
- 성능도 비슷
- EnumMap의 생성자가 받는 키 타입의 Class 객체는 한정적 탕비 토큰으로, 런타임 제네릭 타입 정보를 제공

<br>

## Stream도 사용할 수 있다

stream을 사용해 맵을 관리하면 코드를 더 줄일 수 있다.

```java
System.out.println(Arrays.stream(garden)
				  .collect(groupingBy(p -> p.lifeCycle)));
```

### 단점

- 고유한 맵 구현체를 사용했기 때문에 EnumMap을 써서 얻은 공간과 성능 이점이 사라진다.

매개변수 3개 짜리 `Collections.groupingBy` 메서드는 `mapFactory` 매개변수에 원하는 맵 구현체를 명시해 호출할 수 있다.

<br>

### EnumMap의 이점을 가지고 가려면 다음과 같이 ~

```java
System.out.println(Arrays.stream(garden)
				  .collect(groupingBy(p -> p.lifeCycle,
				  () -> new EnumMap<>(LifeCycle.class), toSet())));
```


#### 이렇게하면 EnumMap과 아예 똑같나?

살짝 다름

- EnumMap : 언제나 식물의 생애주기당 하나씩 중첩 맵을 제작
- Stream : 해당 생애주기에 속하는 식물이 있을 때만 제작


<br>

# 두 열거 타입 값들을 매핑

<br>

## Ordinal을 써볼까?

두가지 상태(Phase)를 전이(Transition)와 매핑하는 프로그램

```java
public enum Phase {
	SOLID, LIQUID, GAS;

	public enum Transition {
		MELT, FREEZE, BOIL, CONDENSE, SUBLIME, DEPOSIT;

		private static final Transition[][] = {
			{ null, MELT, SUBLIME },
			{ FREEZE, null, BOIL },
			{ DEPOSIT, CONDENSE, null }
		};

		public static Transition from(Phase from, Phase to) {
			return TRANSITIONS[from.ordinal()][to.ordinal()];
		}
	}
}
```

- 위에 예제와 동일한 단점
- Phase나 Phase.Transition 열거 타입을 수정ㅇ하면서 상전이 표 TRANSITIONS를 함께 수정하지 않거나, 실수가 일어나면 런타임 오류 발생
- null 도 점차 많아진다

<br>

## 그럼 어떡해? -> EnumMap 사용

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
  
        // 맵 초기화  
        private static final Map<Phase, Map<Phase, Transition>>  
                m = Stream.of(values())  
                .collect(  
                        groupingBy(t -> t.from,   
                                () -> new EnumMap<>(Phase.class),   
                                toMap(t -> t.to, t -> t,   
                                        (x, y) -> y,  
                                        () -> new EnumMap<>(Phase.class))));  
          
        public static Transition from(Phase from, Phase to) {  
            return m.get(from).get(to);  
        }  
    }  
}
```
