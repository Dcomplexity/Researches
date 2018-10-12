#include <iostream>
#include <vector>
using namespace std;
int staNum = 5;
int actNum = 2;
int nodenumber = 10;

int main(int argc, char const *argv[])
{
//    vector <int> first (10); // It will initial the vector by 0
//    for (int i = 0; i < 10; i++) {
//        first[i] = i;
//    }
//    for (int i = 0; i < first.size(); i++) {
//        cout << first[i] << endl;
//    }
//
//    vector<vector<int>> second (4, vector<int> (4));
//    for (int i = 0; i < second.size(); i++) {
//        for (int j = 0; j < second[i].size(); j++) {
//            cout << second[i][j] << "\t";
//        }
//        cout << endl;
//    }
//    vector<vector<double>> sumAccount (staNum, vector<double> (actNum));
//    vector<vector<double>> avgFrac (staNum, vector<double> (actNum));
//    for (int i = 0; i < sumAccount.size(); i++) {
//        for (int j = 0; j < sumAccount[i].size(); j++){
//            cout << sumAccount[i][j] << "\t";
//        }
//        cout << endl;
//    }
//
//    vector<vector<vector<double>>> curStrategyFrac (nodenumber, vector<vector<double>> (staNum, vector<double> (actNum)));
//    vector<vector<vector<double>>> preStrategyFrac (nodenumber, vector<vector<double>> (staNum, vector<double> (actNum)));
//
//    int count = 0;
//    for(int i = 0; i < curStrategyFrac.size(); i++) {
//        for(int j = 0; j < curStrategyFrac[i].size(); j++){
//            for (int k = 0; k < curStrategyFrac[i][j].size(); k++){
//                count += 1;
//                cout << count << "\t" << curStrategyFrac[i][j][k] << endl;
//            }
//        }
//    }
    vector<vector<int>> gameChain (10000, vector<int> ());
    for (int i = 0; i < gameChain.size(); i++) {
        for (int j = 0; j < 10; j++) {
            gameChain[i].push_back(j);
        }
    }
    for (int i = 0; i < gameChain.size(); i++) {
        for (int j = 0; j < gameChain[i].size(); j++) {
            cout << gameChain[i][j] << "\t";
        }
        cout << endl;
    }

    
    return 0;
}
