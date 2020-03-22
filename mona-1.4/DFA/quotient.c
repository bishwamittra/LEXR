/*
 * MONA
 * Copyright (C) 1997-2013 Aarhus University.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the  Free Software
 * Foundation, Inc., 51 Franklin Street, Suite 500, Boston, MA 02110-1335,
 * USA.
 */

#include "dfa.h"
#include "../BDD/hash.h"
#include "../Mem/mem.h"

struct slist_ {
  int state;
  struct slist_ *next;  
};

typedef struct slist_ *slist;

struct state_inf_fwd_ {
  int is_final;
  int go_1,go_2;
};
typedef struct state_inf_fwd_ state_inf_fwd;

struct graph_ {
  int *stack;
  int top;
  slist *V; 
  int *F; 
};

typedef struct graph_ graph;

graph *new_graph(int sz) 
{
  int i;
  graph *G=mem_alloc(sizeof(graph));
  
  G->stack = mem_alloc((sizeof *(G->stack)) * sz);
  G->top=0;
  G->V = mem_alloc((sizeof *(G->V)) * sz);
  G->F = mem_alloc((sizeof *(G->F)) * sz);
  for (i=0;i<sz;i++) { G->V[i] = NULL; G->F[i]= 0; }
  return G;
}

void reset_finals(graph *G, int sz) 
{
  int i;
  G->top=0;
  for (i=0;i<sz;i++) G->F[i] = 0;
}

slist new_state(int state, slist nxt)
{  slist l = mem_alloc(sizeof *l);
   l->state = state;
   l->next = nxt;
   return(l);
}

void insert_edge(graph *G, int from, int to) {
  (G->V)[from] = new_state(to, (G->V)[from]);
}

void final_add(graph *G, int i) {
  if (!G->F[i]) {
    G->stack[G->top] = i;
    G->top++;
    G->F[i]=1;
  }
}

int pick_final(graph *G) 
{
  if (G->top) {
    G->top--;
    return G->stack[G->top];
  }
  else 
    return -1;
}

graph *revert(state_inf_fwd *R, int size) 
{
  int i;
  graph *G=new_graph(size);
  
  for(i=0; i<size; i++) {
    if (R[i].go_1 == R[i].go_2) {
      insert_edge(G, R[i].go_1, i);
    }
    else {
      insert_edge(G, R[i].go_1, i);
      insert_edge(G, R[i].go_2, i);
    }
  };  
  return G;
}

void make_finals(graph *G, state_inf_fwd *R, int sz) 
{
  int i;  
  G->top=0;
  for (i=0;i<sz;i++) G->F[i] = 0;
  for(i=0; i<sz; i++) 
    if (R[i].is_final) 
      final_add(G,i);
}

void color(graph *G) {
  slist sl;
  int v;

  while ((v=pick_final(G))!=(-1)) {
    sl=G->V[v];
    while (sl) {
      final_add(G,sl->state);
      sl = sl->next;
    }
  }
}

int read00(bdd_manager *bddm, bdd_ptr p, unsigned var_index, int choice) {
  if (bdd_is_leaf(bddm, p)) {
    return bdd_leaf_value(bddm, p);
  }
  else {
    if (bdd_ifindex(bddm,p)==var_index) {
      if (choice)
        return (read00(bddm, bdd_then(bddm,p), var_index, choice));
      else
        return (read00(bddm, bdd_else(bddm,p), var_index, choice));
    }
    else
      return (read00(bddm, bdd_else(bddm,p), var_index, choice));
  }
}

/*

void print_G(graph *G, int sz) 
{
  slist sl;
  int i;

  for (i=0; i<sz; i++) {
    printf("\nto state %i from:\n",i);
    sl=G->V[i];
    while (sl) {
      printf("%i ",sl->state);
      sl = sl->next;
    }
    if (G->F[i]) printf("\nis final");
  }
}
  
void print_R(state_inf_fwd *R, int sz)
{
  int i;

  for (i=0; i<sz; i++) {
    printf("State %i: go_1=%i, go_2=%i\n",i, R[i].go_1, R[i].go_2);
  };
}

*/

void free_G(graph *G, int sz) 
{
  slist snxt, sold;
  int i;

  for (i=0; i<sz; i++) {
    snxt=G->V[i];
    while ((sold=snxt)) {
      snxt = sold->next;
      mem_free(sold); 
    }
  }
  mem_free(G->V);
  mem_free(G->F);
  mem_free(G->stack);
  mem_free(G); 
}

void dfaRightQuotient(DFA *a, unsigned var_index) 
{
  graph *G;
  int i;
  state_inf_fwd *R = mem_alloc(sizeof(*R)*(a->ns));
  int *f = mem_alloc(sizeof(*f)*(a->ns));
    
  for (i=0; i<a->ns; i++) {
    R[i].go_1 = read00(a->bddm, a->q[i], var_index, 0);
    R[i].go_2 = read00(a->bddm, a->q[i], var_index, 1);
    R[i].is_final = (a->f[i] == 1)? 1 : 0;
  };
  /* find states from which some string of 00..00X00..00
     letters can reach a +1 state; put result in f */
  G = revert(R, a->ns);
  make_finals(G, R, a->ns);
  color(G);
  for(i=0;i<a->ns;i++) 
    f[i] = (G->F[i]? 1 : 0);
  /* find states from which some string of 00..00X00..00
     letters can reach a -1 state */
  for (i=0; i<a->ns; i++) 
    R[i].is_final = (a->f[i] == -1)? 1 : 0;
  make_finals(G, R, a->ns);
  color(G);
  /* now a state is +1 if some path along 00..00x00..00 letters takes
     it to an original +1 state; otherwise, the state is -1 if some
     such path takes it to an original -1 state: */
  for(i=0;i<a->ns;i++) {
    a->f[i] = (f[i]? 1 : (G->F[i]? -1 : 0));
  }
  free_G(G, a->ns);
  mem_free(f);
  mem_free(R);
}

