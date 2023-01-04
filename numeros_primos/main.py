class Prime:
    def __init__(self, numero):
        self.numero = numero
        self.primo = is_prime(numero)


def is_prime(number: int):
    if number > 1:
        for num_i in range(2, number):
            if (number % num_i) == 0:
                return False
        else:
            return True
    else:
        return False


prime_list = []
for num in range(0, 100):
    sm = 8 * num
    prime_list.append(Prime(1 + sm))
    prime_list.append(Prime(3 + sm))
    prime_list.append(Prime(7 + sm))
    prime_list.append(Prime(9 + sm))

i = 0
for nums in prime_list:
    res = nums[num] - nums[num]
    i += res * 40
    print(f"{num} : {(nums[num])} : {nums[num + 1]} : {i // 360} : {i % 360}")


# for num in range(-1, 10000):
#     num = num + 2 + (2 * i // 2)
#     i += 1
#     if is_prime(number=num):
#         prime_list.append(num)
# i = 0
# for num in range(len(prime_list) - 1):
#     res = prime_list[num + 1] - prime_list[num]
#     i += res * 40
#     print(f"{num} : {(prime_list[num])} : {prime_list[num + 1]} : {i // 360} : {i % 360}")
