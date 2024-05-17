> 작성자: 프람
> 작성 일시: 2024.05.16
> 내용: Effective java 3/E 아이템-36


## 비트 필드란?
과거 컴퓨터 메모리 자원 귀했을 때, 효율적으로 데이터를 저장하기 위해 등장한 개념입니다.

아래 예시를 한번 봅시다.

```java
public class Text {

public static final int STYLE_BOLD = 1 << 0; 			//1
    public static final int STYLE_ITALIC = 1 << 1;		//2
    public static final int STYLE_UNDERLINE = 1 << 2;		//3
    public static final int STYLE_STRIKETHROUGH = 1 << 3;	//4
    
    //매개변수 styles는 0개 이상의 STYLE_ 상수를 비트별 OR한 값이다.
    public void applyStyles(int styles) {
    	//...
    }
}
```

STYLE_BOLD(1), STYLE_ITALIC(2), STYLE_UNDERLINE(4), STYLE_STRIKETHROUGH(8) 4가지의 클래스 변수를 가지고 있습니다. 차례대로 2의 제곱수로 구성되어있습니다.



그렇게 된다면, 해당 클래스 변수를 통해 아래 예시 method인 applyStyles와 같은 메스드의 파라미터에 Bit-wise operation을 통해 클래스의 속성을 찾아주는 형식입니다.



상수를 2의 제곱수로 두고 재활용하게 된다면, 불필요한 메모리 낭비를 줄일 수 있는 메커니즘인거죠.

```java
//사용 예시 (OR 연산)
text.applyStyles(STYLE_BOLD | STYLE_ITALIC);
```



이러한 비트 필드을 이용한다면, 비트별 연산을(합집합, 교집합, 집합 연산)을 효율적으로 수행할 수 있습니다.



다만, 현재는 메모리의 발전으로 이러한 코드를 찾아보기는 들물 것입니다.



그럼에도, 비드 필드가 가지는 문제점을 몇가지 짚어보겠습니다.



1. 해석이 어렵다.
2. 모든 원소를 순회하기 까다롭다.
3. 최대 몇 비트가 필요한지 예측하여야 한다. (API 확장의 어려움)



대안
이런 난해한 코드를 없애주고, 성능 역시 큰 차이가 없는 EnumSet을 사용할 수 있겠습니다.

```java
public class Text {
	public enum Style { BOLD, ITALIC, UNDERLINE, STRIKETHROUGH }
    
    // 어떤 Set을 넘겨도 되나, EnumSet이 가장 좋다.
    public void applyStyles(Set<Style> styles) {
    	// ...
    }    
}
```





Enum Set 역시 내부적으로 Bit 연산을 하기 때문에 속도 역시 bit field와 차이 없다 합니다.

--- 


[[1] Bit Field](http://underpop.online.fr/j/java/hardcore-java/hardcorejv-chp-7-sect-2.html) 

