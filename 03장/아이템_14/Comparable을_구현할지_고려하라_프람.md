# Comparable을 구현할지 고려하라

> 작성자: 프람
> 
> 작성일시: 2024\_04\_25  

## 01\. Comparable이란?

아이템 10(equals는 일반 규약을 지켜 재정의할)에서 소개하는 equals와 두가지를 제외한다면 같다.

**equals와 차이점**

1.  동치성 비교에 더해 순서까지 비교할 수 있으며 제네릭하다.
2.  자연적인 순서(natural order)가 있음을 뜻한다.

## 02\. Comparable의 장점

학습 테스트의 예시를 통해 장점을 몇가지 소개하겠다.

1.  Collection sort  
    ex) TreeSet, TreeMap, Arrays.sort, Collections.sort 에서의 정렬 기능있다.  
      
    정렬은 가지고 있는 원소의 Comparable의 구현 메서드인 compareTo를 통해 이루어진다.  
      
    따라서 해당 자료구조를 사용하려거든 원소로 가지고 있는 클래스가 comparable을 구현하고 있는 구현체여야한다.![스크린샷 2024-04-25 오후 3 09 21](https://github.com/koust6u/2024-effective-java/assets/111568619/a08c85fd-3d8a-4696-b5c4-efaefb3cb51d)
2.  Stream API에서의 sort  
    Stream API에서도 보면 stream들의 정렬해주는 sort메서드를 제공해주어 편리한 정렬을 도와준다.  
    아래 String stream을 정렬하고 있는 예시이다.  
      
    단, String의 경우에는 comparable의 구현체이기 때문에 아래와 같이 간단하게 정렬이 가능하다.![image](https://github.com/koust6u/2024-effective-java/assets/111568619/40d671d0-2172-4487-ac9c-26d16214505c)그렇다면 우리가 자체적으로 구현한 class의 경우에는 어떻게 stream에서 정렬해주면 되는지 알아보자.  
      
    우선 아래는 PhoneNumber 클래스는 areaCode, prefix 그리고 lineNumber 값을 가지고 있다.  
      
    우리는 이 클래스의 자연적인 순서를 areaCode → prefix → lineNumber의 순서로 오름차순 정렬을 해야한다고 가정하자.  
      
    이 때 Stream의 sort메서드를 활용할 수 있는 방법을 몇가지 제시하겠다.
3.  ```java 
    public class PhoneNumber {
       private int areaCode;
       private int prefix;
       private int lineNumber;
    
       public PhoneNumber(int areaCode, int prefix, int lineNumber){
         this.areaCode = areaCode;
         this.prefix = prefix;
         this.lineNumber = lineNumber;
      }
    // 생략...
    }
    ```

-   sort 메서드에 Comparator 정렬 순서에 따라 구현해주기  
    
    ![image](https://github.com/koust6u/2024-effective-java/assets/111568619/6b61a664-1b90-4761-adf5-fd49d102abaf)
    
-   하지만 위 코드는 우리가 원하는 바처럼 areaCode → prefix → lineNumber를 정렬하는 것이 아닌 areaCode만을 가지고 정렬을 한다.  
      
    이럴 경우 아래와 같이 comparator construction method 을 사용하여 구현한다.  
    
    ![image](https://github.com/koust6u/2024-effective-java/assets/111568619/c31dd69a-05a6-4556-8051-a2031819b613)
    
-   꽤 단순하고 가독성이 좋게 코드를 짰다고 생각한다. 하지만, 이럴 경우 클라이언트에서 PhoneNumber의 정렬 순서에 대한 정보를 가지고 있게 된다.  
      
    다소 객체지향스럽지 않다.  
    그렇기 때문에 우리는 comparable을 구현하여 캡슐화를 지켜주자! 아래의 코드가 지금 이해가 되지 않아도 좋다.  
      
    추후 언급할 규약 부분에서 더 자세하게 다루겠다.이렇게 Comparable을 구현하고 나니 클라이언트의 stream 코드가 훨씬 깔끔해졌다.👍  
    
    ![image](https://github.com/koust6u/2024-effective-java/assets/111568619/3b68b26a-1bb6-450f-ae1d-93bef65f74ab)
    
  
  ```java
    public class PhoneNumber implements Comparable<PhoneNumber> {
      private int areaCode; private int prefix;
      private int lineNumber;
    //생성자, Getter, Setter
      @Override
      public int compareTo(PhoneNumber pn) {
        int result = Integer.compare(areaCode, pn.areaCode);
        if (result == 0) {
          result = Integer.compare(prefix, pn.prefix);
          if (result == 0) {
            result = Integer.compare(lineNumber, pn.lineNumber);
          }
       }
     return result;
     }
  }
  ```


## 03\. 규약

우선, Comparable의 구현 메서드인 compareTo는  
  
**비교 대상보다 크다면 양수**를,  
  
**같다면 0**을,  
  
그리고 **작다면 음수**를 반환해야한다[\[1\]](https://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html)  
  
이 사실을 알았다면, 더 자세한 규약들을 살펴보자.

```java
int sgn(int x) {
  return (x < 0) ? -1 : ((x == 0) ? 0 : 1);
}
```

> 1.  Comparable을 구현한 클래스는 모든 x, y에 대해 sgn(x.compareTo(y)) == - sgn(y.compareTo(x))여야 한다.(예외의 경우도 동일하다.)

즉, Comparable을 구현한 클래스는 아래 학습 테스트 예시와 반사성을 가져야 한다는 것이다.

![image](https://github.com/koust6u/2024-effective-java/assets/111568619/47725b54-876b-4238-ab10-90441c449a3e)

> 2.  Comparable을 구현한 클래스는 추이성을 보장해야 한다. 즉, (x.comareTo(y)) > 0 && y.compareTo(z) > 0) 이면 x.compareTo(z) > 0 이다.

이 역시, 학습 테스트의 예시를 보고 이해해보자.

![image](https://github.com/koust6u/2024-effective-java/assets/111568619/acd9c488-f175-4a25-b2ec-123dd58e24ba)

> 3.  Comparable을 구현한 클래스는 모든 z에 대해 x.compareTo(y) == 0 이면 sgn(x.compareTo(z)) == sgn(y.compareTo(z))이다.

마지막 필수 규약도 학습 코드를 살펴보자.

![image](https://github.com/koust6u/2024-effective-java/assets/111568619/482cb056-a941-4a8d-aa6c-a5f064ae19f5)

> 4.  권고: (x.compareTo(y) == 0) == (x.equals(y)) 여야 한다.

이 권고 규악은 equals가 논리적 동치성을 따진다는 것을 주목해야한다.  
  
아래 학습 테스트 예시를 보면 BigInteger를 "1.0"으로 초기화 한것과 "1.00"으로 초기화한것은  
  
서로 논리적 동치관계가 아님을 확인할 수 있다.

![image](https://github.com/koust6u/2024-effective-java/assets/111568619/26565406-73eb-4f75-9aaa-d7950f9729bd)

이유는 간단하다. float point에 대한 IEEE 표준 스펙[\[2\]](https://ieeexplore.ieee.org/document/8766229)에 따라 1.0과 1.00 다르게 보는 것은 어쩌면 당연하다.

```java
System.out.println(0.1 + 0.2 == 0.3);
```

또 다른 예

```java
public static void main(String[] args) {
        int i = 1;
        double d = 0.1;

        System.out.println(i -d * 9);

        BigDecimal bd = BigDecimal.valueOf(0.1);
        System.out.println(BigDecimal.valueOf(1).min(bd.multiply(BigDecimal.valueOf(9))));
    }
```

그 이유는 이 코드를 직접 돌려보고 눈으로 확인해보자.

---

## 04\. 구현

규약에 따라 구현하는 방법은 크게 두가지로 앞서 소개한 예시처럼 compareTo 작성하는 것과

```java
public class PhoneNumber implements Comparable<PhoneNumber> {
  private int areaCode;
  private int prefix;
  private int lineNumber;
  //생성자, Getter, Setter

  @Override
    public int compareTo(PhoneNumber pn) {
        int result = Integer.compare(areaCode, pn.areaCode);
        if (result == 0) {
            result = Integer.compare(prefix, pn.prefix);
            if (result == 0) {
                result = Integer.compare(lineNumber, pn.lineNumber);
            }
        }
        return result;
    }
} 
```

다음으로는 연산자 생성 메서드(Comparator construction method)를 만드는 것 두가지로 나뉜다.

```java
public class PhoneNumber implements Comparable<PhoneNumber> { 
    private static final Comparator<BestPhoneNumber> COMPARATOR = Comparator
            .comparingInt(BestPhoneNumber::getAreaCode)
            .thenComparing(BestPhoneNumber::getPrefix)
            .thenComparingInt(BestPhoneNumber::getLineNumber);

    private int areaCode;
    private int prefix;
    private int lineNumber;

    public BestPhoneNumber(int areaCode, int prefix, int lineNumber) {
        this.areaCode = areaCode;
        this.prefix = prefix;
        this.lineNumber = lineNumber;
    }

    @Override
    public int compareTo(BestPhoneNumber pn) {
        return COMPARATOR.compare(this, pn);
    }

//생략 

}
```

두 번째 예시가 더 깔끔해보인다. 하지만 성능 상으로 10%정도의 차이가 있다하지만,  
  
크게 신경 쓸 정도의 오버헤드인가?라는 것을 고민했을 때,  
  
그냥 무시하고 두번째 방법을 쓸것을 추천한다.

## 05\. 결론

정렬이 필요한 객체라면(자연적인 순서가 있다면), comparable을 구현하자!

### 참고자료

[\[1\] Oracle Comparable DOCS](https://docs.oracle.com/javase/8/docs/api/java/lang/Comparable.html)  
  
[\[2\] IEEE 754](https://ieeexplore.ieee.org/document/8766229)
