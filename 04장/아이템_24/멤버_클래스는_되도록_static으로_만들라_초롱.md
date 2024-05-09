# 중첩 클래스(nested class)
- 다른 클래스 안에 정의된 클래스
- 자신을 감싼 바같 클래스에서만 쓰여야 한다.
- 그 외의 쓰임새가 있다면 톱레벨 클래스로 만들어야 한다.

## 중첩 클래스의 종류
- 정적 멤버 클래스
- 비정적 멤버 클래스
- 익명 클래스
- 지역 클래스

정적 멤버 클래스를 제외한 클래스들은 내부 클래스(inner class)라고 한다.

# 정적 멤버 클래스
- 일반 클래스와 동일하지만, 다른 클래스 안에 선언되고, 바깥 클래스의 private 멤버에 접근할 수 있다.
- private으로 선언시 바깥 클래스에서만 접근할 수 있다.

```java
public class Sample {
    private String name = "샘플";
    
    private static class PrivateSample {
        public void test() {
            Sample sample = new Sample();
            
            // 바깥 클래스의 private 멤버에 접근
            sample.name = "변경";
        }
    }
}
```

## 사용 시기
- `Map`의 `Entry`와 같이 바깥 클래스가 표현하는 객체의 한 부분(구성요소)일 때 사용
    - 모든 `Entry`가 `Map`과 연관되어 있지만 `Map`은 `Entry`의 `getKey()`, `getValue()`등의 메소드를 직접 사용할 수 없다.
```java
public interface Map<K, V> {
    interface Entry<K, V> {

        K getKey();

        V getValue();

        V setValue(V value);

        boolean equals(Object o);

        int hashCode();

        public static <K extends Comparable<? super K>, V> Comparator<Map.Entry<K, V>> comparingByKey() {
            return (Comparator<Map.Entry<K, V>> & Serializable)
                    (c1, c2) -> c1.getKey().compareTo(c2.getKey());
        }

        public static <K, V extends Comparable<? super V>> Comparator<Map.Entry<K, V>> comparingByValue() {
            return (Comparator<Map.Entry<K, V>> & Serializable)
                    (c1, c2) -> c1.getValue().compareTo(c2.getValue());
        }

        public static <K, V> Comparator<Map.Entry<K, V>> comparingByKey(Comparator<? super K> cmp) {
            Objects.requireNonNull(cmp);
            return (Comparator<Map.Entry<K, V>> & Serializable)
                    (c1, c2) -> cmp.compare(c1.getKey(), c2.getKey());
        }

        public static <K, V> Comparator<Map.Entry<K, V>> comparingByValue(Comparator<? super V> cmp) {
            Objects.requireNonNull(cmp);
            return (Comparator<Map.Entry<K, V>> & Serializable)
                    (c1, c2) -> cmp.compare(c1.getValue(), c2.getValue());
        }

        @SuppressWarnings("unchecked")
        public static <K, V> Map.Entry<K, V> copyOf(Map.Entry<? extends K, ? extends V> e) {
            Objects.requireNonNull(e);
            if (e instanceof KeyValueHolder) {
                return (Map.Entry<K, V>) e;
            } else {
                return Map.entry(e.getKey(), e.getValue());
            }
        }
    }
}
```

# 비정적 멤버 클래스
- static이 붙지 않은 멤버 클래스
- 비정적 멤버 클래스의 인스턴스는 바깥 클래스의 인스턴스와 암묵적으로 연결된다.
    - 비정적 멤버 클래스의 인스턴스 메서드에서 `클래스명.this` 형태로 바깥 인스턴스의 메서드를 호출하거나 바깥 인스턴스의 참조를 가져올 수 있다.
- 바깥 인스턴스 없이는 생성할 수 없다.

```java
public class Sample {
    private String name = "샘플";
    
    public class PublicSample {
        // 바깥 클래스의 메서드 호출
        public void test() {
            Sample.this.method();
        }
    }
    
    public PublicSample createPublicSample() {
        return new PublicSample();
    }
    
    public void method() {
        System.out.println(name);
    }
}
```

## 비정적 멤버 클래스의 인스턴스와 바깥 인스턴스 사이의 관계
```java
Sample sample = new Sample();
PublicSample publicSample1 = sample.createPublicSample();   // 바깥 클래스의 인스턴스 메서드에서 비정적 멤버 클래스의 생성자를 호출하는 방법
PublicSample publicSample2 = sample.new PublicSample();     // `바깥 인스턴스의 클래스.new 멤버클래스()`를 호출해 수동으로 만드는 방법
```
- 이 관계 정보는 비정적 멤버 클래스의 인스턴스 안에 만들어져 메모리 공간을 차지하며, 생성 시간도 더 걸린다.

## 사용시기
- 비정적 멤버 클래스는 어댑터의 역할을 정의할 때 자주 쓰인다.
- `Map`의 `KeySet`과 같은 뷰의 역할을 하는 인스턴스처럼 보이게 하는 것처럼!
```java
public class HashMap<K,V> extends AbstractMap<K,V> implements Map<K,V>, Cloneable, Serializable {
    final class KeySet extends AbstractSet<K> {     // 비정적 멤버 클래스로 구현되어 있다.
        public final int size() {
            return size;
        }

        public final void clear() {
            HashMap.this.clear();
        }

        public final Iterator<K> iterator() {
            return new KeyIterator();
        }

        public final boolean contains(Object o) {
            return containsKey(o);
        }

        public final boolean remove(Object key) {
            return removeNode(hash(key), key, null, false, true) != null;
        }

        public final Spliterator<K> spliterator() {
            return new KeySpliterator<>(HashMap.this, 0, -1, 0, 0);
        }

        public Object[] toArray() {
            return keysToArray(new Object[size]);
        }

        public <T> T[] toArray(T[] a) {
            return keysToArray(prepareArray(a));
        }

        public final void forEach(Consumer<? super K> action) {
            Node<K, V>[] tab;
            if (action == null)
                throw new NullPointerException();
            if (size > 0 && (tab = table) != null) {
                int mc = modCount;
                for (Node<K, V> e : tab) {
                    for (; e != null; e = e.next)
                        action.accept(e.key);
                }
                if (modCount != mc)
                    throw new ConcurrentModificationException();
            }
        }
    }
}
```
## 결로
- 멤버 클래스에서 바깥 인스턴스에 접근할 일이 없다면 무조건 static을 붙여서 정적 멤버 클래스로 만들자!
    - static을 생략하면 바깥 인스턴스로의 숨은 외부 참조를 갖게 된다.
    - 이 참조를 저장하려면 시간과 공간이 소비된다.
    - 가비지 컬렉션이 바깥 클래스의 인스턴스를 수거하지 못해 메모리 누수가 생길 수 있다.
    - 참조가 눈에 보이지 않아 문제의 원인을 찾기도 힘들다.

# 익명 클래스
- 이름이 없는 클래스
- 바깥 클래스의 멤버가 아니다.
- 쓰이는 시점에 선언과 동시에 인스턴스가 만들어진다.
- 어디서든 만들 수 있다.

## 제약 사항
- 비정적인 문맥에서 사용될 때만 바깥 클래스의 인스턴스를 참조할 수 있다.
- 정적 문맥에서라도 상수 변수 이외의 정적 멤버는 가질 수 없다.
- 선언한 지점에서만 인스턴스를 만들 수 있다.
- instanceof 검사나 클래스 이름이 필요한 작업은 수행할 수 없다.
- 여러 인터페이스를 구현할 수 없다.
- 인터페이스를 구현하는 동시에 다른 클래스를 상속할 수 없다.
- 짧지 않으면 가독성이 떨어진다.

```java
public class Calculator {
    private int x;
    private int y;

    public Calculator(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int plus() {
        Operator operator = new Operator() {
            private static final String COMMENT = "더하기"; // 상수
            // private static int num = 10; // 상수 외의 정적 멤버는 불가능
          
            @Override
            public int plus() {
                // Calculator.plus()가 static이면 x, y 참조 불가
                return x + y;
            }
        };
        return operator.plus();
    }
}

interface Operator {
    int plus();
}
```
## 사용 시기
- 즉석에서 작은 함수 객체나 처리 객체를 만드는 데 주로 사용
    - 람다 등장 이후로 람다가 이 역할을 대체
- 정적 팩토리 메서드를 구현할 때 사용되기도 한다.

# 지역 클래스
- 지역 변수를 선언할 수 있는 곳이면 어디서든 선언 가능
- 유효 범위는 지역 변수와 동일
- 멤버 클래스처럼 이름이 있고 반복해서 사용 가능
- 익명 클래스처럼 비정적 문맥에서 사용될 때만 바깥 인스턴스 참조 가능
- 정적 멤버는 가질 수 없으며, 가독성을 위해 짧게 작성
```java
public class Sample {
    private int number;

    public Sample(int number) {
        this.number = number;
    }

    public void test() {
        // 지역변수처럼 선언해서 사용할 수 있다.
        class LocalClass {
            private String name;

            public LocalClass(String name) {
                this.name = name;
            }

            public void print() {
                // 비정적 문맥에선 바깥 인스턴스를 참조 할 수 있다.
                System.out.println(number + name);
            }
        }

        LocalClass localClass = new LocalClass("local");

        localClass.print();
    }
}
```
