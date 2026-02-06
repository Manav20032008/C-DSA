/*
->  Tail recursive factorial

int factTail(int n, int a=1) {
    if (n == 0) return a;
    return factTail(n - 1, n * a);
}


->  Non-tail factorial

int fact(int n) {
    if (n == 0) return 1;
    return n * fact(n - 1);
}
    
*/