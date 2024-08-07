def create_spiral(n):
    try:#Had to google this one but i do understand the concept
        #take it as a learning moment
        row1 = 0
        result = [[0 for i in range(n)] for j in range(n)]
        num = 1
        col1 = 0
        max_row = max_col = n

        while n <= n**2:
            for i in range(col1, max_col): #adding numbers across the matrix colums: left to right
                result[col1][i] = num
                num += 1
            if num > n ** 2:
                break
            for i in range(row1 + 1, max_row): #adding numbers across matrix rows: down direction
                result[i][max_row - 1] = num
                num += 1
            if num > n ** 2:
                break
            for i in range(max_col - 2, col1 - 1, -1): #adding numbers across matrix colums: right to left
                result[max_col - 1][i] = num
                num += 1
                if num > n ** 2:
                    break
            for i in range(max_row - 2, row1, -1): #adding numbers across matrix rows: up direction
                if result[i][col1] == 0:
                    result[i][col1] = num
                    num += 1
                if num > n ** 2:
                    break

            row1 += 1
            max_row -= 1
            max_col -= 1
            col1 += 1
        return result if num > 0 else []
    except TypeError:
        return []