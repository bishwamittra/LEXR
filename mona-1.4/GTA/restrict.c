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
#include "gta.h"

void gtaRestrict(GTA *g)
{
  int i;
  for (i = 0; i < g->ss[0].size; i++)
    if (g->final[i] == -1)
      g->final[i] = 0; /* turn rejects into don't-cares */
}

void gtaUnrestrict(GTA *g)
{
  int i;
  for (i = 0; i < g->ss[0].size; i++)
    if (g->final[i] == 0)
      g->final[i] = -1; /* turn don't-cares into rejects */
}

