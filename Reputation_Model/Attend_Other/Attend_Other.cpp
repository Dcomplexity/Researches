//
// Created by dc199 on 2018/10/9.
//

#include <stdlib.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <time.h>
#include <math.h>
#include <cstdio>
#include <string>
#include <vector>

#include "Node.h"

using namespace std;

const int nodenumber = 10000;
const int totaledges = 20000;

int main(int argc, char* argv[]) {
    int runs = atoi(argv[1]);
    int nets = atoi(argv[2]);

    long int playtimes = atoll(argv[3]);
    long int initialtimes = atoll(argv[4]);

    double initialMorVal = atof(argv[5]);

    char buff[100];
    sprintf(buff, "MorVal_%.3f_fraction.txt", initialMorVal);
    string outFilename = buff;

    cout << outFilename << endl;
    ofstream out_f(outFilename.c_str());

    srand(time(0));
    int h_nets, h_runs;
    int i, j, k;
    double r;
    double cnumber = 0;
    double f = 0;
    Node *p = NULL;
    Node *q = NULL;
    double strategy[nodenumber];
    double ostrategy[nodenumber];
    double payoffs[nodenumber];
    double opayoffs[nodenumber];
    double contribution[nodenumber];
    double coopNum[nodenumber];
    double fre_c;
    double co_number;

    double morValList[nodenumber];
    double involveNum[nodenumber];

    // This value is to store the Frequence of Strategy used to show the final state.
    double strategyFre[nodenumber];

    double alpha = 0.05;

    clock_t startTime, endTime;

    for (r = 0.2; r <= 2.05; r = r + 0.05) {
        startTime = clock();
        f = 0;
        for (h_nets = 0; h_nets < nets; h_nets++) {
            list node[nodenumber];
            int j_n[4];
            for (k = 0; k < nodenumber; k++) {
                node[k].head->nodecode = k;
            }
            for (k = 0; k < nodenumber; k++) {
                node[k].head->next = NULL;
            }
            for (k = 0; k < nodenumber; k++) {
                morValList[k] = initialMorVal;
            }
            for (k = 0; k < nodenumber; k++) {
                i = k;
                j_n[0] = (i + 1) % 100 + (i / 100) * 100;
                j_n[1] = (i + 99) % 100 + (i / 100) * 100;
                j_n[2] = (i + 9900) % 10000;
                j_n[3] = (i + 100) % 10000;
                for (int k_n = 0; k_n < 4; k_n++) {
                    node[i].insert(j_n[k_n]);
                }
            }
            for (h_runs = 0; h_runs < runs; h_runs++) {
                for (k = 0; k < nodenumber; k++) {
                    strategy[k] = rand() % 2;
                }
                for (k = 0; k < nodenumber; k++) {
                    morValList[k] = initialMorVal;
                }
                for (k = 0; k < nodenumber; k++) {
                    strategyFre[k] = 0.0;
                }
                for (int pt = 0; pt < playtimes; pt++) {
               //     vector<vector<int>> gameChain(nodenumber, vector<int> ());

                    if (r == 0.2 && pt == 0) {
                        ofstream fStart("strategy_matrix_start.txt");
                        for (int ki = 0; ki < 100; ki++) {
                            for (int kj = 0; kj < 100; kj++) {
                                fStart << strategy[ki * 100 + kj] << " ";
                            }
                            fStart << '\n';
                        }
                        fStart.close();
                    }

                    list gameChain[nodenumber];
                    for (k = 0; k < nodenumber; k++) {
                        gameChain[k].head->nodecode = k;
                    }
                    for (k = 0; k < nodenumber; k++) {
                        gameChain[k].head->next = NULL;
                    }

                    for (k = 0; k < nodenumber; k++) {
                        payoffs[k] = 0;
                        ostrategy[k] = strategy[k];
                        contribution[k] = 0;
                        coopNum[k] = 0;
                        involveNum[k] = 0;
                    }

//                    for (k = 0; k < nodenumber; k++) {
//                        p = node[k].head;
//                        while (p != NULL) {
//                            double morPro = (double)rand() / RAND_MAX;
//                            if (morPro < morValList[p->nodecode]) {
//                                // if the individual attend the public goods game, the flag is one.
//                                gameChain[p->nodecode].push_back(k);
//                                contribution[k] = contribution[k] + strategy[p->nodecode];
//                                participateNum[k] = participateNum[k] + 1;
//                            }
//                            p = p->next;
//                        }
//                    }
//
//                    for (k = 0; k < nodenumber; k++) {
//                        for (int kk = 0; kk < gameChain[k].size(); kk++) {
//                           int hostNode = gameChain[k][kk];
//                           payoffs[k] = payoffs[k] + contribution[hostNode] * r * 5 / participateNum[hostNode];
//                        }
//                        payoffs[k] = payoffs[k] - strategy[k] * gameChain[k].size();
//                    }

                    for (k = 0; k < nodenumber; k++) {
                        p = node[k].head;
                        while (p != NULL) {
                            double morPro = (double)rand() / RAND_MAX;
                            if (morPro < morValList[p->nodecode]) {
                                gameChain[p->nodecode].insert(k);
                                contribution[k] = contribution[k] + strategy[p->nodecode];
                                involveNum[k] = involveNum[k] + 1;
                            }
                            p = p->next;
                        }
                    }

                    for (k = 0; k < nodenumber; k++) {
                        p = gameChain[k].head->next;
                        // Here, we do not need to decide whether involveNum[p->nodecode] is 0.
                        // Because, if p != NULL, means that the node k attend the public goods game hosted by p.
                        // Then, the involveNum[p->nodecode] can not be 0.
                        while (p != NULL) {
                            payoffs[k] = payoffs[k] + contribution[p->nodecode] * r * 5 / involveNum[p->nodecode];
                            p = p->next;
                        }
                        payoffs[k] = payoffs[k] - strategy[k] * gameChain[k].neinumber();
                    }

                    for (k = 0; k < nodenumber; k++) {
                        if (strategy[k] == 0) {
                            p = node[k].head;
                            float neighCoNum = 0.0;
                            while (p != NULL) {
                                if (strategy[p->nodecode] == 1) {
                                    neighCoNum += 1.0;
                                }
                                p = p->next;
                            }
                            morValList[k] = morValList[k] - morValList[k] * neighCoNum/(node[k].neinumber() + 1);
                        }
                    }

                    // Imitating Process
                    for (k = 0; k < nodenumber; k++) {
                        double w1 = 0.01;
                        double w2 = (double)rand() / RAND_MAX;
                        if (w1 > w2) {
                            if (strategy[k] == 1) {
                                strategy[k] = 0;
                            }
                            else {
                                strategy[k] = 1;
                            }
                        }
                        else {
                            int t;
                            p = node[k].head;
                            t = rand() % (node[k].neinumber() + 1);
                            for (int kp = 0; kp < t; kp++) {
                                p = p->next;
                            }
                            double t1 = 1 / (1 + exp(10 * (payoffs[k] - payoffs[p->nodecode])));
                            double t2 = (double) rand() / RAND_MAX;
                            if (t2 <= t1) {
                                strategy[k] = ostrategy[p->nodecode];
                            }
                        }
                    }

                    if (pt >= initialtimes) {
                        cnumber = 0;
                        for (k = 0; k < nodenumber; k++) {
                            if (strategy[k] == 1) {
                                cnumber += 1;
                            }
                        }
                        cnumber = cnumber / nodenumber;
                        f =  f + cnumber;
                    }

                    if (h_nets == nets-1 && h_runs == runs-1 && r == 0.2)
                    {
                        if (pt >= initialtimes) {
                            for (k = 0; k < nodenumber; k++) {
                                strategyFre[k] += strategy[k];
                            }
                        }
                    }

                    if (pt == playtimes-1 && h_nets == nets-1 && h_runs == runs-1 && r == 0.2) {
                        int finalNums = playtimes - initialtimes;
                        for (k = 0; k < nodenumber; k++) {
                            strategyFre[k] = strategyFre[k] / finalNums;
                        }
                        ofstream fFinal("strategy_matrix_final.txt");
                        for (int ki = 0; ki < 100; ki++){
                            for (int kj = 0; kj < 100; kj++) {
                                fFinal << strategyFre[ki * 100 + kj] << " ";
                            }
                            fFinal << '\n';
                        }
                        fFinal.close();
                    }
                } // End pt
            } // End h_runs
        } // End h_nets
        f = f / (nets * runs * (playtimes - initialtimes));
        out_f << r << '\t' << f << endl;
        endTime = clock();
        double totalTime;
        totalTime = (double)(endTime - startTime) / CLOCKS_PER_SEC;
        cout << "End r" << '\t' << r << '\t' << totalTime << "s" << endl;
    } // End r
} // End main

