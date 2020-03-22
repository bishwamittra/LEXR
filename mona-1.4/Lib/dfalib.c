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

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "dfalib.h"

void makeIncident(mdDfa *dfa, mdState i, mNode n, int *j)
{
  if (dfa->bdd[n].idx == -1)
    dfa->incident[i][*(j++)] = dfa->bdd[n].lo;
  else {
    makeIncident(dfa, i, dfa->bdd[n].lo, j);
    makeIncident(dfa, i, dfa->bdd[n].hi, j);
  }
}

mdDfa *mdLoad(char *filename)
{
  FILE *file;
  mdDfa *dfa;
  mdState i;
  int j;

  if ((file = fopen(filename, "r")) == 0)
    return 0;
  dfa = (mdDfa *) malloc(sizeof(mdDfa));
  if (fscanf(file,
	     "MONA DFA\n"
	     "number of variables: %u\n"
	     "variables:",
	     &dfa->numVars) != 1) {
    fclose(file);
    free(dfa);
    return 0;
  }
  dfa->var = (char **) malloc(sizeof(char *)*dfa->numVars);
  for (i = 0; i < dfa->numVars; i++) {
    char t[100];
    if (fscanf(file, " %s", t) != 1) {
      fclose(file);
      free(dfa);
      return 0;
    }
    dfa->var[i] = (char *) malloc(sizeof(char)*(strlen(t)+1));
    strcpy(dfa->var[i], t);
  }
  if (fscanf(file, "\norders:") != 0) {
    fclose(file);
    free(dfa);
    return 0;
  }
  dfa->order = (int *) malloc(sizeof(int)*dfa->numVars);
  for (i = 0; i < dfa->numVars; i++)
    if (fscanf(file, " %d", &dfa->order[i]) != 1) {
      fclose(file);
      free(dfa);
      return 0;
    }
  if (fscanf(file,
	     "\nstates: %u\n"
	     "initial: %u\n"
	     "bdd nodes: %u\n"
	     "final:", 
	     &dfa->states, &dfa->q0, &dfa->bddNodes) != 3) {
    fclose(file);
    free(dfa);
    return 0;
  }
  dfa->f = (mdKind *) malloc(sizeof(mdKind)*dfa->states);
  for (i = 0; i < dfa->states; i++) {
    int t;
    if (fscanf(file, " %d", &t) != 1) {
      fclose(file);
      free(dfa);
      return 0;
    }
    dfa->f[i] = t;
  }
  if (fscanf(file, "\nbehaviour:") != 0) {
    fclose(file);
    free(dfa);
    return 0;
  }
  dfa->behaviour = (mNode *) malloc(sizeof(mNode)*dfa->states);
  for (i = 0; i < dfa->states; i++)
    if (fscanf(file, " %u", &dfa->behaviour[i]) != 1) {
      fclose(file);
      free(dfa);
      return 0;
    }
  if (fscanf(file, "\nbdd:\n") != 0) {
    fclose(file);
    free(dfa);
    return 0;
  }
  dfa->bdd = (mBdd *) malloc(sizeof(mBdd)*dfa->bddNodes);
  for (i = 0; i < dfa->bddNodes; i++)
    if (fscanf(file, "%i %u %u\n", 
	       &dfa->bdd[i].idx,
	       &dfa->bdd[i].lo,
	       &dfa->bdd[i].hi) != 3) {
      fclose(file);
      free(dfa);
      return 0;
    }
  dfa->incident = 0;

  if (fscanf(file, " ") != 0) {
    fclose(file);
    free(dfa);
    return 0;
  }
  if (fgetc(file) != 'e' ||
      fgetc(file) != 'n' ||
      fgetc(file) != 'd') {
    fclose(file);
    mdFree(dfa);
    return 0;
  }
  fclose(file);

  dfa->incident = (unsigned **) malloc(sizeof(unsigned *)*dfa->states);
  for (i = 0; i < dfa->states; i++) {
    dfa->incident[i] = (unsigned *) malloc(sizeof(unsigned)*(dfa->states+1));
    j = 0;
    makeIncident(dfa, i, dfa->behaviour[i], &j);
    dfa->incident[i][j] = -1;
  } 
  
  return dfa;
}

int mdStore(mdDfa *dfa, char *filename)
{
  int i;
  FILE *file;

  if ((file = fopen(filename, "w")) == 0)
    return 0;

  fprintf(file,
	  "MONA DFA\n"
	  "number of variables: %u\n"
	  "variables:", dfa->numVars);
  for (i = 0; i < dfa->numVars; i++)
    fprintf(file, " %s", dfa->var[i]);
  fprintf(file, "\norders:");
  for (i = 0; i < dfa->numVars; i++)
    fprintf(file, " %d", dfa->order[i]);
  fprintf(file,
	  "\nstates: %u\n"
	  "initial: %u\n"
	  "bdd nodes: %u\n"
	  "final:",
	  dfa->states, dfa->q0, dfa->bddNodes);
  for (i = 0; i < dfa->states; i++) {
    int t = dfa->f[i];
    fprintf(file, " %d", t);
  }
  fprintf(file, "\nbehaviour:");
  for (i = 0; i < dfa->states; i++)
    fprintf(file, " %u", dfa->behaviour[i]);
  fprintf(file, "\nbdd:\n");
  for (i = 0; i < dfa->bddNodes; i++)
    fprintf(file, "%i %u %u\n", 
	    dfa->bdd[i].idx,
	    dfa->bdd[i].lo,
	    dfa->bdd[i].hi);
  fprintf(file, "end\n");

  fclose(file);
  return 1;
}

void mdFree(mdDfa *dfa)
{
  int i;
  if (dfa->incident) {
    for (i = 0; i < dfa->states; i++)
      free(dfa->incident[i]);
    free(dfa->incident);
  }
  free(dfa->behaviour);
  free(dfa->bdd);
  free(dfa->f);
  for (i = 0; i < dfa->numVars; i++) {
    free(dfa->var[i]);
  }
  free(dfa->var);
  free(dfa->order);
  free(dfa);
}

mdState mdDelta(mdDfa *dfa, mdState s, mA a)
{
  mNode n = dfa->behaviour[s];
  
  while (dfa->bdd[n].idx != -1)
    if (a[dfa->bdd[n].idx])
      n = dfa->bdd[n].hi;
    else
      n = dfa->bdd[n].lo;

  return dfa->bdd[n].lo;
}
