//
// Created by dc199 on 2018/10/9.
//

#include <iostream>
#include <fstream>

using namespace std;

struct Node {
    int nodecode;
    double payoffs;
    int supervise_flag;
    Node *next;
};

class list {
public:
    Node *head;
    list() {
        head = new Node;
        head->next = NULL;
    }
    ~list();
    void insert(int i);
    int neinumber(void);
    int check(int i);
    void dropNode(int i);
    void cutoff(int i);
};

list::~list() {
    Node *p = head->next, *q;
    while (p != NULL) {
        q = p->next;
        delete p;
        p = NULL;
        p = q;
    }
    delete head;
    head = NULL;
}

void list::insert(int i) {
    Node *s, *q = head;
    s = new Node;
    s->nodecode = i;
    s->next = q->next;
    q->next = s;
}

int list::neinumber() {
    int number = 0;
    Node *p = head;
    p = head->next;
    while (p != NULL) {
        number++;
        p = p->next;
    }
    return number;
}

int list::check(int i) {
    Node *q = head;
    while (q != NULL) {
        if (q->nodecode == i) {
            q = NULL;
            return 1;
        }
    }
    q = NULL;
    return 0;
}

// drop one node
void list::dropNode(int i) {
   Node *s, *q = head;
   s = q->next;
   while (s != NULL) {
       if (s->nodecode == i) {
           q->next = s->next;
           delete s;
           s = NULL;
           return;
       }
       q = s;
       s = s->next;
   }
}

// cut off the rest of the list
void list::cutoff(int i) {
    Node *s, *q = head;
    s = q->next;
    while (s != NULL) {
        if (s->nodecode == i) {
            q->next = s->next;
            s->next = NULL;
            delete s;
            return;
        }
        q = s;
        s = s->next;
    }
}
