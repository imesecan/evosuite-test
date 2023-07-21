package org.leakreducer;

import java.util.Scanner;

public class Driver
{
    static Scanner in = new Scanner(System.in);
    public static void main(String[] args) 
    {
        int N = in.nextInt();
        for(int i=0; i<N; i++)
        {
            int secret = in.nextInt();
            int low = in.nextInt();

            System.out.print(Main.process(secret, low)+ " ");
        }
    }
}
