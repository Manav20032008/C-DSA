'''
204. Count Primes
Given an integer n, return the number of prime numbers that are strictly less than n.

Example 1:

Input: n = 10
Output: 4
Explanation: There are 4 prime numbers less than 10, they are 2, 3, 5, 7.

Constraints:
0 <= n <= 5 * 10^6

# ? Sieve of Eratosthenes method
# ! Can Be Solved by DP

Complexity
Time complexity: O(N log log N)

Space complexity: O(N)
'''


class Solution(object):
    def countPrimes(self, n):
        if n < 2 :
            return 0 

        prime = [True] *n
        prime[0] = prime[1] = False

        for i in range(2,int(n**0.5)+1):
            if prime[i]:
                for j in range(i*i,n,i):
                    prime[j]=False

        return sum(prime)      

