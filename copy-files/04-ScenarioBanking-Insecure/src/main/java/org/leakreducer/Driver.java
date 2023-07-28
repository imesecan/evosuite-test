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

            Account account = new Account();
            AccountOwner owner = new AccountOwner(account);
            Beneficiary beneficiary = new Beneficiary();

            int deposit = in.nextInt();     // secret 1
            int withdraw = in.nextInt();    // secret 2

            account.deposit(deposit);
            owner.payBeneficiary(beneficiary, withdraw);
        }
    }
}
