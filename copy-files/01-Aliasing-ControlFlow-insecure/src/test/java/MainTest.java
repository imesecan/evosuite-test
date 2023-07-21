import static org.junit.jupiter.api.Assertions.*;
public class MainTest {
   @org.junit.jupiter.api.Test
    void test1(){
        int res = Main.process(3, 4);
        assertEquals(4, res);
    }
   @org.junit.jupiter.api.Test
    void test2(){
        int res = Main.process(42, 4);
        assertEquals(2, res);
    }
   @org.junit.jupiter.api.Test
    void test3(){
        int res = Main.process(5, 3);
        assertEquals(3, res);
    }
   @org.junit.jupiter.api.Test
    void test4(){
        int res = Main.process(42, -17);
        assertEquals(2, res);
    }
}