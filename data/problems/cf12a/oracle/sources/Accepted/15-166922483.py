li1 = list(input().split())[0]
li2 = list(input().split())[0]
li3 = list(input().split())[0]

if li1[0] == li3[2] and li1[1] == li3[1] and li1[2] == li3[0] and li2[0] == li2[2]:
    print("YES")
else:
    print("NO")
# for z in range(int(input())):
#     excel_input = list(input().split())
#     excel_input = excel_input[0]
#     if excel_input[0] == 'R' and excel_input[1].isdigit():
#         # R__C__
#         idx = 1
#         while excel_input[idx].isdigit():
#             idx += 1
#         row_num = idx
#         col_num = int(excel_input[idx+1:])
#         col_num = 731
#         # while col_num >= 26:
#         #     print(col_num//26)
#         #     print(col_num%26)
#         #     col_num = col_num - 26*col_num//26
#         print(col_num%26)
#         print(excel_input[1:row_num])
#     else:
#         # Alphabets Digits
#         idx = 0
#         column_num = 0
#         while excel_input[idx].isalpha():
#             column_num = ord(excel_input[idx])-64 + column_num
#             column_num *= 26
#             idx += 1
#         print('R' + excel_input[idx:] + 'C' + str(int(column_num/26)))