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

    ofstream out_f("Cooperators_Fraction.txt");

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

    double alpha = 0.05;

    for (r = 0.2; r <= 2.05; r = r + 0.05) {
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

                for (int pt = 0; pt < playtimes; pt++) {
                    for (k = 0; k < nodenumber; k++) {
                        payoffs[k] = 0;
                        ostrategy[k] = strategy[k];
                        contribution[k] = 0;
                        coopNum[k] = 0;
                    }
                    for (k = 0; k < nodenumber; k++) {
                        p = node[k].head;
                        while (p != NULL) {
                            contribution[k] = contribution[k] + strategy[p->nodecode];
                            p = p->next;
                        }
                    }
                    for (k = 0; k < nodenumber; k++) {
                        p = node[k].head;
                        while (p != NULL) {
                            p->payoffs = contribution[p->nodecode] * r * 5 / (node[p->nodecode].neinumber() + 1);
                            // However, this network structure is a lattice.
                            // p->payoffs = contribution[p->nodecode] * r;
                            payoffs[k] = payoffs[k] + p->payoffs;
                            p = p->next;
                        }
                        payoffs[k] = payoffs[k] - strategy[k] * (node[k].neinumber() + 1);
                        // payoffs[k] = payoffs[k] - strategy[k] * 5;
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
                } // End pt
            } // End h_runs
        } // End h_nets
        f = f / (nets * runs * (playtimes - initialtimes));
        out_f << r << '\t' << f << endl;
        cout << "End r" << '\t' << r << endl;
    } // End r
} // End main

