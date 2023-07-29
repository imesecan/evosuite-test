package org.leakreducer;

import java.util.Scanner;

public class Driver
{
    public static void main(String[] args) 
    {
        Scanner in = new Scanner(System.in);
        int N = in.nextInt();
        for(int i=0; i<N; i++)
        {
            int secret = in.nextInt();
            System.out.print(Program.drive(secret)+" ");
        }
    }
}
