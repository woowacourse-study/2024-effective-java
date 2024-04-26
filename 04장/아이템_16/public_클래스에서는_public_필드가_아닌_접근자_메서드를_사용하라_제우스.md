# 아이템 16: public 클래스에서는 public 필드가 아닌 접근자 메서드를 사용하라

잘못된 코드

```java
class Point {
    public double x;
    public double y;
}
```

개선된 코드

```java
class Point {
    private double x;
    private double y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public double setX(double x) {
        this.x = x;
    }

    public double setY(double y) {
        return this.y = y;
    }
}
```

접근자를 제공함으로써 내부 표현 방식을 바꿀 유연성을 얻을 수 있다.

접근자란 getter, setter를 의미한다.

## package-private 또는 private 중첩 클래스

두 경우에는 오히려 좋을 수도 있다.

어차피 중첩 클래스의 클라이언트는 외부 클래스이기 때문이다.

아래는 Item 2의 피자 예제다. 

```java
public abstract class Pizza {

    public enum Topping { HAM, MUSHROOM, ONION, PEPPER, SAUSAGE }

    final Set<Topping> toppings;

    abstract static class Builder<T extends Builder<T>> {

        EnumSet<Topping> toppings = EnumSet.noneOf(Topping.class);

        public T addTopping(Topping topping) {
            toppings.add(topping);
            return self();
        }

        abstract Pizza build();

        protected abstract T self();
    }

    Pizza(Builder<?> builder) {
        toppings = builder.toppings.clone();
    }
}
```

외부 클래스 Pizza와 내부 정적 클래스 Builder가 있다. 

Pizza 생성자에서 Builder의 toppings 필드에 직접 접근하는 게 보이는가?

이렇게 어떤 클래스가 단 하나의 클래스와만 관계를 맺는다면, 내부 클래스로 작성하는 게 좋다. 

이때는 필드에 접근하는 게 아무런 문제가 없을 뿐더러, 오히려 두 클래스의 관계를 이해하기 좋다. 
