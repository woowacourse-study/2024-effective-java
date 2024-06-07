# [item 58] 전통적인 for 문보다는 for-each 문을 사용하라

전통적인 for문
- 반복자와 인덱스 변수가 코드를 지저분하게 한다. 정말로 필요한 건 원소뿐
- 반복자, 인덱스의 무분별한 등자응로 변수를 잘못 사용할 가능성이 높다.
- 컬렉션인가 배열인가에 따라 코드 형태가 상당히 달라진다.

for-each문
* 반복자와 인덱스 변수를 사용하지 않아서 코드가 깔끔하다.
* 컬렉션과 배열을 모두 처리할 수 있다.
* 중첩 순회시 이점이 더욱 커진다.
    ```java
    enum Suit { CLUB, DIAMOND, HEART, SPADE }
    enum Rank { ACE, DEUCE, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING }
    
    @Test
    @DisplayName("NoSuchElementException 을 던지는 예제")
    public void test() {
        Collection<Suit> suits = Arrays.asList(Suit.values());
        Collection<Rank> ranks = Arrays.asList(Rank.values());
    
        Assertions.assertThrows(NoSuchElementException.class, () ->{
            for (Iterator<Suit> i = suits.iterator(); i.hasNext();) {
                for (Iterator<Rank> j = ranks.iterator(); j.hasNext();) {
                    System.out.println(i.next() + ", " + j.next());
                }
            }
        });
    }
    ``` 
    * j문 안에서는 i.next()를 한번만 불러야 하는데, j가 돌때마다 부름 -> NoSuchElementException을 던진다.
    * 해결 방법은 아래와 같다. 
    ```java
    @Test   
    @DisplayName("정상적으로 동작하는 케이스 but 코드가 복잡해보인다.")
    public void test3() {
    Collection<Face> faces = EnumSet.allOf(Face.class);
    
        for (Iterator<Face> i = faces.iterator(); i.hasNext();) {
            Face elementI = i.next();
            for (Iterator<Face> j = faces.iterator(); j.hasNext();) {
                System.out.println(elementI + ", " + j.next());
            }
        }
    }
    ```
    * 그러나 for-each문으로는 더 쉽게 해결할 수 있다.
    ```java
    @Test
    @DisplayName("for-each의 사용으로 코드가 훨씬 깔끔해진다.")
    public void test4() {
    Collection<Face> faces = EnumSet.allOf(Face.class);
    
        for (Face face1 : faces) {
            for (Face face2 : faces) {
                System.out.println(face1 + ", " + face2);
            }
        }
    }
    ```

> 속도
>  for문과 for-each문과 속도는 그대로다.

for-each문을 사용할 수 없는 경우
* 파괴적인 필터링 : 컬렉션을 순회하면서 선택된 원소를 제거해야 하는 경우에 사용해야 한다.
* 변형 : 리스트나 배열을 순회하면서 원소의 값 일부나 전체를 교체해야 하는 경우 인덱스를 사용해야 한다.
* 병렬 반복 : 컬렉션을 병렬로 순회해야 한다면 각각 반복자와 인덱스 변수를 사용해야 한다.


