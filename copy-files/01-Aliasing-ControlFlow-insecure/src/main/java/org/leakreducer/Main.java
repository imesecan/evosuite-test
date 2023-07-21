package org.leakreducer;

public class Main {

    static class A {
        int val;

        A(int val) {
            this.val = val;
        }
    }

    public static int process(int secret, int val) {
        A a = new A(val);
        A b = a;

        if (secret == 42) {
            a.val = 2;
        }

        return b.val;
    }
}
