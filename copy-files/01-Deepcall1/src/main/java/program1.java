import java.util.*;
class program1 
{
  public static boolean foo(boolean h, int cnt) {
    return deep1(h, cnt);
  }

  public static boolean deep1(boolean x, int cnt) {
    if (cnt < 0) return false;
    if (cnt >=1000) 
      return deep2(x, cnt+1);

    return deep1(x, cnt+1);
  }

  public static boolean deep2(boolean x, int cnt) {
    if (cnt < 1000) return false;
    if (cnt >=2000) 
      return deep3(x, cnt+1);

    return deep2(x, cnt+1);
  }

  public static boolean deep3(boolean x, int cnt) {
    if (cnt < 2000) return false;
    if (cnt >=3000)
      return deep4(x, cnt+1);

    return deep3(x, cnt+1);
  }

  public static boolean deep4(boolean x, int cnt) {
    if (cnt < 3000) return false;
    if (cnt >=4000)
      return deep5(x, cnt+1);

    return deep4(x, cnt+1);
  }

  public static boolean deep5(boolean x, int cnt) {
    if (cnt < 4000) return false;
    if (cnt >=5000)
      return x;

    return deep5(x, cnt+1);
  }

  public static void main (String [] args) 
  {
    Scanner inp = new Scanner(System.in);
    boolean x = false;
    try { 
        int num = inp.nextInt();
        System.out.print(num + " ");
        x = num % 2 == 0;
    } catch(NoSuchElementException e) {
        System.out.println("Error: NoSuchElementException");
    }
    
    System.out.println(deep4(x, 3500));
  }
}
