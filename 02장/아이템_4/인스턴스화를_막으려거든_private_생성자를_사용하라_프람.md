# 아이템04: 인스턴스화를 막으려거든 private 생성자를 사용하라
> 작성자: 프람 <br/>
> 작성일시: 2024_04_17


## 01. 인스턴화가 불필요한 경우

자바로 코드를 작성하다보면 종종 Util class[1]를 만드는 경우가 있다.

그 예시는 JDK 표준 API에서 볼 수 있는데, 대표적으로 `java.lang.Math`가 있다. 

```java
public final class Math {
  ...생략
  public static double sqrt(double a) {
    return StrictMath.sqrt(a);
  }

  public static int abs(int a) {
    return (a < 0) ? -a : a;
  }

  public static double floor(double a) {
        return StrictMath.floor(a);
  }
  생략...
}
```

위 java.lang.Math의 예시 코드와 같이 별도의 인스턴스 변수를 가지지 않고 정적 메서드만을 가지는 class를 util라 한다(일종의 helper class).
따라서, util class의 경우에는 인스턴스화가 불필요하다 볼 수 있다. 

가령 우리가 String를 파싱하는 기능을 가지는 Util class가 있다고 가정해보자.  

```java
public class ParseUtil {
    public static List<String> parseByDelimiter(final String plaintext, final String delimiter) {
        return Arrays.stream(plaintext.split(delimiter))
                .toList();
    }
}
```

아래, 해당 Util class를 사용하는 코드를 사용하는 클라이언트를 보자 <br/>
```java
ParseUtil parseUtil = new ParseUtil();
List<String> parsedNameTextList = parseUtil.parseByDelimiter("프람,호티,배키,켬미,제우스,폰드,도비,초롱", ",");
System.out.println(parsedNameTextList);
```
컴파일러가 ~~(코드 작성자가 생성자를 정의하지 않는 경우)~~ 자동으로 기본 생성자를 만들어주기 때문에,
위 코드 처럼 기본 생성자로 ParseUtils을 인스터스화할 수 있다. <br/> 
  
```java
List<String> parsedNameTextList = ParseUtil.parseByDelimiter("프람,호티,배키,켬미,제우스,폰드,도비,초롱", ",");
System.out.println(parsedNameTextList);
```
이렇게 코드를 대체해도 기능적으로 똑같다. <br/>
따라서, 위 예시가 본 아이템에서 설명하는 불필요한 인스턴스화라고 할 수 있겠다.

## 02. 그래서 인스턴스화를 막으려거든?

### 02-01. 방법1: Util class를 `abstract class`로 만든다.
오라클의 공식 튜토리얼을[2] 살펴보면 `abstract class는 인스턴스화를 할수 없다.` 설명하고 있다.
<img width="1029" alt="oracle-abstract-class-defination" src="https://github.com/koust6u/2024-effective-java/assets/111568619/417890da-b761-4957-9868-7d5f0c58f1ed">

IDE에서도 컴파일 에러로 잡아주고 있는 모습이 아래와 같이 보인다.
<img width="984" alt="abstract-class-impl" src="https://github.com/koust6u/2024-effective-java/assets/111568619/98c89132-3024-4665-800d-bcdb85b8d371">

<img width="1213" alt="abstract-class-client" src="https://github.com/koust6u/2024-effective-java/assets/111568619/3a6152f2-65a1-4d94-ad5c-6b17c967cb27">

하지만, 이 방법에는 몇 가지 문제점이 존재한다.
+ 상속해서 사용하면 그만이다.
+ abstract class의 사용 용도를 생각하여, 다른 개발자가 상속을 해서 사용하라는 뜻으로 오해 할 여지가 생긴다.

### 02-02. 방법2: private 생성자를 사용하라.
아이템의 제목과 같이, 기본 생성자를 private으로 명시적으로 작성한다. <br/> 
```java
public class ParseUtil {

    private ParseUtil() {}

    public static List<String> parseByDelimiter(final String plaintext, final String delimiter) {
        return Arrays.stream(plaintext.split(delimiter))
                .toList();
    }
}

```
이렇게 된다면 컴파일러가 묵시적으로 기본 생성자를 생성하는 것을 막을 수 있다. <br/>
또한, 해당 ***객체 외부에서는 생성자를 호출할 수 없기 때문에 인스턴스화 역시 막을 수 있다.***

하지만! 이 방법에도 문제가 있다.

+ 객체 내부에서는 기본 생성자를 통한 인스턴스화 가능하지 않다.
+ '작성한 코드를 사용하지 않는다?' 논리적인 모순이 생긴다.

따라서 해당 문제를 해결하기 위한 방법은 2가지 있다.
1. private 생성자에 주석으로 **인스턴스가 불가능한 클래스**임을 주석으로 문서화하여 알린다.
2. 아래 예시와 같이 Error를 통해 접근을 불가능함을 알린다.
    ```java
   private ParseUtil() {
        throw new AssertionError("인스턴스화를 할 수 없는 클래스입니다.");
    }

   ``` 

책의 저자는 1번 방법과 2번 방법을 같이 사용할 것을 권장하고 있다. 

```java
//기본 생성자가 만들어지는 것을 막는다(인스턴스 방지용).
private ParseUtil() {
  throw new AssertionError("인스턴스화를 할 수 없는 클래스입니다.");
}
```

## 03. 결론
불필요한 인스턴스화를 막을려거든 private 생성자를 통해 생성자에 대한 접근을 막아줘라.

---
#### 참고자료
[[1]Java Helper vs. Utility Classes](https://www.baeldung.com/java-helper-vs-utility-classes) <br/>
[[2] Abstract Methods and Classes](https://docs.oracle.com/javase/tutorial/java/IandI/abstract.html)

