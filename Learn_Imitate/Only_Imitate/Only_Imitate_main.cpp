#include <stdlib.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <time.h>
#include <math.h>
#include "Node.h"
#include <cstdio>
#include <string>
#include <vector>

using namespace std;

const int nodenumber = 10000;
const int totaledges = 20000;

const int cooperate = 1;
const int defect = 0;

int actions[2] = {defect, cooperate};

// The states represent the fraction of cooperators in the individual's neighborhood
double states[5] = {0.0, 0.25, 0.5, 0.75, 1.0};
const int actNum = 2;
const int staNum = 5;

// Return the index of distribution list based on the probability
int chooseFromDis(vector<double> distribution) {
    double randomW = (double) rand() / RAND_MAX;
    double sumW = 0.0;
    for (int disI = 0; disI < distribution.size(); disI++) {
        sumW += distribution[disI];
        if (randomW <= sumW) {
            return disI;
        }
    }
	cout << "There is an error!" << endl;
    return 0;
}


int tellState(double coopFrac) {
    if (coopFrac < 0.25) { // zero cooperator
        return 0;
    }
    else if (coopFrac < 0.5) { // one cooperator
        return 1;
    }
    else if (coopFrac < 0.75) { // two cooperator
        return 2;
    }
    else if (coopFrac < 1) { // three cooperator
        return 3;
    }
    else { // four cooperator
        return 4;
    }
}

int main(int argc, char* argv[]) {
    int runs = atoi(argv[1]);
    int nets = atoi(argv[2]);
    long int playtimes = atoll(argv[3]);
    long int initialtimes = atoll(argv[4]);
    float w = atof(argv[5]);

    char buff[100];
    sprintf(buff, "w_%.2f_fraction.txt", w);
    string outFilename = buff;

    cout << outFilename << endl;
    ofstream out_f(outFilename.c_str());

    srand(time(0));
    int h_nets, h_runs;
    int i, j, k, staK, actK;
    int stateIndex;
    double r;

    vector<vector<double>> sumAccount (staNum, vector<double> (actNum));
    vector<vector<double>> avgFrac (staNum, vector<double> (actNum));

    Node *p = NULL;
    Node *q = NULL;

    vector<double> curAction (nodenumber);
    vector<double> preAction (nodenumber);

    vector<vector<vector<double>>> curStrategyFrac (nodenumber, vector<vector<double>> (staNum, vector<double> (actNum)));
    vector<vector<vector<double>>> preStrategyFrac (nodenumber, vector<vector<double>> (staNum, vector<double> (actNum)));

    vector<double> curState (nodenumber);
    vector<double> preState (nodenumber);

    vector<double> payoffs (nodenumber);
    vector<double> opayoffs (nodenumber);
    vector<double> contribution (nodenumber);
    double fre_c;
    double co_number;

    double alpha = 0.05;

    for (r = 0.2; r <= 1.2; r = r + 0.05) {
        for (staK = 0; staK < staNum; staK++) {
            for (actK = 0; actK < actNum; actK++) {
                avgFrac[staK][actK] = 0.0;
            }
        }

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
                    for (staK = 0; staK < staNum; staK++) {
                        // There is a half probability to choose defect behavior
                        curStrategyFrac[k][staK][0] = rand() % 2;
                        curStrategyFrac[k][staK][1] = 1.0 - curStrategyFrac[k][staK][0];
                    }
                }
                
                for (int pt = 0; pt < playtimes; pt++) {
                    for (k = 0; k < nodenumber; k++) {
                        for (staK = 0; staK < staNum; staK++) {
                            for (actK = 0; actK < actNum; actK++) {
                                preStrategyFrac[k][staK][actK] = curStrategyFrac[k][staK][actK];
                            }
                        }
                        payoffs[k] = 0;
                        contribution[k] = 0;
                    }
                    
                    // If it is the first round, nodes choose action randomly.
                    // If the probability is less than w, then individual will choose action randomly.
                    double w_d = (double) rand() / RAND_MAX;
                    if (pt == 0 || w_d < w) {
                        for (k = 0; k < nodenumber; k++) {
                            curAction[k] = rand() % 2;
                            preAction[k] = curAction[k];
                        }
                    }
                    else {
                        for (k = 0; k < nodenumber; k++) {
                            double neighCoopFrac = 0.0;
                            double neighCoopNum = 0.0;
                            p = node[k].head->next;
                            while (p != NULL) {
                                if (preAction[p->nodecode] == 1) {
                                    neighCoopNum += 1;
                                }
                                p = p->next;
                            }
                            neighCoopFrac = neighCoopNum / node[k].neinumber();
                            curState[k] = tellState(neighCoopFrac);
                            stateIndex = curState[k];
                            curAction[k] = chooseFromDis(curStrategyFrac[k][stateIndex]);
                            preAction[k] = curAction[k];
                        }
                    }
                    
                    for (k = 0; k < nodenumber; k++) {
                        p = node[k].head;
                        while (p != NULL) {
                            contribution[k] = contribution[k] + curAction[p->nodecode];
                            p = p->next;
                        }
                    }
                    
                    for (k = 0; k < nodenumber; k++) {
                        p = node[k].head;
                        while (p != NULL) {
                            p->payoffs = contribution[p->nodecode] * r * 5 / (node[p->nodecode].neinumber() + 1);
                            payoffs[k] = payoffs[k] + p->payoffs;
                            p = p->next;
                        }
                        payoffs[k] = payoffs[k] - curAction[k] * (node[k].neinumber() + 1);
                    }
                    
                    // Imitating Process
                    for (k = 0; k < nodenumber; k++) {
                        int t;
                        p = node[k].head;
                        t = rand() % (node[k].neinumber() + 1);
                        for (int kp = 0; kp < t; kp++) {
                            p = p->next;
                        }
                        double t1 = 1 / (1 + exp(10 * (payoffs[k] - payoffs[p->nodecode])));
                        double t2 = (double) rand() / RAND_MAX;
                        if (t2 <= t1) {
                            for (staK = 0; staK < staNum; staK++) {
                                for (actK = 0; actK < actNum; actK++) {
                                    // The node will imitate his neighbor's whole strategy, regardless of the state.
                                    curStrategyFrac[k][staK][actK] = preStrategyFrac[p->nodecode][staK][actK];
                                }
                            }
                        }
                    }
                    
                    if (pt >= initialtimes) {
                        for (staK = 0; staK < staNum; staK++) {
                            for (actK = 0; actK < actNum; actK++) {
                                sumAccount[staK][actK] = 0;
                            }
                        }
                        for (staK = 0; staK < staNum; staK++) {
                            for (actK = 0; actK < actNum; actK++) {
                                for (k = 0; k < nodenumber; k++) {
                                    sumAccount[staK][actK] += curStrategyFrac[k][staK][actK];
                                }
                            }
                        }
                        for (staK = 0; staK < staNum; staK++) {
                            for (actK = 0; actK < actNum; actK++) {
                                sumAccount[staK][actK] = sumAccount[staK][actK] / nodenumber;
                            }
                        }
                        for (staK = 0; staK < staNum; staK++) {
                            for (actK = 0; actK < actNum; actK++) {
                                avgFrac[staK][actK] += sumAccount[staK][actK];
                            }
                        }
                    }
                } // End pt
            } // End h_runs
        } // End h_nets
        for (staK = 0; staK < staNum; staK++) {
            for (actK = 0; actK < actNum; actK++) {
                avgFrac[staK][actK] = avgFrac[staK][actK] / (nets * runs * (playtimes - initialtimes));
            }
        }
        
        out_f << r << endl;
        for (staK = 0; staK < staNum; staK++) {
            out_f << staK;
            for (actK = 0; actK < actNum; actK++) {
                out_f << "\t" << avgFrac[staK][actK];
            }
            out_f << endl;
        }
        cout << "end r" << "\t" << r << endl;
    } // End r
} // End main
