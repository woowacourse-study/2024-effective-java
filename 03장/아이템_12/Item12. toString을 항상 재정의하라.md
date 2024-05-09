
### 🤔 toString은 언제 사용될까요?

- toString을 호출할 때 ! `(수동)`
- 객체를 println, printf, 문자열 연산자(+), assert 구문에 넘길 때 `(자동)`
- 디버거가 객체를 출력할 때 `(자동)`
- 객체를 참조하는 컴포넌트가 오류 메시지를 로깅할 때 `(자동)`


### 🤔 재정의 해야 돼. 왜?

앞서 말했듯이 <mark class="hltr-yellow"> 내가 직접 호출하지 않아도, 우리도 모르게 toString을 쓴다.
</mark>
즉, 제대로 재정의하지 않는다면, 쓸모없는 메시지가 로그나 프로그램에 남겨진다.

**왜 쓸데없지?** Object의 기본 toString 메서드가 우리가 작성한 클래스에 적합한 문자열을 반환하는 경우는 거의 없다

그래서 toString을 재정의해서  '**간결하면서 사람이 읽기 쉬운 형태의 유익한 정보**'를 반환해야 한다. 

> [!Note] 재정의 안 한 toString 
> PhoneNumber@adbbd : 클래스명@16진수로\_표현한\_해시코드
> 
> 010-3322-1100 이라고 알려주면 더 좋지 않을까?



### 🤔 어떤 경우 해야 돼?

#### 모든 하위 클래스

>'모든 하위 클래스에서 이 메서드를 재정의해라'
> 상위 클래스에서 이미 알맞게 재정의한 경우는 예외 ~!

toString을 잘 구현한 클래스는 사용하기에 훨씬 즐겁고, 그 클래스를 사용한 시스템은 디버깅하기 쉽다.

#### 하위 클래스들이 공유해야 할 문자열 표현이 있는 추상 클래스

대다수의 컬렉션 구현체는 추상 컬렉션 클래스들의 toString 메서드를 상속해 쓴다.

### 🤔 그럼 안해도 되는 건 없어?

정적 유틸리티 클래스나 대부분의 열거타입은 이미 완벽한 toString을 제공하니 따로 재정의하지 않아도 된다.


### 🤔 그럼 어떻게 재정의?

#### 1. 간결하면서 사람이 읽기 쉬운 형태의 유익한 정보를 담아라


 > [!Example]
 > System.out.println(phoneNumber + "에 연결할 수 없습니다.");
 > 
 > -> (재정의 X) PhoneNumber@adbbd에 연결할 수 없습니다.
 > -> (재정의 O) 010-3322-1100에 연결할 수 없습니다.
 
 > [!Example]
 > Map.of(("Jenney", new PoneNumber("010-3322-1100")));
 > 
 > -> (재정의 X) Jenney=PhoneNumber@adbbd
 > -> (재정의 O) Jenney=0103322-1100 
 


#### 2. 그 객체가 가진 주요 정보 모두를 담아라


##### 주요정보가 담기지 않았을 때 문제 

```java
class Data {  
    private final int id;  
    private final String name;  
    private final int age;  
  
    public Data(int id, String name, int age) {  
        this.id = id;  
        this.name = name;  
        this.age = age;  
    }  
    
    @Override  
    public String toString() {  
        return "{ %s , %d }".formatted(name, age);  
    }  

	// 3가지 정보가 다 동일하면 같은 객체하기로 함
    @Override  
    public boolean equals(Object o) {  
        if (this == o) return true;  
        if (o == null || getClass() != o.getClass()) return false;  
        Data data = (Data) o;  
        return id == data.id && age == data.age && Objects.equals(name, data.name);  
    }  
  
    @Override  
    public int hashCode() {  
        return Objects.hash(id, name, age);  
    }  
}
```

Data 객체의 toString을 위와 같이 재정의했을 때 다음 테스트 결과 로그는 어떻게 될까?

```java
@Test  
void test() {  
    assertThat(new Data(1, "켬미", 24))  
            .isEqualTo(new Data(2, "켬미", 24));  
}
```

바로 다음과 같다.

![](https://i.imgur.com/1Y7lVHz.png)


해당 로그만 보면 우리는 이런 생각을 할 수도 있다 "<mark class="hltr-yellow">왜 실패했지, 지금 로그 상으로는 모든 값이 동일한데?!</mark>"

<mark class="hltr-yellow">그러니 최대한 모든 객체를 toStirng에 담는 것이 좋다</mark>


##### + 객체가 거대하거나, 객체 상태가 문자열로 표현하기에 적합하지 않다면 ?

요약 정보를 반환해라

```java
class PhoneNumbers {
	private String cityName;
	private List<PhoneNumber> phoneNumbers;
	
	public PhoneNumbers(String cityName, List<PhoneNumber> phoneNumbers) {
		this.cityName = cityName;
		this.phoneNumbers = phoneNumbers;
	}

	@Override
	public String toString() {
		return "%s 거주자 전화번호부(총 %d개)".format(cityName, phoneNumber.size());
	}
}
```


> 이상적으로는 스스로를 완벽히 설명하는 문자열이어야 한다.


#### 3. 반환 값의 포맷을 문서화할지 정해라

**장점**
- 명확하고, 사람이 읽을 수 있게 된다
- 값 그대로 입출력에 사용하거나, CSV 파일처럼 사람이 읽을 수 있는 데이터 객체로 저장할 수도 있다.
- ex. BigInteger, BigDecimal과 대부분의 기본 타입 클래스


**단점**
- 포맷을 명시하면 계속 포맷에 얽매이게 된다.
- 구체적인 만큼 유연성이 없다

##### 포맷을 명시하든 아니든 여러분의 의도는 명확히 밝혀야한다.


```java
// 전화번호: 포맷 명시 O
// 이 문자열은 "XXX-YYY-ZZZZ" 형태의 12글자로 구성된다.
// XXX 는 지역 코드, YYY는 프리픽스, ZZZZ는 가입자 번호이다
@Override 
public Strng toString() {
	return String.format("%03d-%03d-%04d",
		areaCode, prefix, lineNum);
} 

// 약물: 포맷 명시 X
// 그냥 멋지게 출력 ex)  유형=사랑, 냄새=테레빈유
@Override 
public Strng toString() {
}
```


사실 어떻게 해도 상관 없음
**중요한 것은 toString이 반환한 값에 포함된 정보를 얻어올 수 있는 API를 제공하자**

