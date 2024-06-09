> 작성자: 프람
> 
> 작성 일시: 2024.06.06

### 🎯QUIZ.1
```java 
System.out.println(1.03 - 0.42); //뭐가 출력될까요?
```
<img width="1206" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/b49b8b85-a460-4c8c-95e8-bfadb48cb15d">

### ✅ Answer.1 
<img width="1253" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/0a848766-6703-495c-8782-3350a862836c">

### 🎯QUIZ.2
```java
System.out.println(1.00 - 9 * 0.10) // 뭐가 출력될까요?
```
<img width="1171" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/67b48006-9ac1-4e69-933d-8b68e4d3bc63">


### ✅ Answer2.
<img width="1011" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/6bf5f030-91c9-4305-beee-e30b23d7ce73">



### 이유를 각자 알아봅시다.(말로 설명하겠음)

IEEE 754  - Bias 127 기준 
<img width="1314" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/8557bcac-9686-4ce7-b8f5-69059014b22a">



### 예제. 1024.75 를 계산해보아요  

<img width="1309" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/dab22011-9176-4e7b-bbf0-3fde87476826">


### 가수부가 길어지면?

반올림을 해버린다. 

<img width="1274" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/258214f8-e198-4887-a654-b5a89a673b26">


### 🎯QUIZ.3
우리는 IEEE 754 부동소수점 계산 방식의 한계를 알아보았습니다.

만약 우리가 뱅킹 시스템과 같이 민감한 정보를 다뤄야 할땐 어떨까요?

```java
public class BankingSystem {  
  
    public static void main(String[] args) {  
        double funds = 1.00;  
        int itemBought = 0;  
        for (double price = 0.10; price <= funds; price += 0.10) {  
            funds -= price;  // 1: 0.1 | 2: 0.2 | 3: 0.3 | 4: 0.4  
            itemBought++;  
        }  
        System.out.println(itemBought + "개 구입");  
        System.out.println("잔돈(달러):" + funds);  
    }  
}
```

### ✅ Answer3.
<img width="871" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/f7a86241-e6ed-4d3d-a331-93d0af57f4e0">


정답은: 큰일난다!!!

### 대안

```java
public class BankingSystem {  
    private static final BigDecimal TEN_CENTS = new BigDecimal(".10");  
  
    public static void main(String[] args) {  
        BigDecimal funds = new BigDecimal("1.00");  
        int itemBought = 0;  
        for (BigDecimal price = TEN_CENTS; funds.compareTo(price) >= 0; price = price.add(TEN_CENTS)) {  
            funds = funds.subtract(price);  // 1: 0.1 | 2: 0.2 | 3: 0.3 | 4: 0.4  
            itemBought++;  
        }  
        System.out.println(itemBought + "개 구입");  
        System.out.println("잔돈(달러):" + funds);  
    }  
}
```

### 결과
<img width="658" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/89e46e8e-5a15-498a-9372-719d04876427">


### 문제점 
1. 높은 정확성을 위해 대량의 숫자에 큰 오버헤드 동안한다.
2. 그럼에도 불변 객체로 매번 생성
3. 더하기 add , 빼기 subtract 등 사용하기 복잡하다.


### 대안의 대안?
package java.math.RoundingMode 8가지 라운드 규칙중 적절한 것을 찾아 적용해보자.

<img width="1166" alt="image" src="https://github.com/koust6u/2024-effective-java/assets/111568619/fbcc6be6-84f0-4928-8b8d-109a695fbfc6">


### 결론
민감한 계산은 BigDecimal을 사용하여 구현하자.
