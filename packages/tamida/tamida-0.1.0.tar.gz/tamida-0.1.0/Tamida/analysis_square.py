import math
import scipy.special as sp
def is_factorial(x):
    """
    Kiểm tra xem 1 số có phải là giai thừa của 1 số hay là không?
    """
    if x == 1:
        return True
    fact = 1
    i = 1
    while fact < x:
        i += 1
        fact *= i
    return fact == x  
def is_square_number(a):
    """
    Kiểm tra xem số a có phải là số chính phương không.
    - a: Số cần kiểm tra.
    - Trả về True nếu a là số chính phương, ngược lại trả về False.
    """
    return a > 0 and a == int(math.sqrt(a)) ** 2

def small_square(x):
    """
    Tìm số nguyên dương nhỏ nhất i sao cho tổng của các bình phương từ 1 đến i lớn hơn x.
    """
    i = 1
    while (1/6 * (i + 1) * i * (2 * i + 1)) < x:
        i += 1
    return i

def is_prime(n):
    """
    Kiểm tra xem số n có phải là số nguyên tố không.
    
    Một số nguyên tố là một số tự nhiên lớn hơn 1 chỉ chia hết cho 1 và chính nó.
    Ví dụ: 2, 3, 5, 7, 11 là các số nguyên tố.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def square_combination(n, k, start=1, current_combination=[], results=[]):
    """
    Tìm tất cả các tổ hợp gồm k số khác nhau sao cho tổng bình phương của chúng bằng n.

    Tham số:
    - n: Số cần biểu diễn dưới dạng tổng bình phương.
    - k: Số phần tử trong tổ hợp.
    - start: Giá trị bắt đầu để đảm bảo các số trong tổ hợp không trùng nhau.
    - current_combination: Danh sách các số đang được chọn trong quá trình đệ quy.
    - results: Danh sách lưu trữ tất cả các tổ hợp hợp lệ.

    Trả về:
    - Danh sách các chuỗi biểu diễn các tổ hợp hợp lệ.
    """
    if k == 0:
        if sum(x**2 for x in current_combination) == n:
            results.append(f"{n} = " + " + ".join(f"{x}^2" for x in current_combination))
        return
    
    limit = int(math.sqrt(n)) + 1
    for i in range(start, limit):
        square_combination(n, k - 1, i + 1, current_combination + [i], results)
    
    return results  # Trả về danh sách kết quả
def pitago_reverse(x):
    """
    Kiểm tra xem x có thể biểu diễn dưới dạng hiệu của hai số bình phương không.

    Hàm tìm hai số nguyên dương a và b sao cho:
        x = a^2 - b^2
    Nếu tìm thấy, hàm trả về chuỗi biểu diễn phép toán.
    Nếu không tìm thấy, hàm trả về thông báo rằng x không phải là số Pitago đảo ngược.

    Tham số:
    - x: Số nguyên dương cần kiểm tra.

    Trả về:
    - Danh sách các chuỗi biểu diễn x dưới dạng hiệu hai số bình phương nếu tìm thấy.
    - Chuỗi thông báo nếu không tìm thấy tổ hợp nào.
    """
    results = []  # Danh sách lưu trữ các kết quả hợp lệ
    for i in range(1, int(math.sqrt(x)) + 1):
        if (x % i == 0) and (x // i > i) and ((i + x // i) % 2 == 0):
            a = (x // i + i) // 2
            b = (x // i - i) // 2
            results.append(f"{x} = {a}^2 - {b}^2")
    
    if results:
        return results  # Trả về danh sách kết quả
    else:
        return f"{x} not a Pitago's reverse number."  # Nếu không tìm thấy kết quả nào
def is_gauss_number(x):
    """
    Kiểm tra xem x có phải là một số Gauss không.

    Một số Gauss là số có thể biểu diễn dưới dạng tổng các số bình phương 
    của các số nguyên liên tiếp, và theo lý thuyết, x thỏa mãn điều kiện 
    8x + 1 phải là một số chính phương.

    Tham số:
    - x: Số nguyên cần kiểm tra.

    Trả về:
    - Chuỗi thông báo nếu x là số Gauss, với thông điệp "x is Gauss number.".
    - Chuỗi thông báo nếu x không phải số Gauss, với thông điệp "x is not Gauss number".
    """
    if is_square_number(8*x+1):
        return f" {x} is Gauss number."
    else:
        return f"{x} is not Gauss number."
def is_power_of(n):
    """
    kiểm tra xem 1 số có thể biểu diễn thành a^b không với a,b là số nguyên không âm
    """
    global power_a,power_b
    if n <= 1:
        return True  # Trường hợp đặc biệt: 1 = 1^b và 0 = 0^b

    for power_a in range(2, int(math.sqrt(n)) + 1):  # a từ 2 đến căn bậc hai của n
        power_b = round(math.log(n, power_a))  # b = log(n) / log(a)
        if power_a** power_b == n:  # Kiểm tra nếu a^b = n
            return True
    return False
def power_of(n):
    """
    Kiểm tra xem số n có thể được biểu diễn dưới dạng a^b với a và b là số nguyên không âm hay không.
    Nếu có, in ra giá trị của a và b, nếu không, in ra thông báo không thể biểu diễn.
    """
    if is_power_of(n):
        print(f"{n} = {power_a}^{power_b}")
    else:
        print(f"{n} cannot be expressed as a^b with a and b being non-negative integers.")
def conjecture_collatz(x, dem=0):
    """
    Hàm đệ quy thực hiện phép toán Collatz (hay còn gọi là Conjecture của Collatz).
    Đối với một số x, nếu x là chẵn, chia cho 2, nếu lẻ, nhân với 3 và cộng 1.
    Hàm này đếm số bước cần thiết để số x trở thành 1.

    :param x: Số cần thực hiện phép toán Collatz
    :param dem: Biến đếm số bước (mặc định là 0)
    :return: Số bước cần thiết để số x trở thành 1
    """
    if x == 1:
        return dem  
    
    return conjecture_collatz(x // 2 if x % 2 == 0 else 3 * x + 1, dem + 1)
def fibonacci(n):
    """
    Hàm đệ quy tính giá trị số Fibonacci tại chỉ số n.
    Dãy số Fibonacci được xác định bởi công thức:
        F(0) = 0, F(1) = 1
        F(n) = F(n-1) + F(n-2) với n >= 2

    Hàm này sử dụng phương pháp đệ quy để tính giá trị Fibonacci tại chỉ số n.
    
    :param n: Chỉ số trong dãy số Fibonacci (n phải là một số nguyên không âm)
    :return: Giá trị của số Fibonacci tại chỉ số n
    """
    if n <= 1:
        return n  
    return fibonacci(n - 1) + fibonacci(n - 2) 
def subfactorial(n):
    """
    Hàm đệ quy tính subfactorial (!n) của một số tự nhiên n.
    
    Subfactorial là số cách sắp xếp các phần tử sao cho không phần tử nào ở đúng vị trí ban đầu.
    
    Công thức:
        !0 = 1
        !1 = 0
        !n = (n - 1) * (!n-1 + !n-2) với n >= 2
    
    :param n: Số tự nhiên n
    :return: Giá trị của subfactorial (!n)
    """
    if n == 0:
        return 1
    elif n == 1:
        return 0
    else:
        return (n - 1) * (subfactorial(n - 1) + subfactorial(n - 2))
def factorial(n):
    """
    Hàm đệ quy tính giai thừa (n!) của một số tự nhiên n.
    
    Giai thừa của n được tính bằng công thức:
        n! = n * (n-1)! với n >= 1
        0! = 1
    
    :param n: Số tự nhiên n
    :return: Giá trị của giai thừa n!
    """
    if n == 0:
        return 1 
    else:
        return n * factorial(n - 1) 
def catalan(n):
    """
    Hàm tính số Catalan thứ n.

    Số Catalan là một chuỗi số trong lý thuyết tổ hợp, với nhiều ứng dụng trong việc đếm các cấu trúc tổ hợp như cây nhị phân, phân vùng, v.v.
    Công thức tính số Catalan thứ n:
    C_n = (2n)! / ((n+1)! * n!)

    :param n: Số nguyên không âm cần tính số Catalan thứ n.
    :return: Giá trị số Catalan thứ n, được tính theo công thức trên.
    """
    return factorial(2 * n) // (factorial(n + 1) * factorial(n))
def is_armstrong(n):
    """
    Hàm kiểm tra xem số n có phải là số Armstrong hay không.

    Số Armstrong là một số mà tổng các chữ số của nó, mỗi chữ số được nâng lên lũy thừa với số lượng chữ số của số đó, bằng chính số đó.
    Ví dụ:
    - 153 là số Armstrong vì: 1^3 + 5^3 + 3^3 = 153
    - 370 là số Armstrong vì: 3^3 + 7^3 + 0^3 = 370

    :param n: Số nguyên không âm cần kiểm tra.
    :return: True nếu số n là số Armstrong, False nếu không.
    """
    num_digits = len(str(n))
    return n == sum(int(digit) ** num_digits for digit in str(n))
def decimal_to_binary(n):
    """
    Hàm chuyển đổi số thập phân n thành số nhị phân.
    
    :param n: Số thập phân cần chuyển đổi
    :return: Chuỗi nhị phân tương ứng với số thập phân
    """
    if n == 0:
        return "0"
    elif n == 1:
        return "1"
    else:
        return decimal_to_binary(n // 2) + str(n % 2)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
def lcm(a, b):
    return abs(a * b) // gcd(a, b)
def harmonic_number(n):
    """
    Hàm tính số Harmonic thứ n.

    Số Harmonic thứ n được tính theo công thức:
    H_n = 1 + 1/2 + 1/3 + ... + 1/n

    :param n: Số nguyên không âm, đại diện cho số thứ hạng trong chuỗi số Harmonic.
    :return: Giá trị số Harmonic thứ n.
    """
    return sum(1/i for i in range(1, n+1))
def pochhammer(x, n):
    """
    Hàm tính giá trị của biểu thức Pochhammer (x)_n.

    Biểu thức Pochhammer (x)_n được định nghĩa là:
    (x)_n = x * (x+1) * (x+2) * ... * (x+n-1)

    :param x: Số thực hoặc số phức bất kỳ.
    :param n: Số nguyên không âm (n ≥ 0) đại diện cho độ dài chuỗi.
    :return: Giá trị của biểu thức Pochhammer (x)_n.
    """
    result = 1
    for i in range(n):
        result *= (x + i)
    return result
def bell_number(n):
    """
    Hàm tính số Bell thứ n, tức là số cách phân chia một tập hợp gồm n phần tử thành các tập con không rỗng.

    :param n: Số nguyên không âm đại diện cho số phần tử của tập hợp.
    :return: Số Bell thứ n, là số cách phân chia tập hợp thành các phần tử con.
    """
    bell = [[0 for i in range(n+1)] for j in range(n+1)]
    
    bell[0][0] = 1  # Số Bell của tập hợp rỗng
    
    # Tính bảng Bell
    for i in range(1, n+1):
        # Đặt bell[i][0] = bell[i-1][n-1]
        bell[i][0] = bell[i-1][i-1]
        
        # Tính các giá trị còn lại
        for j in range(1, i+1):
            bell[i][j] = bell[i-1][j-1] + bell[i][j-1]
    
    return bell[n][0]

def bernoulli_number(n):
    """
    Hàm tính số Bernoulli thứ n. Số Bernoulli được sử dụng trong lý thuyết tổ hợp và chuỗi Taylor.
    
    :param n: Số nguyên không âm đại diện cho chỉ số trong chuỗi số Bernoulli.
    :return: Giá trị của số Bernoulli thứ n.
    """
    # Tạo một mảng để lưu trữ các số Bernoulli
    B = [0] * (n+1)
    
    # Số Bernoulli B_0 = 1
    B[0] = 1
    
    # Sử dụng phương pháp đệ quy để tính các số Bernoulli
    for m in range(1, n+1):
        B[m] = 0
        for k in range(m):
            B[m] -= binomial(m, k) * B[k] / (m - k + 1)
    
    return B[n]

def binomial(n, k):
    """
    Hàm tính hệ số nhị thức C(n, k) = n! / (k! * (n-k)!)
    
    :param n: Số nguyên không âm n.
    :param k: Số nguyên không âm k.
    :return: Hệ số nhị thức C(n, k).
    """
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    num = 1
    denom = 1
    for i in range(k):
        num *= (n - i)
        denom *= (i + 1)
    return num // denom
def carmichael_lambda(n):
    """
    Hàm tính giá trị của hàm Carmichael λ(n), hay còn gọi là hàm chu kỳ.
    
    :param n: Số nguyên không âm n
    :return: Giá trị của hàm Carmichael λ(n)
    """
    if n == 1:
        return 1
    
    # Nếu n là số nguyên tố
    if is_prime(n):
        return n - 1
    
    # Phân tích thừa số n thành các số nguyên tố
    factors = prime_factors(n)
    
    # Nếu n là một số nguyên tố mạnh
    if len(factors) == 1:
        p = factors[0]
        if p == 2 and n == 2:
            return 1
        return p - 1

    # Tính λ(n) từ các thừa số của n
    lcm_result = 1
    for factor in factors:
        lcm_result = lcm(lcm_result, factor)

    return lcm_result
def prime_factors(n):
    """
    Hàm phân tích thừa số nguyên tố của n.
    
    :param n: Số nguyên dương n
    :return: danh sách các thừa số nguyên tố của n
    """
    factors = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors
def divisors(n):
    """
    Hàm trả về tất cả các ước số của n.
    
    :param n: Số nguyên dương n
    :return: Danh sách các ước số của n
    """
    divs = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:  # Đảm bảo không thêm trùng lặp nếu i == n // i
                divs.append(n // i)
    return divs

def divisor_sigma(n):
    """
    Hàm tính tổng các ước số của n, bao gồm cả n và 1.
    
    :param n: Số nguyên dương n
    :return: Tổng các ước số của n
    """
    return sum(divisors(n))
def euler_totient(n):
    """
    Hàm tính giá trị của Euler's Totient Function (phi(n)).
    
    :param n: Số nguyên n
    :return: Giá trị của Euler's Totient Function (phi(n))
    """
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result
def eulerian_polynomial(n, x):
    """
    Hàm tính Eulerian Polynomial A_n(x) cho một giá trị n và x.
    
    :param n: Số nguyên n
    :param x: Giá trị của biến x trong đa thức Eulerian
    :return: Giá trị của đa thức Eulerian A_n(x)
    """
    A = [[0] * (n + 1) for _ in range(n + 1)]
    A[0][0] = 1
    for i in range(1, n + 1):
        for j in range(i + 1):
            if j == 0:
                A[i][j] = (i + 1) * A[i - 1][j]
            else:
                A[i][j] = (i - j) * A[i - 1][j - 1] + (j + 1) * A[i - 1][j]
    result = 0
    for k in range(n + 1):
        result += A[n][k] * (x ** k)
    return result
def lucas(n):
    """
    Hàm tính số Lucas thứ n.
    
    :param n: Chỉ số n của số Lucas cần tính
    :return: Số Lucas thứ n
    """
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return lucas(n - 1) + lucas(n - 2)
def partition(n):
    """
    Hàm tính số phân tách của một số nguyên dương n.
    
    :param n: Số nguyên cần phân tách
    :return: Số phân tách của n
    """
    # Bảng để lưu trữ số partition của các số
    dp = [0] * (n + 1)
    dp[0] = 1  # Số phân tách của 0 là 1 (một cách duy nhất: không có số nào)
    
    # Tính số partition của các số từ 1 đến n
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
    
    return dp[n]
def realsign(x):
    """
    Hàm tính dấu của số thực x.
    
    :param x: Một số thực
    :return: 1 nếu x > 0, 0 nếu x == 0, -1 nếu x < 0
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
def stirling1(n, k):
    """
    Hàm tính số Stirling của loại đầu tiên S(n, k) - số cách phân tách n phần tử thành k chuỗi vòng.
    
    :param n: Số phần tử cần phân tách
    :param k: Số chuỗi vòng
    :return: S(n, k) - Số Stirling của loại đầu tiên
    """
    # Tạo bảng DP để lưu trữ kết quả tính toán
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    # Điều kiện ban đầu
    dp[0][0] = 1  # S(0, 0) = 1
    
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            dp[i][j] = dp[i - 1][j - 1] + (i - 1) * dp[i - 1][j]
    
    return dp[n][k]
def erf_function(x):
    """
    Hàm tính giá trị của hàm error function erf(x) sử dụng thư viện scipy.
    
    :param x: Một số thực đầu vào
    :return: Giá trị của hàm erf(x)
    """
    return sp.erf(x)
def erfc_function(x):
    """
    Tính giá trị của hàm erfc(x).
    
    :param x: Một số thực đầu vào
    :return: Giá trị của hàm erfc(x)
    """
    return sp.erfc(x)

def erfi_function(x):
    """
    Tính giá trị của hàm erfi(x).
    
    :param x: Một số thực đầu vào
    :return: Giá trị của hàm erfi(x)
    """
    return sp.erfi(x)
def number_root(x, n):
    """
    Tính tổng lũy thừa bậc n của từng chữ số trong số nguyên dương x.
    """
    if x == 0:  
        return 0
    return (x % 10) ** n + number_root(x // 10, n)