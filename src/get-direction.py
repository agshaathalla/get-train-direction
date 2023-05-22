import csv
import os

def getPath():
    map = """x,x,x,x,x,x,x,x,x,x,x,x,x
x,1Tanah Tinggi ,1Tangerang,x,x,5Pasar Senen,5Gang Sentiong,5Kramat,5Pondok Jati,5L,5L,5L,x
x,1Batu Ceper,x,x,x,5Kemayoran,x,x,x,x,x,5L,x
x,1Poris,x,x,x,5Rajawali,x,3Mangga Besar,3Sawah Besar,3Juanda,x,5L,x
x,1Kali Deres,x,4Tanjung Priok,4Ancol,6Kampung Bandan,6Jakarta Kota,3Jayakarta,x,3Gondangdia,x,5L,x
x,1Rawa Buaya,x,x,x,5Angke,x,x,x,3Cikini,x,5L,x
x,1Bojong Indah,1Taman Kota,1Pesing,1Grogol,6Duri,6Tanah Abang,5Karet,5Sudirman,6Manggarai,5Matraman,5Jatinegara,x
x,x,x,x,x,x,2Palmerah,x,x,3Tebet,x,5Klender,x
x,x,x,x,2Jurang Mangu,2Pondok Ranji,2Kebayoran,x,x,3Cawang,x,5Buaran,x
x,x,x,x,2Sudimara,x,x,x,x,3Duren Kalibata,x,5Klender Baru,x
x,x,x,x,2Rawa Buntu,2Serpong,x,x,x,3Pasar Minggu Baru,x,5Cakung,x
x,x,x,x,x,2Cisauk,x,x,x,3Pasar Minggu,x,5Kranji,x
x,2Tenjo,2Daru,2Cilejit,2Parung Panjang,2Cicayur,x,x,x,3Tanjung Barat,x,5Bekasi,x
x,2Tigaraksa,x,x,x,x,x,x,x,3Lenteng Agung,x,5Bekasi Timur,x
x,2Cikoya,x,x,x,x,3Nambo,x,x,3Univ. Pancasila,x,5Tambun,x
x,2Maja,x,x,4Bogor,x,3Cibinong,x,x,3Univ. Indonesia,x,5Cibitung,x
x,2Citeras,x,x,3Cilebut,3Bojong Gede,3Citayam,3Depok,3Depok Baru,3Pondok Cina,x,5Metland Telaga Murni,x
x,2Rangkasbitung,x,x,x,x,x,x,x,x,x,5Cikarang,x
x,x,x,x,x,x,x,x,x,x,x,x,x"""

    lines = map.splitlines()
    reader = csv.reader(lines, delimiter=',')
    matrix = [[[0 for z in range(3)] for y in range(13)] for x in range(19)]
    j = 0
    for row in reader:
        for i in range(len(row)):
            if(row[i] == "x"):
                matrix[j][i][1] = False
            else:
                matrix[j][i][1] = True

            if (row[i][0] == "1"):
                matrix[j][i][2] = "Tangerang"
                kata = row[i].split("1")[1]
            elif (row[i][0] == "2"):
                matrix[j][i][2] = "Rangkasbitung"
                kata = row[i].split("2")[1]
            elif (row[i][0] == "3"):
                matrix[j][i][2] = "Bogor"
                kata = row[i].split("3")[1]
            elif (row[i][0] == "4"):
                matrix[j][i][2] = "Tanjung Priok"
                kata = row[i].split("4")[1]
            elif (row[i][0] == "5"):
                matrix[j][i][2] = "Bekasi"
                kata = row[i].split("5")[1]
            elif (row[i][0] == "6"):
                matrix[j][i][2] = "Transit"
                kata = row[i].split("6")[1]
            else:
                kata = row[i]
            matrix[j][i][0] = kata
        j += 1
    return matrix

def getStationIndex(matrix, station):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if(matrix[i][j][0] == station):
                return i,j
            
def getJalur(matrix, start, end):
    stack = [[start]]
    if(start == end):
        return stack[0]
    while(True):
        saatIni = stack[0]
        i,j = getStationIndex(matrix, saatIni[0])
        #up
        if(matrix[i-1][j][1] == True):
            diAppend1 = [matrix[i-1][j][0]] + saatIni
            stack= stack + [diAppend1]
            matrix[i-1][j][1] = False
            if(matrix[i-1][j][0] == end):
                break
        #down
        if(matrix[i+1][j][1] == True):
            diAppend2 = [matrix[i+1][j][0]] + saatIni
            stack = stack + [diAppend2]
            matrix[i+1][j][1] = False
            if(matrix[i+1][j][0] == end):
                break
        #left
        if(matrix[i][j-1][1] == True):
            diAppend3 = [matrix[i][j-1][0]] + saatIni
            stack = stack + [diAppend3]
            matrix[i][j-1][1] = False
            if(matrix[i][j-1][0] == end):
                break
        #right
        if(matrix[i][j+1][1] == True):
            diAppend4 = [matrix[i][j+1][0]] + saatIni
            stack = stack + [diAppend4]
            matrix[i][j+1][1] = False
            if(matrix[i][j+1][0] == end):
                break

        stack.remove(saatIni)
    hasil = stack.pop()
    pattern = []
    for i in range(len(hasil)):
        temp = hasil.pop()
        if temp != "L":
            pattern.append(temp)
    a = 0
    if len(pattern) > 2:
        while a<len(pattern)-1:
            q,r = getStationIndex(matrix, pattern[a])
            if(matrix[q][r][2] == "Transit" and a>0):
                m,n = getStationIndex(matrix, pattern[a-1])
                jalurSebelum = matrix[m][n][2]
                o,p = getStationIndex(matrix, pattern[a+1])
                jalurSesudah = matrix[o][p][2]
                if jalurSesudah == "Transit":
                    o,p = getStationIndex(matrix, pattern[a+2])
                    jalurSesudah = matrix[o][p][2]
                    a+=1
                if jalurSebelum != jalurSesudah:
                    kata = "Pindah ke jalur " + jalurSesudah
                    pattern.insert(a+1, kata)
                    a += 1
            a += 1
    return pattern

def main():
    os.system("cls")
    print("Masukkan Stasiun asal dan stasiun tujuan anda")
    start = input("Stasiun asal : ")
    end = input("Stasiun tujuan : ")
    
    print(f"Jalur yang harus anda lalui dari Stasiun {start} menuju Stasiun {end} adalah : ")

    path = getJalur(getPath(), start, end)

    for i in range(len(path)-1):
        print(path[i], end=" -> ")
    print(path[-1], end=".")
    print("")

main()
