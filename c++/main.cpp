#include <iostream>
#include <vector>
using namespace std;

class Grid {
protected:
    static const int GRID_SIZE = 9;
    static const int BOX_SIZE = 3;
    vector<vector<int>> grid;

public:
    Grid() {
        // 初始化一个9x9的方格为0
        grid = vector<vector<int>>(GRID_SIZE, vector<int>(GRID_SIZE, 0));
    }

    // 得到方格的特定行
    vector<int> getRow(int row) {
        return grid[row];
    }

    // 得到方格的特定列
    vector<int> getColumn(int col) {
        vector<int> column;
        for (int i = 0; i < GRID_SIZE; ++i) {
            column.push_back(grid[i][col]);
        }
        return column;
    }

    // 得到一个3x3的子方格
    vector<int> getBox(int row, int col) {
        vector<int> box;
        int boxRowStart = (row / BOX_SIZE) * BOX_SIZE;
        int boxColStart = (col / BOX_SIZE) * BOX_SIZE;
        
        for (int i = 0; i < BOX_SIZE; ++i) {
            for (int j = 0; j < BOX_SIZE; ++j) {
                box.push_back(grid[boxRowStart + i][boxColStart + j]);
            }
        }
        return box;
    }

    // 对方格的对应索引位置赋值
    void setValue(int row, int col, int value) {
        grid[row][col] = value;
    }

    // 输出方格
    void displayGrid() {
        for (int i = 0; i < GRID_SIZE; ++i) {
            for (int j = 0; j < GRID_SIZE; ++j) {
                cout << grid[i][j] << " ";
            }
            cout << endl;
        }
    }
};
class Sudoku : public Grid {
public:
    Sudoku(string input) {
        parse(input);
    }

    // 解析字符串输入，反串行化
    void parse(string input) {
        int index = 0;
        for (int i = 0; i < GRID_SIZE; ++i) {
            for (int j = 0; j < GRID_SIZE; ++j) {
                grid[i][j] = input[index++] - '0'; 
            }
        }
    }

    // 推理函数
    vector<int> getInference(int row, int col) {
        vector<int> possibleValues;

        if (grid[row][col] != 0) return possibleValues; //如果该位置已赋值，直接return

        bool used[10] = {false}; // 记录已在行、列和框中使用的数字

        // 标记已在行、列和框中使用的数字
        for (int num : getRow(row)) used[num] = true;
        for (int num : getColumn(col)) used[num] = true;
        for (int num : getBox(row, col)) used[num] = true;

        // 枚举所有未在行、列和框中使用的数字
        for (int i = 1; i <= 9; ++i) {
            if (!used[i]) possibleValues.push_back(i);
        }

        return possibleValues;
    }

    // 显示给定位置的可能值
    void displayInference(int row, int col) {
        if(col==0){
            cout<<"|";
        }
        if(grid[row][col]!=0){
            cout<<grid[row][col];
            for(int _=0;_<8;_++){cout<<" ";}
            cout<<"|";
        }else{
            vector<int> inference = getInference(row, col);
            for (int val : inference) {
                cout << val;
            }
            for(int _=0;_<10-int(inference.size());_++){cout<<" ";}
            cout<<"|";
        }
        if(col==8){cout<<'\n';}
    }
    //显示所有值
    void displayInference_all() {
        for(int i=0;i<9;i++){
            for(int j=0;j<9;j++){
                displayInference(i,j);
            }
        }
    }
};
int main() {
    // 得到输入
    string input = "300967001040302080020000070070000090000873000500010003004705100905000207800621004";//017903600000080000900000507072010430000402070064370250701000065000030000005601720 

    // 创建 Sudoku 实例
    Sudoku sudoku(input);

    // 显示 解串行化的数独方格
    cout << "Initial Sudoku Grid:\n";
    sudoku.displayGrid();

    //输出所有格子的可能值
    sudoku.displayInference_all();

    return 0;
}
