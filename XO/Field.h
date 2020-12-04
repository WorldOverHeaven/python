#ifndef XO3_FIELD_H
#define XO3_FIELD_H

#include <utility>
#include <string>
#include <vector>
#include <iostream>
using namespace std;

vector<vector<int>> createAttackWeights() {
    vector<vector<int>> attackWeights;
    attackWeights.reserve(6);
    for (int i = 0; i < 6; ++i) {
        attackWeights[i].reserve(4);
        for (int j = 0; j < 4; ++j) {
            attackWeights[i][j] = 0;
        }
    }

    for (int k = 0; k < 5; ++k) {
        attackWeights[k][0] = 0;
    }

    attackWeights[1][1] = 20;
    attackWeights[2][1] = 400;
    attackWeights[3][1] = 800;
    attackWeights[4][1] = 1200;
    attackWeights[5][1] = 40000;

    attackWeights[1][2] = 50;
    attackWeights[2][2] = 1000;
    attackWeights[3][2] = 1400;
    attackWeights[4][2] = 20000;
    attackWeights[5][2] = 40000;

    attackWeights[5][0] = 40000;

    return attackWeights;
}

vector<vector<int>> res(int size) {
    vector<vector<int>> field;
    field.reserve(size);
    for (int i = 0; i < size; ++i) {
        field[i].reserve(size);
        for (int j = 0; j < size; ++j) {
            field[i][j] = 0;
        }
    }
    return field;
}

enum status {
    win0,
    winX,
    draw,
    endGame
};

class Field {
private:
    int size;
    int step;
    int len;
    vector<vector<int>> attackWeights = createAttackWeights();
    status st;
    vector<vector<int>> field;
public:
    Field() {
        size = 19;
        step = 0;
        len = 5;
        st = draw;
        field = res(size);
    }

    Field(int s, int l) {
        size = s;
        len = l;
        step = 0;
        st = draw;
        field = res(size);
    }

    Field(vector<vector<int>>& a, int b) {
        size = 19;
        len = 5;
        step = b;
        st = draw;
        field = res(19);
        for (int k, i = 0; i < 19; ++i) {
            for (int j = 0; j < 19; ++j) {
                k = a[i][j];
                field[i][j] = k;
            }
        }
    }

    explicit Field(string a) {
        size = 19;
        len = 5;
        st = draw;
        field.reserve(size);
        for (int ii = 0; ii < 19; ++ii) {
            field[ii].reserve(19);
            for (int jj = 0; jj < 19; ++jj) {
                field[ii][jj] = 0;
            }
        }
        int kk = 0;
        for (int k = 0; k < 361; ++k) {
            if (a[k] == '0') {
                field[k / 19][k % 19] = -1;
                ++kk;
            }
            if (a[k] == 'X') {
                field[k / 19][k % 19] = 1;
                ++kk;
            }
            if (a[k] == ' ') {
                field[k / 19][k % 19] = 0;
            }
        }
        step = kk;
    }

    ~Field() = default;

    vector<vector<int>> getField() {
        vector<vector<int>> a(size);
        for (int i = 0; i < size; ++i) {
            a[i].reserve(size);
            for (int j = 0; j < size; ++j) {
                a[i][j] = field[i][j];
            }
        }
        return a;
    }

    int get(int i, int j) {
        return (field[(i + size) % size][(j + size) % size]);
    }

    status predict(int i, int j) {
        if (step == size * size) {
            return endGame;
        }
        int c = get(i, j);
        int sum = c;
        for (int k = 1; k < len; ++k) {
            sum += get(i - k, j - k);
        }
        for (int k = 1; k < len; ++k) {
            if (sum == len) {
                return winX;
            }
            if (sum == -len) {
                return win0;
            }
            sum -= get(i - len + k, j - len + k);
            sum += get(i + k, j + k);
        }

        sum = c;
        for (int k = 1; k < len; ++k) {
            sum += get(i - k, j + k);
        }
        for (int k = 1; k < len; ++k) {
            if (sum == len) {
                return winX;
            }
            if (sum == -len) {
                return win0;
            }
            sum -= get(i - len + k, j + len - k);
            sum += get(i + k, j - k);
        }

        sum = c;
        for (int k = 1; k < len; ++k) {
            sum += get(i, j + k);
        }
        for (int k = 1; k < len; ++k) {
            if (sum == len) {
                return winX;
            }
            if (sum == -len) {
                return win0;
            }
            sum -= get(i , j + len - k);
            sum += get(i, j - k);
        }

        sum = c;
        for (int k = 1; k < len; ++k) {
            sum += get(i - k, j);
        }
        for (int k = 1; k < len; ++k) {
            if (sum == len) {
                return winX;
            }
            if (sum == -len) {
                return win0;
            }
            sum -= get(i - len + k, j);
            sum += get(i + k, j);
        }
        return draw;
    }

    status predict2(int i, int j) {
        if (step == size * size) {
            return endGame;
        }
        auto lines = makeLines(i, j);
        vector<int> count(8);
        for (int k = 0; k < 8; ++k) {
            count[k] = 0;
        }
        for (int k = 0; k < len * 2 + 1; ++ k) {
            for (int kk = 0; kk < 4; ++kk) {
                if (lines[kk][k] == -1) {
                    ++count[kk * 2];
                } else {
                    count[kk * 2] = 0;
                }
                if (lines[kk][k] == 1) {
                    ++count[kk * 2 + 1];
                } else {
                    count[kk * 2 + 1] = 0;
                }

                if (count[kk * 2] == len) {
                    return win0;
                }
                if (count[kk * 2 + 1] == len) {
                    return winX;
                }
            }
        }
        return draw;
    }

    void savePut(int i, int j) {
        field[i][j] = (step % 2 == 0 ? 1 : -1);
        ++step;
    }

    status put(int i, int j) {
        i = (i + size) % size;
        j = (j + size) % size;
        field[i][j] = (step % 2 == 0 ? 1 : -1);
        ++step;
        return predict2(i, j);
    }

    void print() {
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                if(field[i][j] == -1) {
                    cout << "0 ";
                }
                if(field[i][j] == 1) {
                    cout << "X ";
                }
                if(field[i][j] == 0) {
                    cout << ". ";
                }
            }
            cout << "\n";
        }
        cout << "\n";
    }

    pair<int, int> nextMove1() {
        if (step == 0) {
            pair<int, int> a;
            a.first = size / 2;
            a.second = size / 2;
            return a;
        }
        int max = 0;
        pair<int, int> a;
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                if (field[i][j] == 0) {
                    int sum = 0;
                    sum += abs(get(i - 1, j - 1));
                    sum += abs(get(i - 1, j));
                    sum += abs(get(i - 1, j + 1));
                    sum += abs(get(i, j + 1));
                    sum += abs(get(i, j - 1));
                    sum += abs(get(i + 1, j - 1));
                    sum += abs(get(i + 1, j));
                    sum += abs(get(i + 1, j + 1));
                    if (sum >= max) {
                        max = sum;
                        a.first = i;
                        a.second = j;
                    }
                }
            }
        }
        return a;
    }

    /*

    makeLine возвращает 4 линии
    */


    vector<vector<int>> makeLines(int i, int j) {
        vector<vector<int>> line(4);
        for (int k = 0; k < 4; ++k) {
            line[k].reserve(len * 2 + 1);
        }

        for (int k = -len; k <= len; ++k) {
            line[0][k + len] = get(i + k, j + k);
            line[1][k + len] = get(i + k, j - k);
            line[2][k + len] = get(i + k, j);
            line[3][k + len] = get(i, j + k);
        }

        return line;
    }

    int count(vector<int>& line) {
        int power = 1;
        int potential = 2;
        int ln = 1;
        bool flag = true;

        int f = step % 2 == 0 ? 1 : -1;

        for (int k = 1; k <= len; ++k) {
            if (line[len + k] == f) {
                ++ln;
                if (flag) {
                    ++power;
                }
            }
            if (line[len + k] == -f) {
                if (flag) {
                    --potential;
                }
                break;
            }
            if (line[len + k] == 0) {
                ++ln;
                flag = false;
            }
        }

        flag = true;

        for (int k = 1; k <= len; ++k) {
            if (line[len - k] == f) {
                ++ln;
                if (flag) {
                    ++power;
                }
            }
            if (line[len - k] == -f) {
                if (flag) {
                    --potential;
                }
                break;
            }
            if (line[len - k] == 0) {
                ++ln;
                flag = false;
            }
        }

        int sum = 0;

        if (ln >= len) {
            if (power >= 5) {
                return 400000;
            }
            sum += attackWeights[power][potential];
        }

        power = 1;
        potential = 2;
        ln = 1;
        flag = true;

        f = -f;

        for (int k = 1; k <= len; ++k) {
            if (line[len + k] == f) {
                ++ln;
                if (flag) {
                    ++power;
                }
            }
            if (line[len + k] == -f) {
                if (flag) {
                    --potential;
                }
                break;
            }
            if (line[len + k] == 0) {
                ++ln;
                flag = false;
            }
        }

        flag = true;

        for (int k = 1; k <= len; ++k) {
            if (line[len - k] == f) {
                ++ln;
                if (flag) {
                    ++power;
                }
            }
            if (line[len - k] == -f) {
                if (flag) {
                    --potential;
                }
                break;
            }
            if (line[len - k] == 0) {
                ++ln;
                flag = false;
            }
        }

        if (ln >= len) {
            if (power > 5) {
                power = 5;
            }
            sum += attackWeights[power][potential] * 21 / 20;
        }

        return sum;
    }

    pair<int, int> nextMove2() {
        if (step == 0) {
            pair<int, int> a;
            a.first = size / 2;
            a.second = size / 2;
            return a;
        }
        int max = 0;
        pair<int, int> a;
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                if (field[i][j] == 0) {
                    int sum = 0;
                    vector<vector<int>> lines = makeLines(i, j);
                    for (int k = 0; k < 4; ++k) {
                        sum += count(lines[k]);
                    }
                    if (sum >= max) {
                        max = sum;
                        a.first = i;
                        a.second = j;
                    }
                }
            }
        }
        return a;
    }
};

#endif //XO3_FIELD_H
