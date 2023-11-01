def is_compatible(donor, recipient):
    # Extract antigen and rhesus of both the donor and recipient
    donor_antigen = donor[:-1] # everything until the last index (the rhesus)
    recipient_antigen = recipient[:-1]
    donor_rhesus = donor[-1] # only the last index (the rhesus)
    recipient_rhesus = recipient[-1]

    # (1) Antigen verification
    # if the recipient antigen is AB or the donor antigen is O, they are antigen compatible
    if recipient_antigen == "AB" or donor_antigen == "O":
        compatible_antigen = True
    # else if the recipient and donor antigen are the same, they are antigen compatible
    elif recipient_antigen == donor_antigen:
        compatible_antigen = True
    # otherwise they are antigen incompatible
    else:
        compatible_antigen = False

    # (2) Rhesus verification
    # if the donor rhesus is + and the antigen rhesus is - , they are rhesus incompatible
    if donor_rhesus == "+" and recipient_rhesus == "-":
        compatible_rhesus = False
    # otherwise they are rhesus compatible
    else:
        compatible_rhesus = True

    # (3) Blood compatibility
    # only if both antigen and rhesus are compatible, then they are blood compatible
    if compatible_antigen and compatible_rhesus:
        return True
    else:
        return False

def fibonacci_seq(num):
    if num == 1:
        return 1
    elif num == 0:
        return 0
    return fibonacci_seq(num-1) + fibonacci_seq(num-2)


def isPalindrome(s):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for i in s:
        if i not in alphabet:
            s = s.replace(i, "")
    return s == s[::-1]


def firstUniqChar(s):
    map_dict = {}
    for i in range(len(s)):
        map_dict[s[i]] = map_dict.get(s[i], 0) + 1

    if 1 not in map_dict.values():
        return -1
    return list(map_dict.values()).index(1)


def subarraySum(nums, k):
    num = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            print(nums[i:j+1])
            print((i,j))
            if sum(nums[i:j+1]) == k:
                num += 1
    return num

print(subarraySum([1,1,1], 2))

