## @Override 애너테이션을 일관되게 사용하라

### @Override  
- 자바 기본 제공 애너테이션
- 메서드 선언에만 달 수 있음.
- 상위 타입의 메서드를 재정의 했음을 뜻함.
- **여러 가지 버그들을 예방할 수 있다.**
```java
public class Bigram {
    private final char first;
    private final char second;

    public Bigram(char first, char second) {
        this.first = first;
        this.second = second;
    }
    
    public boolean equals(Bigram b) {
        return b.first == first && b.second == second;
    }
    
    public int hashCode() {
        return 31 * first + second;
    }
}
```

```java
public static void main(String[] args) {
    Set<Bigram> s = new HashSet<>();
    for (int i = 0; i < 10; i++) {
        for (char ch = 'a'; ch <= 'z'; ch++) {
            s.add(new Bigram(ch, ch));
        }
    }

    System.out.println("s.size() = " + s.size());
}
```
개발자는 26의 출력값을 기대하지만 260이 나온 상황
- equals의 매개변수를 Object가 아닌 Bigram으로 두어, equals 재정의가 아닌 오버로딩을 하는 실수를 범함.
```java
  @Override //Method does not override method from its superclass
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Bigram)) return false;
        Bigram bigram = (Bigram) o;
        return first == bigram.first && second == bigram.second;
    }

```
위와 같이 @Override 애너테이션을 달면 컴파일 오류가 발생해 버그를 예방 할 수 있다.

### 예외
구체 클래스에서 상위 클래스의 추상 메서드를 재정의할 때는 굳이 @Override를 달지 않아도 된다.
- 아직 구현하지 않은 추상 메서드가 남아 있다면 컴파일러가 바로 알려주기 때문.
- 일괄로 애너테이션을 붙여두어도 상관 없다.
