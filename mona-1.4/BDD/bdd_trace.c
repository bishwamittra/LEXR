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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bdd.h"
#include "bdd_internal.h"

trace_descr copy_reversed_trace(trace_descr current_trace)
{
  trace_descr reversed_trace;
  trace_descr this_trace;

  reversed_trace = NULL;
  
  while (current_trace) {
    this_trace = (trace_descr) mem_alloc(sizeof(struct trace_descr_));
    this_trace->index = current_trace->index;
    this_trace->value = current_trace->value;
    this_trace->next = reversed_trace;

    reversed_trace = this_trace;
    current_trace = current_trace->next;
  }

  return reversed_trace;
}

paths join_paths(paths *plist1, paths plist2)
{
  if (*plist1) {
    paths pp;
    
    for (pp = *plist1; pp->next; pp = pp->next);
      
    pp->next = plist2;
  }
  else
    *plist1 = plist2;

  return (*plist1);
}

paths mk_paths(bdd_manager *bddm, unsigned p, trace_descr current_trace)
{
  unsigned l, r, index;

  LOAD_lri(&bddm->node_table[p], l, r, index);

  if (index == BDD_LEAF_INDEX) {
    paths this_path;

    this_path = (paths) mem_alloc(sizeof(struct paths_));
    this_path->to = l;
    this_path->trace = copy_reversed_trace (current_trace);
    this_path->next = NULL;

    return this_path;
  }
  else {
    trace_descr this_trace;
    paths right_paths, left_paths;

    this_trace = (trace_descr) mem_alloc(sizeof(struct trace_descr_));
    this_trace->index = index;
    this_trace->value = TRUE;
    this_trace->next = current_trace;

    right_paths = mk_paths(bddm, r, this_trace);

    this_trace->value = FALSE;

    left_paths = mk_paths(bddm, l, this_trace);

    mem_free (this_trace);

    return (join_paths(&left_paths, right_paths));
  }
    
}

paths make_paths(bdd_manager *bddm, unsigned p)
{ 
  return (mk_paths(bddm, p, NULL));
}

void kill_trace(trace_descr t)
{
  if (t) {
    kill_trace (t->next);
    mem_free(t);
  }
}

void kill_paths(paths p)
{
  if (p) {
    kill_trace (p->trace);
    kill_paths (p->next);
    mem_free(p);
  }
}

trace_descr find_one_path(bdd_manager *bddm, unsigned p, unsigned q)
{
  unsigned l, r, index;

  LOAD_lri(&bddm->node_table[p], l, r, index);
  
  if (index == BDD_LEAF_INDEX) {
    if (l == q) {
      trace_descr this_trace;

      this_trace = (trace_descr) mem_alloc(sizeof(struct trace_descr_));
      this_trace->index = index;
      this_trace->value = TRUE;
      this_trace->next = NULL;

      return this_trace;
    }
    else
      return NULL;
  }
  else {
    trace_descr sub_trace, this_trace;
    
    sub_trace = find_one_path(bddm, l, q);
    if (sub_trace) {
      this_trace = (trace_descr) mem_alloc(sizeof(struct trace_descr_));
      this_trace->index = index;
      this_trace->value = FALSE;
      this_trace->next = sub_trace;

      return this_trace;      
    }

    sub_trace = find_one_path(bddm, r, q);
    if (sub_trace) {
      this_trace = (trace_descr) mem_alloc(sizeof(struct trace_descr_));
      this_trace->index = index;
      this_trace->value = TRUE;
      this_trace->next = sub_trace;

      return this_trace;      
    }

    return NULL;
  }
}

void print_bddpaths(unsigned p, unsigned q, bdd_manager *bddm, unsigned b, unsigned no_free_vars, unsigned *offsets)
{
  paths state_paths, pp;
  trace_descr tp;
  int j;

  state_paths = pp = make_paths(bddm, b);
  
  while (pp) {
    printf ("(%d,%d,", p,q);
    for (j = 0; j < no_free_vars; j++) {
      for (tp = pp->trace; tp && (tp->index != offsets[j]); tp = tp->next);
      
      if (tp) {
	if (tp->value) printf("1");
	else printf("0");
      }
      else
	printf("X");	    
    }
    
    printf (") -> %d\n", pp->to);
    pp = pp->next;
  }
  
  kill_paths(state_paths);
}

void print_bddpaths_verbose(unsigned p, unsigned q, bdd_manager *bddm, unsigned b)
{
  paths state_paths, pp;
  trace_descr tp;

  state_paths = pp = make_paths(bddm, b);
  
  while (pp) {
    printf("(%d,%d,", p,q);
    
    for (tp = pp->trace; tp; tp = tp->next) {
      printf("#%d=%c", tp->index, tp->value ? '1' : '0');
      if (tp->next)
	printf(", ");
    }

    printf(") -> %d\n", pp->to);
    pp = pp->next;
  }
  
  kill_paths(state_paths);
}

void print_one_path(unsigned p, unsigned q, bdd_manager *bddm, unsigned no_free_vars, unsigned *offsets)
{
  trace_descr tp,tp_run;
  unsigned j;

  tp = find_one_path(bddm, p, q);
  for (j = 0; j < no_free_vars; j++) {
    tp_run = tp;
    for (;tp_run && (tp_run->index != offsets[j]); tp_run = tp_run->next);
    
    if (tp_run) {
      if (tp_run->value) printf("1");
      else printf("0");
    }
    else
      printf("X");	    
  };
  kill_trace(tp);
}  
