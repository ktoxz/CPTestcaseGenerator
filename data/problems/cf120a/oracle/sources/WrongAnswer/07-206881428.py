def solve(rail, orientation):
    with open('output.txt', 'a+') as writer:
        if (orientation.lower() == 'front' and rail == '1') or (orientation.lower() == 'back' and rail == '2'):
            writer.write('L\n')
        else:
            writer.write('R\n')
    writer.close()

if __name__ == '__main__':
    with open('input.txt', 'r') as reader:
        arr = reader.readlines()
        for i in range(0, len(arr), 2):
            orientation = arr[i]
            if orientation == '':
                break
            rail = arr[i + 1]
            
            solve(rail, orientation)
    
    reader.close()