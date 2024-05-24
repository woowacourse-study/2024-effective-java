# 아이템 40 : @Override 애너테이션을 일관되게 사용하라


`@Override` 애너테이션을 일관되게 사용하면 여러 가지 악명 높은 버그들을 예방해준다.

```jsx
public class Bigram {
    private final char first;
    private final char second;
    public Bigram(char first, char second) {
        this.first = first;
        this.second = second;
    }
    public boolean equals(Bigram b) {    // 문제의 부분
        return b.first == first && b.second == second;
    }
    public int hashCode() {
        return 31 * first + second;
    }
    public static void main(String[] args) {
        Set<Bigram> s = new HashSet<>();
        for (int i = 0; i < 10; i++)
            for (char ch = 'a'; ch <= 'z'; ch++)
                s.add(new Bigram(ch, ch));
        System.out.println(s.size());
    }
}
// 26이 출력될 것 같지만, 실제로는 260이 출력된다.
```

확실히 Bigram 작성자는 `equals` 메서드를 재정의하려 한 것으로 보이고 `hashCode`도 함께 재정의해야 한다는 사실을 잊지 않았다. 

그런데 안타깝게도 `equals`를 '**재정의(overriding)**'한 게 아니라 '**다중정의(overloading)**'해버렸다. `Object`의 `equals`를 재정의하려면 매개변수 타입을 `Object`로 해야만 하는데, 그렇게 하지 않은 것이다.

다행히 이 오류는 컴파일러가 찾아낼 수 있지만, 그러려면 아래의 코드처럼 `Object.equals`를 재정의한다는 의도를 명시해야 한다.

```java
@Override 
public boolean equals(Bigram b) {
    return b.first == first && b.second == second;
}
```

상위 클래스의 메서드를 재정의하려는 모든 메서드에 `@Override` 애너테이션을 달자.

### **예외는 한 가지 뿐이다.**

구체 클래스에서 상위 클래스의 **추상 메서드**를 재정의할 때는 굳이 `@Override`를 달지 않아도 된다. 
구체 클래스인데 아직 구현하지 않은 추상 메서드가 남아 있다면 컴파일러가 그 사실을 바로 알려주기 때문이다.

### **@Override는 클래스뿐 아니라 인터페이스의 메서드를 재정의할 때도 사용할 수 있다.**

구현하려는 인터페이스에 디폴트 메서드가 없음을 안다면 이를 구현한 메서드에서는 `@Override`를 생략해 코드를 조금 더 깔끔히 유지해도 좋다.

하지만, 추상클래스나 인터페이스에서는 상위 클래스나 상위 인터페이스의 메서드를 재정의하는 모든 메서드에 `@Override`를 다는것이 좋다.

예컨대 Set 인터페이스는 Collection 인터페이스를 확장했지만 새로 추가한 메서드는 없다. 따라서 모든 메서드 선언에 `@Override`를 달아 실수로 추가한 메서드가 없음을 보장했다.

### **정리**

- 재정의한 모든 메서드에 **`@Override`** 애너테이션을 의식적으로 달면 여러분이 실수했을때 컴파일러가 바로 알려줄 것이다.
- **예외는 한 가지뿐이다.** 구체 클래스에서 상위 클래스의 추상 메서드를 재정의한 경우엔 이 애너테이션을 달지 않아도 된다.(단다고 해서 해로울 것도 없다)