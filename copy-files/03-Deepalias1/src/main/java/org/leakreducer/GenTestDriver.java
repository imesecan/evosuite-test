package org.leakreducer;

import java.util.Scanner;

public class GenTestDriver
{
    public static void main(String[] args)
    {
        int invalid = -2147483648;
        Scanner in = new Scanner(System.in);
        int M = in.nextInt();  // number of lows
        
        for(int j=0; j<M; j++) {
            int sec = in.nextInt();
            if (sec == invalid)
                System.out.print(invalid+" ");
            else
                System.out.print(Program.drive(sec)+" ");
        }

        for(int j=0; j<M; j++) {
            int sec = in.nextInt();
            if (sec == invalid)
                System.out.print(invalid+" ");
            else
                System.out.print(Program.drive(sec)+" ");
        }

    }
}
