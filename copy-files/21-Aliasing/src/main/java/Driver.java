import java.util.Scanner;
public class Driver
{
    static Scanner in = new Scanner(System.in);
    public static void main(String[] args) 
    {
        int N = in.nextInt();
        for(int i=0; i<N; i++)
        {
            int sec = in.nextInt();
            int val = in.nextInt();
            System.out.println( Main.process(sec, val));
        }
    }
}
