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

	public double getX() { return x; }
	public double getY() { return y; }

	public double setX(double x) { this.x = x; }
	public double setY(double y) { return this.y = y; }
}
```

접근자를 제공함으로써 내부 표현 방식을 바꿀 유연성을 얻을 수 있다. 

## package-private 또는 private 중첩 클래스

두 경우에는 오히려 좋을 수도 있다. 

```java
class ColorPoint {

	private Point point;
	private Color color;

	ColorPoint(double x, double y, Color color) {
		this.point = new Point(x, y);
		this.color = color;
	}

	class Point {
		double x;
		double y;
	}
}
```

어차피 중첩 클래스의 클라이언트는 외부 클래스이기 때문이다. 